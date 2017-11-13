"""
Workspace implemented over files, using the mongomock package.
"""
__author__ = 'Dan Gunter <dkgunter@lbl.gov>'
__date__ = '9/3/15'

# Imports

# Stdlib
try:
    import cStringIO as StringIO
except:
    import StringIO

import copy
import json
import logging
import msgpack
import os
import re
import sys
from datetime import datetime
# Third-party
import dpath.util
# Local
from doekbase.data_api.util import get_logger, log_start, log_end
from doekbase.workspace.baseclient import ServerError

# Logging

_log = get_logger(__name__)

# Globals

NUMERIC_REF_PAT = re.compile('\d+/\d+(/\d+)?')
OBJECT_MAPPING_FILE = 'object_mapping.txt'

# Persist a single WorkspaceFile instance per directory of test data
FILE_STORES = {}

# Exceptions

class LibError(ServerError):
    """To imitate server errors, raise this with a description
    of the error as the argument.
    """
    def __init__(self, description):
        super(LibError, self).__init__('ServerError', -32500, description)

# Functions and classes

ws_url_template = 'https://{}.kbase.us/services/ws/'

def workspace_to_file(ref, workspace='narrative', token=None):
    """Convert Workspace objects to the JSON format read by the
    mongomock module.

    Args:
      ref (str): Workspace object reference e.g. '1019/4/1'
      workspace (str): Name or full URL for workspace to contact; 'narrative'
        or 'ci' are recognized
      token (str): KBase auth token

    Return:
       (dict) Object in the mock schema
    """
    from doekbase.workspace.client import Workspace
    if re.match(r'https://.*', workspace):
        url = workspace
    else:
        url = ws_url_template.format(workspace)
    if token is None:
        token = os.environ.get('KB_AUTH_TOKEN', '')
        if not token:
            raise ValueError('No `token` given and environment does not '
                             'contain value for KB_AUTH_TOKEN')
    ws = Workspace(url, token=token)
    objlist = ws.get_objects([{'ref': ref}])
    obj, oi = objlist[0], objlist[0]['info']
    canonical_ref = "{0}/{1}/{2}".format(oi[6], oi[0], oi[4])
    canonical_name = "{0}/{1}/{2}".format(oi[7], oi[1], oi[4])
    # convert to our schema
    d = {'ref': canonical_ref,
         'type': oi[2],
         'name': canonical_name,
         'links': obj['refs'],
         'data': obj['data'],
         'metadata': oi[10]
         }
    _log.debug('workspace_to_file: returning record for: {}'
               .format(canonical_ref))
    return d


def workspace_file_client(working_directory):
    if working_directory in FILE_STORES:
        return FILE_STORES[working_directory]
    else:
        return WorkspaceFile(working_directory)


class WorkspaceFile(object):
    """Mock object for KBase Workspace service.

    You can use this in place of the doekbase.client.workspace.Workspace class.

    To insulate from changes in the workspace storage format, the input
    data is in a simplified and reduced schema. The input should be a list
    of JSON ojects, separated by commas and bracketed by "[ ]" like a
    normal JSON list. Each object should have these fields:

    * ref - object reference like "123/4"
    * type - Name of the type of this object, e.g. "FooType"
    * name - Name of this object, e.g. "ReferenceGenomeAnnotations/kb|g.3157"
    * links - List of references, each in the same form as the 'ref' field.
    * data - JSON object with the data (whatever you want)
    """

    #: Use MessagePack encoding for workspace objects
    use_msgpack = True
    use_redis = False
    _loaded = []      # static cache of loaded refs
    _mapping = {}     # mapping between ref and stuffed object data
    _links = {}       # references between objects
    _file_map = {}    # mapping between refs and filenames
    _canonicals = {}  # mapping from other refs to canonical ws/obj/ver refs

    #: Version of the workspace we are emulating
    VERSION = '0.5.0'

    def __init__(self, working_directory):
        """Create file-based Workspace instance, using files in
        the given working directory.

        Additional files are added with the `load` method.

        Args:
          working_directory (str): Path to directory with files to load.
        """
        self._wd = working_directory
        # create client and collection
        #client = mm.MongoClient()
        #self._mongodb = client['test_data']
        #self.collection = self._mongodb.create_collection("ws_objects")
        # This monkey-patch avoids a copy of the parsed workspace object
        # as it is added to the mongomock collection. Of course, this
        # means that this dict MUST be treated as immutable by other code.
        #self.collection._internalize_dict = lambda d: d
        # some internal state
        self._oids = {}
        FILE_STORES[working_directory] = self
        self._load_filemap()

    def load(self, ref):
        """Load data from a given reference.

        The reference will be translated into a file to load,
        using the following formula:
        ``<working_directory> + '/' + <ref> + <ext>`,
        where ``<working_directory>`` is the path given to the class
        constructor, ``<ref>`` is the reference given to this
        function, and
        ``<ext>`` is a file extension '.msgpack' if
        `use_msgpack` is True and '.json' otherwise.

        Thus, for ``WorkspaceFile('/tmp/data').load('foo_bar')``,
        the path loaded would be '/tmp/data/foo_bar.msgpack'.

        See class documentation on format of input data.

        Args:
          ref (str): The reference

        Notes:
          * Post-condition: Object is loaded if and only if that reference was
            not loaded previously. Modification timestamp of the underlying
            file is NOT checked, you must manually invalidate modified
            data with :meth:`unload(ref)`.

        Raises:
          IOError: file not found or not readable.
          ValueError: parsing failed.
        """
        # log start
        t0 = log_start(_log, 'WorkspaceFile.load', level=logging.DEBUG,
                       kvp=dict(ref=ref))
        # stop if already loaded in the past
        if ref in self._mapping:
            # log done and return
            log_end(_log, t0, 'WorkspaceFile.load', level=logging.DEBUG,
                    kvp=dict(ref=ref, cached='yes'))
            return
        # cache the parsed data, both by reference and by 'name'
        # (if name is not the same as reference)
        #print("@@ REF={r} RECORD[ref]={rr} RECORD[name]={n}"
        #      .format(r=ref, rr=record['ref'], n=record['name']))
        self._set_record(ref)

        #print('@@ STORE RECORD BY ({},{})'.format(record['ref'], record['name']))
        #print('@@ Links {}'.format(self._links[record['ref']]))
        # insert the parsed data into mongomock
        #self.collection.insert_one(record)
        # log done
        log_end(_log, t0, 'WorkspaceFile.load', level=logging.DEBUG,
                kvp=dict(ref=ref, cached='no'))

    def unload(self, ref):
        """Force reload of ``ref`` the next time.
        Does nothing if ``ref`` is not already loaded.

        Args:
          ref (str): The reference
        Post:
           ref is no longer loaded
        """
        self._del_record(ref)

    # Public methods

    def copy_object(self, prm):
        # do nothing
        return

    def get_object_history(self, prm):
        return []

    def get_object_info_new(self, prm):
        ref = prm['objects'][0]['ref']
        records = self._find_ref(ref)
        result = [self._make_info_tuple(r) for r in records]
        return result

    def get_object_provenance(self, prm):
        return []

    def get_object_subset(self, prm):
        """Note: this is not efficient. It actually looks at
        the whole object.
        """
        def extract_subset_glob(d, parts):
            if isinstance(d, dict):
                _e = {n: extract_subset(d[n], parts) for n in d}
            elif isinstance(d, list):
                _e = [extract_subset(d[n], parts) for n in xrange(len(d))]
            else:
                raise Exception("Unknown behavior for type {}".format(type(d)))

            return _e

        def extract_subset(d, parts, partial=False):
            if partial:
                extent = len(parts)
            else:
                extent = len(parts) - 1

            subset = {}
            _e = subset
            _d = d
            for i in xrange(extent):
                if isinstance(_e, dict) and parts[i] in _e:
                    _e = _e[parts[i]]
                    _d = _d[parts[i]]
                elif isinstance(_e, list) and int(parts[i]) < len(_e):
                    _e = _e[int(parts[i])]
                    _d = _d[int(parts[i])]
                elif isinstance(_d, dict):
                    if parts[i] not in _d:
                        continue

                    if isinstance(_d[parts[i]], dict):
                        _e[parts[i]] = {}
                    elif isinstance(_d[parts[i]], list):
                        _e[parts[i]] = []
                    else:
                        _e[parts[i]] = _d[parts[i]]

                    _e = _e[parts[i]]
                    _d = _d[parts[i]]
                elif isinstance(_d, list):
                    if parts[i] not in _d:
                        continue

                    if isinstance(_d[parts[i]], dict):
                        _e.append({})
                    elif isinstance(d[parts[i]], list):
                        _e.append([])
                    else:
                        _e.append(d[parts[i]])

                    _e = _e[-1]
                    _d = _d[parts[i]]

            if not partial:
                # full copy of last element
                try:
                    _e[parts[-1]] = _d[parts[-1]]
                except KeyError:
                    pass

            return subset

        # loop over each specified subset, and add all results
        # to a single list in `result`
        result = []
        for subset in prm:
            ref, paths = subset['ref'], subset['included']
            # get matching records and data in the paths
            record = self._find_ref(ref)[0]
            # add to result
            extracted = {}
            for p in paths:
                parts = p.split('/')
                # special case where you need glob selections
                if '*' in p:
                    # split the path before and after the glob
                    if '*' in parts:
                        pivot = parts.index('*')
                    elif '[*]' in parts:
                        pivot = parts.index('[*]')
                    else:
                        raise Exception("Unrecognized syntax {}".format(p))

                    pre = parts[:pivot]
                    post = parts[pivot + 1:]
                    # extract the non-glob portion first
                    dpath.util.merge(extracted, extract_subset(record['data'], pre, True))
                    # position the pointer to each object
                    e = extracted
                    d = record['data']
                    for i in xrange(len(pre) - 1):
                        d = d[pre[i]]
                        e = e[pre[i]]

                    glob_data = extract_subset_glob(d[pre[-1]], post)

                    if isinstance(glob_data, list):
                        if len(e[pre[-1]]) == len(glob_data):
                            if isinstance(glob_data[0], dict):
                                for i in xrange(len(glob_data)):
                                    e[pre[-1]][i].update(glob_data[i])
                            elif isinstance(glob_data[0], list):
                                for i in xrange(len(glob_data)):
                                    e[pre[-1]][i] += glob_data[i]
                            else:
                                raise Exception("Unexpected condition at {}, "
                                        + "expected dict or list, found {}".format(pre[-1], type(glob_data)))
                        elif len(e[pre[-1]]) == 0:
                            e[pre[-1]] = glob_data
                    else:
                        dpath.util.merge(e[pre[-1]], glob_data)
                elif '/' in p:
                    dpath.util.merge(extracted, extract_subset(record['data'], parts))
                else:
                    if p in record['data']:
                        extracted[p] = record['data'][p]

            if len(extracted) > 0:
                #print("@@ add extracted: {}".format(extracted))
                obj = self._make_object(record, data=extracted)
                result.append(obj)

        return result

    def get_objects(self, prm):
        result = []
        for refs in prm:
            ref = refs['ref']
            records = self._find_ref(ref)
            #print("@@ GO, got records: {}".format(records))
            objects = [self._make_object(record) for record in records]
            result.extend(objects)
        return result

    def get_objects2(self, prm):
        result = []
        for refs in prm['objects']:
            ref_spec = refs.copy()

            if 'obj_ref_path' in refs:
                # set ref to target object at end of reference chain
                ref_spec['ref'] = refs['obj_ref_path'][-1]
                del ref_spec['obj_ref_path']
            else:
                ref_spec['ref'] = refs['ref']

            if 'included' in refs:
                result.extend(self.get_object_subset([ref_spec]))
            else:
                records = self._find_ref(ref_spec['ref'])
                #print("@@ GO, got records: {}".format(records))
                objects = [self._make_object(record) for record in records]
                result.extend(objects)
        return {'data': result}

    def get_type_info(self, type_name):
        return self._make_type_info({'type': type_name})

    def list_referencing_objects(self, prm):
        #print("@@ list_referencing_objects({})".format(prm))
        # use the object mapping to load any missing object data for references
        self._load_all_files()

        result = []
        for refs in prm:
            ref_result = []
            ref = refs['ref']

            if ref in self._links:
                # find every record that refers to this one
                for r in self._links[ref]:
                    try:
                        record = self._get_record(r)
                        info_tuple = self._make_info_tuple(record)
                        ref_result.append(info_tuple)
                    except KeyError:
                        raise IOError("Missing object data for {}".format(r))

            result.append(ref_result)
        return result

    def translate_to_MD5_types(self, types):
        m = {}
        for t in types:
            if t in MD5_TYPES:
                m[t] = MD5_TYPES[t]
            else:
                raise LibError('Type schema record was not found for {}'
                                  .format(t))
        return m

    def ver(self):
        return self.VERSION

    def get_children(self):
        return []

    def save_objects(self, data=None):
        return True

    # ___ Internal methods ___

    def _get_oid(self, ref):
        if ref in self._oids:
            return self._oids[ref]
        new_oid = (len(self._oids) + abs(hash(ref))) % sys.maxint
        self._oids[ref] = new_oid
        return new_oid

    def _make_info(self, record):
        """Make and return a single 'info' section.
        """
        assert re.match(NUMERIC_REF_PAT, record['ref'])  # require numeric ref
        #print("@@ make_info from: {}".format(record))
        ws_id, obj_id, ver = [int(x) for x in record['ref'].split('/')]
        data = record['data']
        info = {'object_id': obj_id,
                'object_name': 'Object{:d}'.format(obj_id),
                'object_reference': '{}/{}'.format(ws_id, obj_id),
                'object_reference_versioned': '{}/{}'.format(ws_id, obj_id, '1'),
                'type_string': record['type'],
                'save_date': datetime.isoformat(datetime.now()),
                'version': 1,
                'saved_by': 'CookieMonster',
                'workspace_id': ws_id,
                'workspace_name': record['name'],
                'object_checksum': 0,
                'object_size': len(data),
                'object_metadata': record['metadata']
                }
        record = None
        return info

    def _make_info_tuple(self, record):
        """Make the object_info type tuple:

        0: obj_id objid, 1: obj_name name,
        2: type_string type, 3: timestamp save_date,
        4: int version, 5: username saved_by,
		6: ws_id wsid, 7: ws_name workspace,
		8: string chsum, 9: int size, 10: usermeta meta
        """
        assert re.match(NUMERIC_REF_PAT, record['ref'])  # require numeric ref
        wsid, obj_id, ver = [int(x) for x in record['ref'].split('/')]
        return (obj_id, record['name'],
                record['type'], datetime.isoformat(datetime.utcnow()),
                ver, 'joe',
                wsid, record['name'],
                '0', 0, {}
                )

    def _make_object(self, record, data=None):
        r = {
            'data': data or record['data'],
            'info': self._make_info(record),
            'provenance': [],
            'creator': 'Gonzo',
            'created': datetime.isoformat(datetime.now()),
            'refs': [],
            'copied': '',
            'copy_source_inaccessible': 0,
            'extracted_ids': {},
            'handle_error': '',
            'handle_stacktrace': ''
        }
        return r

    def _make_type_info(self, record):
        r = {
            'type_string': record['type'],
            'description': 'This is type {}'.format(record['type']),
            # 'spec_def': '',
            # 'json_schema': '{}',
            # 'parsing_structure': '{}',
            # 'module_vers': [1],
            # 'released_module_vers': [1],
            # 'type_vers' : ['1'],
            # 'released_type_vers': ['1'],
            # 'using_func_defs': [],
            # 'using_type_defs': [],
            # 'used_type_defs': []
        }
        return r

    def _find_ref(self, ref):
        """Find records by reference.

        Args:
          ref (str): numeric or named object reference
        Returns:
          list of records (may be an empty list)
        """
        #print("@@ looking for REF={} in KEYS={}".format(ref, self._loaded.keys()))
        if ref in self._mapping:
            return [self._get_record(ref)]
        elif ref in self._file_map:
            self.load(self._file_map[ref])
            return [self._get_record(ref)]
        else:
            raise IOError("File for {} does not exist".format(ref))

    def _load_all_files(self):
        for ref in self._file_map:
            if ref not in self._mapping:
                self.load(self._file_map[ref])

    def _load_filemap(self):
        map_filename = os.path.join(self._wd, OBJECT_MAPPING_FILE)
        try:
            map_file = open(map_filename, 'r')
            self._file_map = dict([x.strip().split() for x in map_file.readlines()])
            map_file.close()
            return self._file_map
        except IOError, e:
            if not os.path.exists(map_filename):
                raise IOError("File not found: {}".format(map_filename))
            else:
                raise

    def _parse_record(self, path):
        # open the file; raises IOError on failure
        with open(path, 'r') as f:
            if self.use_msgpack:
                data = msgpack.load(f)
            else:
                data = json.load(f)
        return data

    def _del_record(self, ref):
        if ref in self._mapping:
            del self._links[ref]
            del self._loaded[self._mapping[ref]]
            del self._mapping[ref]

    def _set_record(self, ref):
        # create the full path from the reference
        ext = 'msgpack' if self.use_msgpack else 'json'
        full_path = '{}.{}'.format(os.path.join(self._wd, ref), ext)
        # parse the file
        record = self._parse_record(full_path)
        position = len(self._loaded)
        self._canonicals[ref] = record['ref']
        self._canonicals[record['name']] = record['ref']
        self._mapping[ref] = position
        self._mapping[record['ref']] = position
        self._mapping[record['name']] = position
        self._links[record['ref']] = record['links']
        self._loaded.append(msgpack.dumps(record))
        # dump the memory
        record = None

    def _get_record(self, ref):
        return msgpack.loads(self._loaded[self._mapping[ref]])


####

MD5_TYPES = {
    u'KBaseGenomes.Genome-0.1': u'KBaseGenomes.Genome-1e1fce431960397da77cb092d27a50cf',
    u'KBaseGenomes.Genome-1.0': u'KBaseGenomes.Genome-1e1fce431960397da77cb092d27a50cf',
    u'KBaseGenomes.Genome-2.0': u'KBaseGenomes.Genome-e0979de9df4baccca8bdd95f7565fde4',
    u'KBaseGenomes.Genome-3.0': u'KBaseGenomes.Genome-225de07e59f4fdc5d9b8bf0bcd12c498',
    u'KBaseGenomes.Genome-4.0': u'KBaseGenomes.Genome-c0526fae0ce1fd8d342ec94fc4dc510a',
    u'KBaseGenomes.Genome-5.0': u'KBaseGenomes.Genome-c0526fae0ce1fd8d342ec94fc4dc510a',
    u'KBaseGenomes.Genome-6.0': u'KBaseGenomes.Genome-aafaaa7df90d03b33258f4fa7790dcbe',
    u'KBaseGenomes.Genome-7.0': u'KBaseGenomes.Genome-93da9d2c8fb7836fb473dd9c1e4ca89e',
    u'KBaseGenomes.Genome-8.0': u'KBaseGenomes.Genome-51b05a5c27084ae56106e60df5b66df5',
    u'KBaseGenomes.ContigSet-3.0': u'KBaseGenomes.ContigSet-db7f518c9469d166a783d813c15d64e9',
    u'KBaseGenomeAnnotations.AnnotationQuality-0.1': u'KBaseGenomeAnnotations.AnnotationQuality-477a5cc8e4eef9a07eddea445d5b3e03',
    u'KBaseGenomeAnnotations.AnnotationQuality-1.0': u'KBaseGenomeAnnotations.AnnotationQuality-477a5cc8e4eef9a07eddea445d5b3e03',
    u'KBaseGenomeAnnotations.Assembly-0.1': u'KBaseGenomeAnnotations.Assembly-5702392af48de51769471473571ffb1a',
    u'KBaseGenomeAnnotations.Assembly-1.0': u'KBaseGenomeAnnotations.Assembly-5702392af48de51769471473571ffb1a',
    u'KBaseGenomeAnnotations.Assembly-2.0': u'KBaseGenomeAnnotations.Assembly-47f14e00d8ce648a1fdc5b9e091cd11f',
    u'KBaseGenomeAnnotations.Assembly-3.0': u'KBaseGenomeAnnotations.Assembly-ef6feebefd027c4d9239eaae70a85b26',
    u'KBaseGenomeAnnotations.Assembly-4.0': u'KBaseGenomeAnnotations.Assembly-86718020e600a669b3e6e933691a8f71',
    u'KBaseGenomeAnnotations.Assembly-4.1': u'KBaseGenomeAnnotations.Assembly-cb3a414bf249d6fe99ad4cc6f688a12f',
    u'KBaseGenomeAnnotations.EvidenceContainer-0.1': u'KBaseGenomeAnnotations.EvidenceContainer-ffd466ca300b0c9479a2eee1aa4d53be',
    u'KBaseGenomeAnnotations.EvidenceContainer-1.0': u'KBaseGenomeAnnotations.EvidenceContainer-ffd466ca300b0c9479a2eee1aa4d53be',
    u'KBaseGenomeAnnotations.FeatureContainer-0.1': u'KBaseGenomeAnnotations.FeatureContainer-77ee3036a791592496e3852b3c9e87b4',
    u'KBaseGenomeAnnotations.FeatureContainer-1.0': u'KBaseGenomeAnnotations.FeatureContainer-77ee3036a791592496e3852b3c9e87b4',
    u'KBaseGenomeAnnotations.FeatureContainer-1.1': u'KBaseGenomeAnnotations.FeatureContainer-62dd2f0f35bb36532ff4c9b297e9b25c',
    u'KBaseGenomeAnnotations.FeatureContainer-2.0': u'KBaseGenomeAnnotations.FeatureContainer-f185d243be5f27ce0166884be6db7468',
    u'KBaseGenomeAnnotations.GenomeAnnotation-0.1': u'KBaseGenomeAnnotations.GenomeAnnotation-994bc5d281b14ae29d2759bce9d59703',
    u'KBaseGenomeAnnotations.GenomeAnnotation-0.2': u'KBaseGenomeAnnotations.GenomeAnnotation-34168943eac1c2fd0746655790a63afe',
    u'KBaseGenomeAnnotations.GenomeAnnotation-1.0': u'KBaseGenomeAnnotations.GenomeAnnotation-34168943eac1c2fd0746655790a63afe',
    u'KBaseGenomeAnnotations.GenomeAnnotation-1.1': u'KBaseGenomeAnnotations.GenomeAnnotation-2b8b3742f75674d42b36c80fc70a9720',
    u'KBaseGenomeAnnotations.GenomeAnnotation-1.2': u'KBaseGenomeAnnotations.GenomeAnnotation-4e3548f42c702292942c966a6cc6a3e5',
    u'KBaseGenomeAnnotations.GenomeAnnotation-2.0': u'KBaseGenomeAnnotations.GenomeAnnotation-1b53ce5438e8208722827e386d0ba95f',
    u'KBaseGenomeAnnotations.GenomeAnnotation-2.1': u'KBaseGenomeAnnotations.GenomeAnnotation-062b1d9208a5b89a35fc3988854be208',
    u'KBaseGenomeAnnotations.GenomeAnnotation-3.0': u'KBaseGenomeAnnotations.GenomeAnnotation-ed01d109e2b540042ce9d73042fc0584',
    u'KBaseGenomeAnnotations.GenomeAnnotation-3.1': u'KBaseGenomeAnnotations.GenomeAnnotation-dc8e1dfa968ab90dae03811021fcab77',
    u'KBaseGenomeAnnotations.GenomeAnnotationSet-0.1': u'KBaseGenomeAnnotations.GenomeAnnotationSet-a1c6a7e69da3d38e403b8bac4e312a23',
    u'KBaseGenomeAnnotations.GenomeAnnotationSet-1.0': u'KBaseGenomeAnnotations.GenomeAnnotationSet-a1c6a7e69da3d38e403b8bac4e312a23',
    u'KBaseGenomeAnnotations.GenomeAnnotationSummary-1.0': u'KBaseGenomeAnnotations.GenomeAnnotationSummary-6e2bf073a1647761af481b7b78471b2d',
    u'KBaseGenomeAnnotations.GenomeAnnotationSummary-2.0': u'KBaseGenomeAnnotations.GenomeAnnotationSummary-86fafbc48745ddfde386db6ace65a05c',
    u'KBaseGenomeAnnotations.GenomeAnnotationSummary-3.0': u'KBaseGenomeAnnotations.GenomeAnnotationSummary-fe21b69fc95646c5d552d6808e191265',
    u'KBaseGenomeAnnotations.ProteinContainer-0.1': u'KBaseGenomeAnnotations.ProteinContainer-24986e79a34d6c0800b2008c974015b4',
    u'KBaseGenomeAnnotations.ProteinContainer-1.0': u'KBaseGenomeAnnotations.ProteinContainer-24986e79a34d6c0800b2008c974015b4',
    u'KBaseGenomeAnnotations.SeedRoles-0.1': u'KBaseGenomeAnnotations.SeedRoles-4633e4a9703e27c7b6e6760c8ec5f893',
    u'KBaseGenomeAnnotations.SeedRoles-1.0': u'KBaseGenomeAnnotations.SeedRoles-4633e4a9703e27c7b6e6760c8ec5f893',
    u'KBaseGenomeAnnotations.Taxon-0.1': u'KBaseGenomeAnnotations.Taxon-6367e669a33764f466bb0c71628e3b22',
    u'KBaseGenomeAnnotations.Taxon-1.0': u'KBaseGenomeAnnotations.Taxon-6367e669a33764f466bb0c71628e3b22',
    u'KBaseGenomeAnnotations.TaxonLookup-0.1': u'KBaseGenomeAnnotations.TaxonLookup-c5ce71324217b089cb8a17eda359a8f6',
    u'KBaseGenomeAnnotations.TaxonLookup-1.0': u'KBaseGenomeAnnotations.TaxonLookup-c5ce71324217b089cb8a17eda359a8f6',
    u'KBaseGenomeAnnotations.TaxonLookup-2.0': u'KBaseGenomeAnnotations.TaxonLookup-75222de8c337d6d4f53943cd1e5a59aa',
    u'KBaseGenomeAnnotations.TaxonSet-0.1': u'KBaseGenomeAnnotations.TaxonSet-e4b647bbc4d7965a8def8909b10c6b9e',
    u'KBaseGenomeAnnotations.TaxonSet-1.0': u'KBaseGenomeAnnotations.TaxonSet-e4b647bbc4d7965a8def8909b10c6b9e'
}

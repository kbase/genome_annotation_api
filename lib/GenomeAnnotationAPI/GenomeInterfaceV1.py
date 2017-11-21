import requests
import json
import os
import re
from collections import defaultdict
from requests_toolbelt.multipart.encoder import MultipartEncoder

from Workspace.WorkspaceClient import Workspace
from biokbase.AbstractHandle.Client import AbstractHandle as HandleService  # @UnresolvedImport @IgnorePep8
from biokbase.AbstractHandle.Client import ServerError as HandleError  # @UnresolvedImport @IgnorePep8
from AssemblySequenceAPI.AssemblySequenceAPIServiceClient import AssemblySequenceAPI
from DataFileUtil.DataFileUtilClient import DataFileUtil


class GenomeInterfaceV1:
    def __init__(self, services):
        self.ws = Workspace(services['workspace_service_url'])
        self.handle_url = services['handle_service_url']
        self.shock_url = services['shock_service_url']
        self.sw_url = services['service_wizard_url']
        self.dfu = DataFileUtil(os.environ['SDK_CALLBACK_URL'])
        self.taxon_wsname = 'ReferenceTaxons'

    # Input params:
    # typedef structure {
    #     string ref;
    #     list <int> included_feature_position_index;
    #     list <string> ref_path_to_genome;
    # } GenomeSelectorV1;
    #
    # typedef structure {
    #     list <GenomeSelectorV1> genomes;

    #     list <string> included_fields;
    #     list <string> included_feature_fields;

    #     boolean ignore_errors;
    #     boolean no_data;
    #     boolean no_metadata;
    # } GetGenomeParamsV1;
    #
    def get_genome(self, ctx, params):

        object_specifications = self.build_object_specifications(params)

        getObjParams = {'objects': object_specifications}

        if 'ignoreErrors' in params:
            if params['ignoreErrors']==0:
                getObjParams['ignoreErrors']=0
            elif params['ignoreErrors']==1:
                getObjParams['ignoreErrors']=1
            else:
                raise ValueError('ignoreErrors input field must be set to 0 or 1')
        else:
            getObjParams['ignoreErrors']=0

        if 'no_data' in params:
            if params['no_data']==0:
                getObjParams['no_data']=0
            elif params['no_data']==1:
                getObjParams['no_data']=1
            else:
                raise ValueError('no_data input field must be set to 0 or 1')
        else:
            getObjParams['no_data']=0

        #self.validate_proper_ws_type(object_specifications, getObjParams['ignoreErrors'], 'KBaseGenomes.Genome')
        data = self.ws.get_objects2(getObjParams)['data']

        if 'no_metadata' in params:
            if params['no_metadata']==1:
                d2 = []
                for obj in data:
                    d2.append({'data':obj['data']})
                data = d2

        returnPackage = { 'genomes':data }
        return returnPackage

    def build_object_specifications(self,params):

        if 'genomes' not in params:
            raise ValueError('Invalid input - "genomes" input argument field is missing.')
        genomes = params['genomes']

        included_fields = []
        if 'included_fields' in params:
            included_fields = params['included_fields']

        included_feature_fields = []
        if 'included_feature_fields' in params:
            included_feature_fields = params['included_feature_fields']

        # typedef structure {
        #     ws_name workspace;
        #     ws_id wsid;
        #     obj_name name;
        #     obj_id objid;
        #     obj_ver ver;
        #     obj_ref ref;
        #     ref_chain obj_path;
        #     list<obj_ref> obj_ref_path;
        #     list<object_path> included;
        #     boolean strict_maps;
        #     boolean strict_arrays;
        # } ObjectSpecification;

        object_specifications = []
        for g in genomes:
            # create the WS object selector, include the basic fields specified
            ref_path_to_genome = []
            if 'ref_path_to_genome' in g:
                ref_path_to_genome = g['ref_path_to_genome']
            selector = self.create_base_object_spec(g['ref'],ref_path_to_genome)
            included = included_fields

            # if there are specific features selected, get those
            if 'included_feature_position_index' in g and len(g['included_feature_position_index'])>0:
                for pos in g['included_feature_position_index']:
                    base = 'features/'+str(pos)
                    included_feature_paths = self.create_feature_selectors(base, included_feature_fields)
                    for p in included_feature_paths:
                        included.append(p)
            # no selected features, but if included_feature_fields is defined, do that
            elif len(included_feature_fields) >0:
                included_feature_paths = self.create_feature_selectors('features/[*]', included_feature_fields)
                for p in included_feature_paths:
                    included.append(p)

            selector['included'] = included

            object_specifications.append(selector)
        return object_specifications

    def create_feature_selectors(self, base, included_feature_fields):
        included = []
        if len(included_feature_fields)>0:
            for f in included_feature_fields:
                included.append( base + '/' + f)
        else:
            included = [base]
        return included

    def validate_proper_ws_type(self, object_specifications, ignore_errors, type_name):
        info = self.ws.get_object_info_new({
                                'objects': object_specifications,
                                'ignoreErrors': ignore_errors,
                                'includeMetadata': 0
                            })
        # Make sure type name matches, no check for version yet!
        for i in info:
            if i is not None:
                if i[2].split('-')[0] != type_name:
                    raise ValueError('An input object reference is not a '+type_name+'. It was: '+i[2])

    def create_base_object_spec(self, genome_ref, ref_path_to_genome):
        if ref_path_to_genome is not None:
            if len(ref_path_to_genome)>0:
                obj_ref_path = []
                for r in ref_path_to_genome[1:]:
                    obj_ref_path.append(r)
                obj_ref_path.append(genome_ref)

                return {
                    'ref': ref_path_to_genome[0],
                    'obj_ref_path':obj_ref_path
                }
        return { 'ref':genome_ref }

    def save_one_genome(self, ctx, params):
        """
        typedef structure {
            string workspace;
            string name;
            KBaseGenomes.Genome data;
            list<Workspace.ProvenanceAction> provenance;
            boolean hidden;
        } SaveOneGenomeParamsV1;

        typedef structure {
            Workspace.object_info info;
        } SaveGenomeResultV1;
        """

        if 'workspace' not in params:
            raise ValueError('workspace parameter (giving WS name or ID) is required')
        if 'name' not in params:
            raise ValueError('name parameter (giving new genome object name) is required')
        if 'data' not in params:
            raise ValueError('data parameter (giving new genome object data) is required')

        workspace = params['workspace']
        name = params['name']
        data = params['data']

        # Let's check that all handles point to shock nodes owned by calling user
        self.own_handle(data, 'genbank_handle_ref', ctx)
        self.own_handle(data, 'gff_handle_ref', ctx)

        self.check_dna_sequence_in_features(data, ctx)

        provenance = None
        if 'provenance' in params:
            provenance = params['provenance']
        elif 'provenance' in ctx:
            provenance = ctx['provenance']
            for prov_item in provenance:
                if ('service' not in prov_item) or (prov_item['service'] != 'GenomeAnnotationAPI'):
                    continue
                if ('method' not in prov_item) or (prov_item['method'] != 'save_one_genome_v1'):
                    continue
                if 'method_params' not in prov_item:
                    continue
                input_array = prov_item['method_params']
                if len(input_array) != 1:
                    continue
                input_obj = input_array[0]  # SaveOneGenomeParamsV1 type
                if 'data' in input_obj:
                    input_obj['data'] = "<large-data-excluded>"

        hidden = 0
        if 'hidden' in params:
            if params['hidden']==0:
                hidden=0
            elif params['hidden']==1:
                hidden=1
            else:
                raise ValueError('hidden parameter must be set to 0 or 1; it was: '+str(hidden))

        """
        If the closeness_measure values are of type string convert to float before saving
        """
        close_genomes = data.get('close_genomes')
        if close_genomes and len(close_genomes) > 0:

            for close_genome in close_genomes:
                closeness_measure = close_genome.get('closeness_measure')
                if not isinstance(closeness_measure, float):
                    try:
                        close_genome['closeness_measure'] = float(closeness_measure)
                    except:
                        raise TypeError('Invalid closeness_measure value "{}": float expected'
                                        .format(closeness_measure))
        save_params = {
            'objects': [{
                'name': name,
                'data': data,
                'type': 'KBaseGenomes.Genome',
                'provenance': provenance,
                'hidden': hidden
            }]
        }

        if str(workspace).isdigit():
            save_params['id'] = int(workspace)
        else:
            save_params['workspace'] = workspace

        results = self.ws.save_objects(save_params)

        if len(results) != 1:
            raise ValueError('Error saving data.  Workspace did not return proper object info list')

        return {'info': results[0]}

    def _update_genome(self, genome):
        """Checks for missing required fields and fixes breaking changes"""
        # do top level updates
        if 'genome_tier' not in genome:
            genome['source'], genome['genome_tiers'] = self.determine_tier(
                genome['source'])
        if 'molecule_type' not in genome:
            genome['molecule_type'] = 'Unknown'
        if 'taxon_ref' not in genome:
            genome['taxonomy'], genome['taxon_ref'], genome['domain'] \
                = self.retrieve_taxon(self.taxon_wsname,
                                      genome['scientific_name'])
        if any([x not in genome for x in ('dna_size', 'md5', 'gc_content')]):
            assembly_data = self.dfu.get_objects(
                {'object_refs': [genome['assembly_ref']],
                 'ignore_errors': 0})['data'][0]['data']
            genome["gc_content"] = assembly_data['gc_content']
            genome["dna_size"] = assembly_data['dna_size']
            genome["md5"] = assembly_data['md5']

        if 'cdss' not in genome:
            genome['cdss'] = []
        if 'mrnas' not in genome:
            genome['mrnas'] = []

        # do feature level updates
        retained_features = []
        type_counts = defaultdict(int)
        for field in ('mrnas', 'cdss', 'features'):
            for i, feat in enumerate(genome.get(field, [])):
                if 'function' in feat and not isinstance(feat, list):
                    feat['function'] = [feat['function']]
                if 'aliases' in feat:
                    feat['aliases'] = [['db_xref', x] for x in feat['aliases']]
                if 'type' in feat:
                    type_counts[feat['type']] += 1
                # TODO: Ontologies

                # split all the stuff lumped together in old versions into the
                # right arrays
                if field == 'features':
                    if feat.get('type', 'gene') == 'gene':
                        if not feat.get('cdss', []):
                            genome['non_coding_features'].append(feat)
                        else:
                            retained_features.append(feat)
                    elif feat.get('type', 'gene') == 'CDS':
                        if 'protein_md5' not in feat:
                            feat['protein_md5'] = ''
                        if 'parent_gene' not in feat:
                            feat['parent_gene'] = ''
                        genome['cdss'].append(feat)
                    elif feat.get('type', 'gene') == 'mRNA':
                        genome['mrnas'].append(feat)

        genome['features'] = retained_features

        type_counts['mRNA'] = len(genome.get('mrnas', []))
        type_counts['CDS'] = len(genome.get('cdss', []))
        type_counts['protein_encoding_gene'] = len(genome['features'])
        type_counts['non-protein_encoding_gene'] = len(genome.get('non_coding_features', []))
        genome['feature_counts'] = type_counts

        return genome

    @staticmethod
    def retrieve_taxon(taxon_wsname, scientific_name):
        """
        _retrieve_taxon: retrieve taxonomy and taxon_reference

        """
        default = ('Unconfirmed Organism: ' + scientific_name,
                   'ReferenceTaxons/unknown_taxon', 'Unknown')
        solr_url = 'http://kbase.us/internal/solr-ci/search/'
        solr_core = 'taxonomy_ci'
        query = '/select?q=scientific_name:"{}"&fl=scientific_name%2Cscientific_lineage%2Ctaxonomy_id%2Cdomain&rows=5&wt=json'
        match = re.match("\S+\s?\S*", scientific_name)
        if not match:
            return default
        res = requests.get(solr_url + solr_core + query.format(match.group(0)))
        results = res.json()['response']['docs']
        if not results:
            return default
        taxonomy = results[0]['scientific_lineage']
        taxon_reference = '{}/{}_taxon'.format(
            taxon_wsname, results[0]['taxonomy_id'])
        domain = results[0]['domain']

        return taxonomy, taxon_reference, domain

    @staticmethod
    def determine_tier(source):
        """
        Given a user provided source parameter, assign a source and genome tier
        """
        low_source = source.lower()
        if 'refseq' in low_source:
            if 'reference' in low_source:
                return "Refseq", ['Reference', 'Representative',
                                  'ExternalDB']
            if 'representative' in low_source:
                return "Refseq", ['Representative', 'ExternalDB']
            return "Refseq", ['ExternalDB']
        if 'phytozome' in low_source:
            if 'flagship' in source:
                return "Phytosome", ['Reference', 'Representative',
                                     'ExternalDB']
            return "Phytosome", ['Representative', 'ExternalDB']
        if 'ensembl' in low_source:
            return "Ensembl", ['Representative', 'ExternalDB']
        return source, ['User']

    def check_dna_sequence_in_features(self, genome, ctx):
        if not 'features' in genome:
            return
        features_to_work = {}
        for feature in genome['features']:
            if not ('dna_sequence' in feature and feature['dna_sequence']):
                features_to_work[feature['id']] = feature['location']
        if len(features_to_work) > 0:
            aseq = AssemblySequenceAPI(self.sw_url, token=ctx['token'])
            get_dna_params = {'requested_features': features_to_work}
            if 'assembly_ref' in genome:
                get_dna_params['assembly_ref'] = genome['assembly_ref']
            elif 'contigset_ref' in genome:
                get_dna_params['contigset_ref'] = genome['contigset_ref']
            else:
                ## Nothing to do (it may be test genome without contigs)...
                return
            dna_sequences = aseq.get_dna_sequences(get_dna_params)['dna_sequences']
            for feature in genome['features']:
                if feature['id'] in dna_sequences:
                    feature['dna_sequence'] = dna_sequences[feature['id']]
                    feature['dna_sequence_length'] = len(feature['dna_sequence'])

    def own_handle(self, genome, handle_property, ctx):
        if not handle_property in genome:
            return
        token = ctx['token']
        handle_id = genome[handle_property]
        hs = HandleService(self.handle_url, token=token)
        handles = hs.hids_to_handles([handle_id])
        shock_id = handles[0]['id']

        ## Copy from DataFileUtil.own_shock_node implementation:
        header = {'Authorization': 'Oauth {}'.format(token)}
        res = requests.get(self.shock_url + '/node/' + shock_id +
                           '/acl/?verbosity=full',
                           headers=header, allow_redirects=True)
        self.check_shock_response(
            res, 'Error getting ACLs for Shock node {}: '.format(shock_id))
        owner = res.json()['data']['owner']['username']
        if owner != ctx['user_id']:
            shock_id = self.copy_shock_node(ctx, shock_id)
            r = requests.get(self.shock_url + '/node/' + shock_id,
                             headers=header, allow_redirects=True)
            errtxt = ('Error downloading attributes from shock ' +
                      'node {}: ').format(shock_id)
            self.check_shock_response(r, errtxt)
            shock_data = r.json()['data']
            handle = {'id': shock_data['id'],
                      'type': 'shock',
                      'url': self.shock_url,
                      'file_name': shock_data['file']['name'],
                      'remote_md5': shock_data['file']['checksum']['md5']
                      }
            handle_id = hs.persist_handle(handle)
            genome[handle_property] = handle_id

    def copy_shock_node(self, ctx, shock_id):
        token = ctx['token']
        if token is None:
            raise ValueError('Authentication token required!')
        header = {'Authorization': 'Oauth {}'.format(token)}
        source_id = shock_id
        if not source_id:
            raise ValueError('Must provide shock ID')
        mpdata = MultipartEncoder(fields={'copy_data': source_id})
        header['Content-Type'] = mpdata.content_type
        response = requests.post(
            # copy_attributes only works in 0.9.13+
            self.shock_url + '/node?copy_indexes=1',
            headers=header, data=mpdata, allow_redirects=True)
        self.check_shock_response(
            response, ('Error copying Shock node {}: '
                       ).format(source_id))
        shock_data = response.json()['data']
        shock_id = shock_data['id']
        del header['Content-Type']
        r = requests.get(self.shock_url + '/node/' + source_id,
                         headers=header, allow_redirects=True)
        errtxt = ('Error downloading attributes from shock ' +
                  'node {}: ').format(shock_id)
        self.check_shock_response(r, errtxt)
        attribs = r.json()['data']['attributes']
        if attribs:
            files = {'attributes': ('attributes',
                                    json.dumps(attribs).encode('UTF-8'))}
            response = requests.put(
                self.shock_url + '/node/' + shock_id, headers=header,
                files=files, allow_redirects=True)
            self.check_shock_response(
                response, ('Error setting attributes on Shock node {}: '
                           ).format(shock_id))
        return shock_id

    def check_shock_response(self, response, errtxt):
        if not response.ok:
            try:
                err = json.loads(response.content)['error'][0]
            except:
                # this means shock is down or not responding.
                self.log("Couldn't parse response error content from Shock: " +
                         response.content)
                response.raise_for_status()
            raise ValueError(errtxt + str(err))
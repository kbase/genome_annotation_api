# standard libraries
import ConfigParser
import functools
import logging
import os
import sys
import json
import time
import unittest
import shutil

# local imports
from biokbase.workspace.client import Workspace
from AssemblyUtil.AssemblyUtilClient import AssemblyUtil
from GenomeAnnotationAPI.GenomeAnnotationAPIImpl import GenomeAnnotationAPI
from GenomeAnnotationAPI.GenomeAnnotationAPIServer import MethodContext
from GenomeAnnotationAPI.authclient import KBaseAuth as _KBaseAuth

unittest.installHandler()

logging.basicConfig()
g_logger = logging.getLogger(__file__)
g_logger.propagate = False
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
g_logger.addHandler(log_handler)
g_logger.setLevel(logging.INFO)

def log(func):
    if not g_logger:
        raise Exception("Missing logger for @log")

    ENTRY_MSG = "Entering {} with inputs {} {}"
    EXIT_MSG = "Exiting {}"

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        g_logger.info(ENTRY_MSG.format(func.__name__, args, kwargs))
        result = func(*args, **kwargs)
        g_logger.info(EXIT_MSG.format(func.__name__))
        return result

    return wrapper


class GenomeAnnotationAPITests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        cls.cfg = {n[0]: n[1] for n in config.items('GenomeAnnotationAPI')}
        authServiceUrl = cls.cfg.get('auth-service-url',
                "https://kbase.us/services/authorization/Sessions/Login")
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'GenomeAnnotationAPI',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})

        cls.ws = Workspace(cls.cfg['workspace-url'], token=token)
        cls.impl = GenomeAnnotationAPI(cls.cfg)
        suffix = int(time.time() * 1000)
        wsName = "test_GenomeAnnotationAPI_" + str(suffix)
        cls.ws.create_workspace({'workspace': wsName})
        cls.wsName = wsName

        data = json.load(open('data/rhodobacter_contigs.json'))
        # save to ws
        save_info = {
            'workspace': wsName,
            'objects': [{
                'type': 'KBaseGenomes.ContigSet',
                'data': data,
                'name': 'rhodo_contigs'
            }]
        }
        info = cls.ws.save_objects(save_info)[0]
        contigset_ref = str(info[6]) + '/' + str(info[0]) + '/' + str(info[4])
        data = json.load(open('data/rhodobacter.json'))
        data['contigset_ref'] = contigset_ref
        # save to ws
        save_info = {
            'workspace': wsName,
            'objects': [{
                'type': 'KBaseGenomes.Genome',
                'data': data,
                'name': 'rhodobacter'
            }]
        }
        info = cls.ws.save_objects(save_info)[0]
        cls.old_genome_ref = str(info[6]) + '/' + str(info[0]) + '/' + str(
            info[4])
        print('created old test genome')

        assembly_file_path = os.path.join(cls.cfg['scratch'],
                                          'e_coli_assembly.fasta')
        shutil.copy('data/e_coli_assembly.fasta', assembly_file_path)
        au = AssemblyUtil(os.environ['SDK_CALLBACK_URL'])
        assembly_ref = au.save_assembly_from_fasta({
            'workspace_name': cls.wsName,
            'assembly_name': 'ecoli.assembly',
            'file': {'path': assembly_file_path}
        })
        data = json.load(open('data/new_ecoli_genome.json'))
        data['assembly_ref'] = assembly_ref
        # save to ws
        save_info = {
            'workspace': wsName,
            'objects': [{
                'type': 'NewTempGenomes.Genome',
                'data': data,
                'name': 'new_ecoli'
            }]
        }
        info = cls.ws.save_objects(save_info)[0]
        cls.new_genome_ref = str(info[6]) + '/' + str(info[0]) + '/' + str(info[4])
        print('created new test genome')

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.ws.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getType(self, ref=None):
        return self.ws.get_object_info_new({"objects": [{"ref": ref}]})[0][2]

    @log
    def test_get_taxon(self):
        inputs = {'ref': self.new_genome_ref}
        ret = self.impl.get_taxon(self.ctx, inputs)
        self.assertTrue(self.getType(ret[0]).startswith("KBaseGenomeAnnotations.Taxon"),
                        "ERROR: Invalid Genome reference {} from {}".format(ret[0], self.new_genome_ref))

    @log
    def test_get_taxon_old(self):
        inputs = {'ref': self.new_genome_ref}
        ret = self.impl.get_taxon(self.ctx, inputs)
        self.assertTrue(
            self.getType(ret[0]).startswith("KBaseGenomeAnnotations.Taxon"),
            "ERROR: Invalid Genome reference {} from {}".format(ret[0],
                                                                self.old_genome_ref))

    @log
    def test_get_assembly(self):
        inputs = {'ref': self.new_genome_ref}
        ret = self.impl.get_assembly(self.ctx, inputs)
        self.assertTrue(self.getType(ret[0]).startswith("KBaseGenomeAnnotations.Assembly"),
                        "ERROR: Invalid assembly reference {} from {}".format(ret[0], self.new_genome_ref))

    @log
    def test_get_assembly_old(self):
        inputs = {'ref': self.new_genome_ref}
        ret = self.impl.get_assembly(self.ctx, inputs)
        self.assertTrue(
            self.getType(ret[0]).startswith("KBaseGenomeAnnotations.Assembly"),
            "ERROR: Invalid assembly reference {} from {}".format(ret[0],
                                                                   self.old_genome_ref))

    @log
    def test_get_feature_types(self):
        with self.assertRaises(NotImplementedError):
            inputs = {'ref': self.new_genome_ref}
            ret = self.impl.get_feature_types(self.ctx, inputs)

    @log
    def test_get_feature_type_descriptions_all_old(self):
        with self.assertRaises(NotImplementedError):
            inputs = {'ref': self.new_genome_ref}
            ret = self.impl.get_feature_type_descriptions(self.ctx, inputs)

    @log
    def test_get_feature_type_counts_all(self):
        with self.assertRaises(NotImplementedError):
            inputs = {'ref': self.new_genome_ref}
            ret = self.impl.get_feature_type_counts(self.ctx, inputs)

    @log
    def test_get_feature_ids_all(self):
        inputs = {'ref': self.new_genome_ref}
        ret = self.impl.get_feature_ids(self.ctx, inputs)
        self.assertGreater(len(ret[0]), 0, "ERROR: No feature ids returned for all {}".format(self.new_genome_ref))

    @log
    def test_get_feature_ids_all_old(self):
        inputs = {'ref': self.new_genome_ref}
        ret = self.impl.get_feature_ids(self.ctx, inputs)
        self.assertGreater(len(ret[0]), 0,
                           "ERROR: No feature ids returned for all {}".format(
                               self.old_genome_ref))

    @log
    def test_get_feature_ids_genes_by_function(self):
        inputs = {'ref': self.new_genome_ref,
                  'filters': {'function_list': ["structural component", "enzyme"]},
                  'group_by': 'function'
                  }
        ret = self.impl.get_feature_ids(self.ctx, inputs)[0]
        assert 'by_function' in ret
        self.assertGreater(len(ret['by_function']), 0,
                           "ERROR: No feature ids returned for {}".format(
                               inputs))

    @log
    def test_get_feature_ids_genes_by_function_old(self):
        inputs = {'ref': self.old_genome_ref,
                  'filters': {
                      'function_list': ["SSU ribosomal protein S16p",
                                        "hypothetical protein"]},
                  'group_by': 'function'
                  }
        ret = self.impl.get_feature_ids(self.ctx, inputs)[0]
        assert 'by_function' in ret
        self.assertGreater(len(ret['by_function']), 0,
                           "ERROR: No feature ids returned for {}".format(
                               inputs))
    @log
    def test_get_feature_ids_genes_by_alias(self):
        inputs = {'ref': self.new_genome_ref,
                  'filters': {'alias_list': ["b1018", "b2095"]},
                  'group_by': 'alias'
                  }
        ret = self.impl.get_feature_ids(self.ctx, inputs)[0]
        assert 'by_alias' in ret
        self.assertGreater(len(ret['by_alias']), 0,
                           "ERROR: No feature ids returned for {}".format(
                               inputs))

    @log
    def test_get_feature_ids_genes_by_alias_old(self):
        inputs = {'ref': self.old_genome_ref,
                  'filters': {'alias_list': ["b1018", "b2095"]},
                  'group_by': 'alias'
                  }
        ret = self.impl.get_feature_ids(self.ctx, inputs)[0]
        assert 'by_alias' in ret
        self.assertGreater(len(ret['by_alias']), 0,
                           "ERROR: No feature ids returned for {}".format(
                               inputs))

    @log
    def test_get_feature_ids_by_type(self):
        inputs = {'ref': self.new_genome_ref,
                  'filters': {'type_list': ['gene', 'CDS']},
                  'group_by': 'type'
                  }
        ret = self.impl.get_feature_ids(self.ctx, inputs)[0]
        assert 'by_type' in ret
        self.assertGreater(len(ret['by_type']), 0,
                           "ERROR: No feature ids returned for {}".format(
                               inputs))

    @log
    def test_get_feature_ids_by_type_old(self):
        inputs = {'ref': self.old_genome_ref,
                  'filters': {'type_list': ['gene', 'CDS']},
                  'group_by': 'type'
                  }
        ret = self.impl.get_feature_ids(self.ctx, inputs)[0]
        assert 'by_type' in ret
        self.assertGreater(len(ret['by_type']), 0,
                           "ERROR: No feature ids returned for {}".format(
                               inputs))

    @log
    def test_get_feature_ids_by_region(self):
        inputs = {'ref': self.new_genome_ref,
                  'filters': {'region_list': [{"contig_id": 'NC_000913.3',
                                               "strand": "+", "start": 0,
                                               "length": 5000}]},
                  'group_by': 'region'
                  }
        ret = self.impl.get_feature_ids(self.ctx, inputs)[0]
        assert 'by_region' in ret
        self.assertGreater(len(ret['by_region']), 0,
                           "ERROR: No feature ids returned for {}".format(
                               inputs))

    @log
    def test_get_feature_ids_by_region_old(self):
        inputs = {'ref': self.old_genome_ref,
                  'filters': {'region_list': [{"contig_id": 'NODE_185_length_8164_cov_5.03663_ID_369',
                                               "strand": "+", "start": 0,
                                               "length": 5000}]},
                  'group_by': 'region'
                  }
        ret = self.impl.get_feature_ids(self.ctx, inputs)[0]
        assert 'by_region' in ret
        self.assertGreater(len(ret['by_region']), 0,
                           "ERROR: No feature ids returned for {}".format(
                               inputs))

    @log
    def test_get_features_all(self):
        inputs = {'ref': self.new_genome_ref}
        ret = self.impl.get_features(self.ctx, inputs)[0]
        self.assertGreater(len(ret), 0, "ERROR: No feature data returned for all {}".format(self.new_genome_ref))
        assert 'b0021' in ret
        assert ret['b0021']['feature_dna_sequence']

    @log
    def test_get_features_all_old(self):
        inputs = {'ref': self.old_genome_ref}
        ret = self.impl.get_features(self.ctx, inputs)[0]
        self.assertGreater(len(ret), 0,
                           "ERROR: No feature data returned for all {}".format(
                               inputs))
        assert 'kb|g.220339.CDS.1451' in ret
        assert ret['kb|g.220339.CDS.1451']['feature_dna_sequence']

    @log
    def test_get_features_all_exclude_sequence_true(self):
        inputs = {'ref': self.new_genome_ref, 'exclude_sequence': 1}
        ret = self.impl.get_features(self.ctx, inputs)[0]
        self.assertGreater(len(ret), 0, "ERROR: No feature data returned for all {}".format(self.new_genome_ref))
        assert 'b0021' in ret
        self.assertFalse(ret['b0021']['feature_dna_sequence'])

    @log
    def test_get_features_all_exclude_sequence_true_old(self):
        inputs = {'ref': self.old_genome_ref, 'exclude_sequence': 1}
        ret = self.impl.get_features(self.ctx, inputs)[0]
        self.assertGreater(len(ret), 0,
                           "ERROR: No feature data returned for all {}".format(
                               self.old_genome_ref))
        assert 'kb|g.220339.CDS.1451' in ret
        self.assertFalse(ret['kb|g.220339.CDS.1451']['feature_dna_sequence'])

    @log
    def test_get_proteins_all(self):
        with self.assertRaises(NotImplementedError):
            inputs = {'ref': self.new_genome_ref}
            ret = self.impl.get_proteins(self.ctx, inputs)

    @log
    def test_get_feature_locations_all(self):
        with self.assertRaises(NotImplementedError):
            inputs = {'ref': self.new_genome_ref}
            ret = self.impl.get_feature_locations(self.ctx, inputs)

    @log
    def test_get_feature_publications_all(self):
        with self.assertRaises(NotImplementedError):
            inputs = {'ref': self.new_genome_ref}
            ret = self.impl.get_feature_publications(self.ctx, inputs)

    @log
    def test_get_feature_dna_all(self):
        with self.assertRaises(NotImplementedError):
            inputs = {'ref': self.new_genome_ref}
            ret = self.impl.get_feature_dna(self.ctx, inputs)
            self.assertGreater(len(ret[0].keys()), 0, "ERROR: No DNA sequence for {}".format(self.new_genome_ref))

    @log
    def test_get_feature_functions_all(self):
        with self.assertRaises(NotImplementedError):
            inputs = {'ref': self.new_genome_ref}
            ret = self.impl.get_feature_functions(self.ctx, inputs)

    @log
    def test_get_feature_aliases_all(self):
        with self.assertRaises(NotImplementedError):
            inputs = {'ref': self.new_genome_ref}
            ret = self.impl.get_feature_aliases(self.ctx, inputs)

    @log
    def test_get_cds_by_gene_all(self):
        inputs = {'ref': self.new_genome_ref, 'filters': {'type_list': ['gene']}, 'group_by': 'type'}
        gene_id_list = self.impl.get_feature_ids(self.ctx, inputs)[0]["by_type"]["gene"]
        inputs = {'ref': self.new_genome_ref, 'gene_id_list': gene_id_list}
        ret = self.impl.get_cds_by_gene(self.ctx, inputs)[0]
        assert 'b3834' in ret
        assert ret['b3834'] == ['b3834_CDS_1']

    @log
    def test_get_cds_by_gene_all_old(self):
        inputs = {'ref': self.old_genome_ref,
                  'filters': {'type_list': ['gene']}, 'group_by': 'type'}
        gene_id_list = \
            self.impl.get_feature_ids(self.ctx, inputs)[0]["by_type"]["gene"]
        inputs = {'ref': self.old_genome_ref, 'gene_id_list': gene_id_list}
        ret = self.impl.get_cds_by_gene(self.ctx, inputs)
        self.assertFalse(ret[0])

    @log
    def test_get_mrna_by_gene_all(self):
        with self.assertRaises(NotImplementedError):
            inputs = {'ref': self.new_genome_ref, 'filters': {'type_list': ['gene']}, 'group_by': 'type'}
            gene_id_list = self.impl.get_feature_ids(self.ctx, inputs)[0]["by_type"]["gene"]
            inputs = {'ref': self.new_genome_ref, 'gene_id_list': gene_id_list}
            ret = self.impl.get_mrna_by_gene(self.ctx, inputs)

    @log
    def test_get_summary(self):
        with self.assertRaises(NotImplementedError):
            inputs = {'ref': self.new_genome_ref}
            self.impl.get_summary(self.ctx, inputs)

import configparser
import functools
import json
import logging
import os
import shutil
import sys
import time
import unittest

from GenomeAnnotationAPI.GenomeAnnotationAPIImpl import GenomeAnnotationAPI
from GenomeAnnotationAPI.GenomeAnnotationAPIServer import MethodContext
from GenomeAnnotationAPI.authclient import KBaseAuth as _KBaseAuth
from installed_clients.AssemblyUtilClient import AssemblyUtil
from installed_clients.WorkspaceClient import Workspace

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
        config = configparser.ConfigParser()
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
        test_gbk_file = "/kb/module/test/data/kb_g.399.c.1.gbk"
        temp_gbk_file = "/kb/module/work/tmp/kb_g.399.c.1.gbk"
        shutil.copy(test_gbk_file, temp_gbk_file)
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
        info = cls.impl.save_one_genome_v1(cls.ctx, {
            'workspace': wsName,
            'name': "rhodobacter",
            'data': data,
        })[0]['info']
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
                'type': 'KBaseGenomes.Genome',
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
    def test_get_taxon_new(self):
        inputs = {'ref': self.new_genome_ref}
        ret = self.impl.get_taxon(self.ctx, inputs)[0]
        self.assertEqual(self.getType(ret).split('-')[0], "KBaseGenomeAnnotations.Taxon")

    @log
    def test_get_assembly_old(self):
        inputs = {'ref': self.old_genome_ref}
        ret = self.impl.get_assembly(self.ctx, inputs)[0]
        self.assertEqual(self.getType(ret).split('-')[0], "KBaseGenomes.ContigSet")

    @log
    def test_get_assembly_new(self):
        inputs = {'ref': self.new_genome_ref}
        ret = self.impl.get_assembly(self.ctx, inputs)[0]
        self.assertEqual(self.getType(ret).split('-')[0], "KBaseGenomeAnnotations.Assembly")

    @log
    def test_get_feature_types_old(self):
        inputs = {'ref': self.old_genome_ref}
        ret = self.impl.get_feature_types(self.ctx, inputs)[0]
        self.assertEqual(len(ret), 2)
        self.assertEqual(ret[0], 'CDS')

    @log
    def test_get_feature_type_descriptions_all_old(self):
        inputs = {'ref': self.old_genome_ref}
        ret = self.impl.get_feature_type_descriptions(self.ctx, inputs)[0]
        self.assertEqual(len(list(ret.keys())), 4158)
        self.assertEqual(ret.get('kb|g.220339.CDS.3956'), 'CDS')

    @log
    def test_get_feature_type_counts_all_old(self):
        inputs = {'ref': self.old_genome_ref}
        ret = self.impl.get_feature_type_counts(self.ctx, inputs)[0]
        self.assertEqual(len(list(ret.keys())), 2)
        self.assertEqual(ret.get('rna'), 42)

    @log
    def test_get_feature_types_new(self):
        inputs = {'ref': self.new_genome_ref}
        ret = self.impl.get_feature_types(self.ctx, inputs)[0]
        self.assertEqual(len(ret), 12)
        self.assertEqual(ret[0], 'CDS')

    @log
    def test_get_feature_type_descriptions_all_new(self):
        inputs = {'ref': self.new_genome_ref}
        ret = self.impl.get_feature_type_descriptions(self.ctx, inputs)[0]
        self.assertEqual(len(list(ret.keys())), 5092)
        self.assertEqual(ret.get('b3356'), 'gene')

    @log
    def test_get_feature_type_counts_all_new(self):
        inputs = {'ref': self.new_genome_ref}
        ret = self.impl.get_feature_type_counts(self.ctx, inputs)[0]
        self.assertEqual(len(list(ret.keys())), 12)
        self.assertEqual(ret.get('misc_feature'), 11)

    def test_get_proteins_all_old(self):
        inputs = {'ref': self.old_genome_ref}
        ret = self.impl.get_proteins(self.ctx, inputs)[0]
        self.assertEqual(len(list(ret.keys())), 4116)
        self.assertTrue(ret.get('kb|g.220339.CDS.3956'))

    def test_get_proteins_all_new(self):
        inputs = {'ref': self.new_genome_ref}
        ret = self.impl.get_proteins(self.ctx, inputs)[0]
        self.assertEqual(len(list(ret.keys())), 8638)
        self.assertTrue(ret.get('b3356'))

    @log
    def test_get_feature_locations_all_old(self):
        inputs = {'ref': self.old_genome_ref}
        ret = self.impl.get_feature_locations(self.ctx, inputs)[0]
        self.assertEqual(len(list(ret.keys())), 4158)
        self.assertEqual(ret.get('kb|g.220339.CDS.3956'),
                         [['NODE_18_length_32298_cov_4.8199_ID_35', 11339, '-', 420]])

    @log
    def test_get_feature_locations_all_new(self):
        inputs = {'ref': self.new_genome_ref}
        ret = self.impl.get_feature_locations(self.ctx, inputs)[0]
        self.assertEqual(len(list(ret.keys())), 9411)
        self.assertEqual(ret.get('b3356'), [['NC_000913.3', 3485818, '-', 405]])

    @log
    def test_get_feature_dna_all_old(self):
        inputs = {'ref': self.old_genome_ref}
        ret = self.impl.get_feature_dna(self.ctx, inputs)[0]
        self.assertEqual(len(list(ret.keys())), 4158)
        self.assertTrue(ret.get('kb|g.220339.CDS.3956'))

    @log
    def test_get_feature_dna_all_new(self):
        inputs = {'ref': self.new_genome_ref}
        ret = self.impl.get_feature_dna(self.ctx, inputs)[0]
        self.assertEqual(len(list(ret.keys())), 9411)
        self.assertTrue(ret.get('b3356'))

    @log
    def test_get_feature_aliases_all_old(self):
        inputs = {'ref': self.old_genome_ref}
        ret = self.impl.get_feature_aliases(self.ctx, inputs)[0]
        self.assertEqual(len(list(ret.keys())), 4158)
        self.assertEqual(ret.get('kb|g.220339.CDS.3956'), [''])

    @log
    def test_get_feature_aliases_all_new(self):
        inputs = {'ref': self.new_genome_ref}
        ret = self.impl.get_feature_aliases(self.ctx, inputs)[0]
        self.assertEqual(len(list(ret.keys())), 9411)
        self.assertEqual(ret.get('b3356'), ['EcoGene: EG11182', 'GeneID: 947860',
                                            'gene_synonym: ECK3344; JW3319', 'locus_tag: b3356',
                                            'protein_id: NP_417815.1', 'gene: yhfA'])

    @log
    def test_get_feature_functions_all(self):
        inputs = {'ref': self.old_genome_ref}
        ret = self.impl.get_feature_functions(self.ctx, inputs)[0]
        self.assertEqual(ret['kb|g.220339.CDS.3939'], 'DEAD/DEAH box helicase domain protein')
        self.assertEqual(ret['kb|g.220339.rna.40'],
                         'Small Subunit Ribosomal RNA; ssuRNA; SSU rRNA')
        self.assertEqual(len(list(ret.keys())), 4158)

    @log
    def test_get_feature_functions_part(self):
        inputs = {'ref': self.old_genome_ref,
                  'feature_id_list': ['kb|g.220339.CDS.3939', 'kb|g.220339.rna.40']}
        ret = self.impl.get_feature_functions(self.ctx, inputs)[0]
        self.assertEqual(ret['kb|g.220339.CDS.3939'], 'DEAD/DEAH box helicase domain protein')
        self.assertEqual(ret['kb|g.220339.rna.40'],
                         'Small Subunit Ribosomal RNA; ssuRNA; SSU rRNA')
        self.assertEqual(len(list(ret.keys())), 2)

    @log
    def test_get_feature_functions_new(self):
        inputs = {'ref': self.new_genome_ref}
        ret = self.impl.get_feature_functions(self.ctx, inputs)[0]
        self.assertEqual(ret['b4601'], 'product:stationary phase-induced protein')
        self.assertEqual(ret['b4601_CDS_1'], 'product:stationary phase-induced protein')
        self.assertEqual(len(list(ret.keys())), 9411)

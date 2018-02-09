# standard libraries
import ConfigParser
import functools
import logging
import os
import sys
import time
import unittest
import shutil
import json

import requests
import StringIO

from pprint import pprint

# local imports
from biokbase.workspace.client import Workspace
from GenomeAnnotationAPI.GenomeAnnotationAPIImpl import GenomeAnnotationAPI
from GenomeAnnotationAPI.GenomeAnnotationAPIServer import MethodContext
from DataFileUtil.DataFileUtilClient import DataFileUtil
from GenomeAnnotationAPI.authclient import KBaseAuth as _KBaseAuth
from AssemblyUtil.AssemblyUtilClient import AssemblyUtil
from GenomeAnnotationAPI.GenomeInterfaceV1 import GenomeInterfaceV1

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
        print('Setting up class')
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

        # Second user
        test_cfg_file = '/kb/module/work/test.cfg'
        test_cfg_text = "[test]\n"
        with open(test_cfg_file, "r") as f:
            test_cfg_text += f.read()
        config = ConfigParser.ConfigParser()
        config.readfp(StringIO.StringIO(test_cfg_text))
        test_cfg_dict = dict(config.items("test"))
        if ('test_token2' not in test_cfg_dict):
            raise ValueError("Configuration in <module>/test_local/test.cfg file should " +
                             "include second user credentials ('test_token2')")
        token2 = test_cfg_dict['test_token2']
        user2 = auth_client.get_user(token2)
        cls.ctx2 = MethodContext(None)
        cls.ctx2.update({'token': token2,
                         'user_id': user2,
                         'provenance': [
                            {'service': 'NarrativeService',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                         'authenticated': 1})
        
        # create one WS for all tests
        suffix = int(time.time() * 1000)
        wsName = "test_GenomeAnnotationAPI_" + str(suffix)
        ret = cls.ws.create_workspace({'workspace': wsName})
        cls.wsName = wsName

        # preload with reference data
        with open ('data/rhodobacter.json', 'r') as file:
            data_str=file.read()
        data = json.loads(data_str)
        # save old genome
        info = cls.impl.save_one_genome_v1(cls.ctx, {
               'workspace': wsName,
               'name': "rhodobacter",
               'data': data,
           })[0]['info']
        cls.rhodobacter_ref = str(info[6]) +'/' + str(info[0]) + '/' + str(info[4])
        print('created rhodobacter test genome: ' + cls.rhodobacter_ref)

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
        # save new genome
        save_info = {
            'workspace': wsName,
            'objects': [{
                'type': 'KBaseGenomes.Genome',
                'data': data,
                'name': 'new_ecoli'
            }]
        }
        info = cls.ws.save_objects(save_info)[0]
        cls.new_genome_ref = str(info[6]) + '/' + str(info[0]) + '/' + str(
            info[4])
        print('created new test genome')

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.ws.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def generatePesudoRandomWorkspaceName(self):
        if hasattr(self, 'wsName'):
            return self.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_GenomeAnnotationAPI_" + str(suffix)
        ret = self.ws.create_workspace({'workspace': wsName})
        self.wsName = wsName
        return wsName

    def getRhodobacterRef(self):
        if hasattr(self, 'rhodobacter_ref'):
            return self.rhodobacter_ref

        # create a WS
        wsName = self.generatePesudoRandomWorkspaceName()
        # read in the test Rhodobacter genome
        with open('data/rhodobacter.json', 'r') as file:
            data_str=file.read()
        data = json.loads(data_str)
        data['cdss'] = []  # Support for new Genome type structure
        data['mrnas'] = [] # Support for new Genome type structure
        # save to ws
        result = self.ws.save_objects({
                'workspace':wsName,
                'objects': [{
                    'type':'KBaseGenomes.Genome',
                    'data':data,
                    'name':'rhodobacter'
                }]
            })
        info = result[0]
        self.rhodobacter_ref = str(info[6]) +'/' + str(info[0]) + '/' + str(info[4])
        print('created rhodobacter test genome: ' + self.rhodobacter_ref)
        return self.rhodobacter_ref

    def getType(self, ref=None):
        return self.ws.get_object_info_new({"objects": [{"ref": ref}]})[0][2]

    def _downgraded(self, data):
        self.assertTrue('features' in data)
        self.assertTrue('cdss' not in data)
        self.assertTrue('mrnas' not in data)
        one_feat = data['features'][0]
        self.assertEqual(one_feat['type'], 'gene')
        self.assertEqual(one_feat['function'], 'leader; Amino acid biosynthesi'
                                               's: Threonine; product:thr oper'
                                               'on leader peptide')
        self.assertEqual(one_feat['aliases'][0], 'ECK0001; JW4367')
        self.assertEqual(one_feat['ontology_terms'],
                         {'GO':
                             {'GO:0009088':
                                 {
                                     "evidence": [],
                                     "id": "GO:0009088",
                                     "ontology_ref": "6308/3/2",
                                     "term_lineage": [],
                                     "term_name": "threonine biosynthetic process"
                                 }}})
        two_feat = data['features'][-1]
        self.assertEqual(two_feat['type'], 'gene')
        self.assertEqual(two_feat['aliases'][0], 'b4370')

    @log
    def test_genome_downgrade(self):
        data = json.load(open('data/new_ecoli_genome.json'))
        down_data = GenomeInterfaceV1.downgrade_genome(data)
        self._downgraded(down_data)

    def test_bad_get_genome_input(self):
        with self.assertRaisesRegexp(ValueError, 'must be a boolean'):
            ret = self.impl.get_genome_v1(self.ctx,
                      {
                          'genomes': [{
                              'ref': self.new_genome_ref
                          }],
                          'no_data': 'T'
                      })[0]
        with self.assertRaisesRegexp(ValueError, 'must be a boolean'):
            ret = self.impl.get_genome_v1(self.ctx,
                      {
                          'genomes': [{
                              'ref': self.new_genome_ref
                          }],
                          'ignoreErrors': 'T'
                      })[0]
        with self.assertRaisesRegexp(ValueError, 'must be a boolean'):
            ret = self.impl.get_genome_v1(self.ctx,
                      {
                          'genomes': [{
                              'ref': self.new_genome_ref
                          }],
                          'downgrade': 'T'
                      })[0]
        with self.assertRaisesRegexp(ValueError, 'must be a boolean'):
            ret = self.impl.get_genome_v1(self.ctx,
                      {
                          'genomes': [{
                              'ref': self.new_genome_ref
                          }],
                          'no_metadata': 'T'
                      })[0]

    @log
    def test_get_new_genome_downgrade(self):
        ret = self.impl.get_genome_v1(self.ctx,
          {
              'genomes': [{
                  'ref': self.new_genome_ref
              }]
          })[0]
        # test stuff
        data = ret['genomes'][0]['data']
        self.assertEqual(len(ret['genomes']), 1)
        self._downgraded(data)
        # api saves as old type
        ret = self.impl.save_one_genome_v1(self.ctx, {
               'workspace': self.wsName,
               'name': "test_revert",
               'data': data,
           })[0]
        self.assertTrue(ret)

    @log
    def test_get_new_genome_full(self):
        ret = self.impl.get_genome_v1(self.ctx,
                                      {
                                          'genomes': [{
                                              'ref': self.new_genome_ref
                                          }],
                                          'downgrade': 0
                                      })[0]
        # test stuff
        data = ret['genomes'][0]['data']
        self.assertEqual(len(ret['genomes']), 1)
        self.assertTrue('features' in data)
        feat = data['features'][0]
        self.assertEqual(feat['id'], 'b0001')
        self.assertTrue('db_xrefs' in feat)
        self.assertTrue('functions' in feat)
        self.assertTrue('cdss' in data)
        cds = data['cdss'][0]
        self.assertEqual(cds['id'], 'b0001_CDS_1')
        self.assertTrue('db_xrefs' in cds)
        self.assertTrue('functions' in cds)
        self.assertTrue('inference_data' in cds)
        self.assertItemsEqual(cds["aliases"],
                              [["gene_synonym", "ECK0001; JW4367"],
                              ["gene", "thrL"],
                              ["locus_tag", "b0001"],
                              ["protein_id", "NP_414542.1"]
                               ])
        self.assertTrue('mrnas' in data)
        self.assertEqual(len(data['mrnas']), 0)
        self.assertTrue('non_coding_features' in data)
        self.assertEqual(data['non_coding_features'][0]["id"],
                         "repeat_region_1")
        self.assertTrue('genome_tiers' in data)
        self.assertTrue('ontologies_present' in data)

    @log
    def test_get_new_genome_subset(self):
        ret = self.impl.get_genome_v1(self.ctx,
                  {
                      'genomes': [{
                          'ref': self.new_genome_ref,
                          'feature_array': 'cdss',
                          'included_feature_position_index': [0]
                      }],
                      'included_feature_fields': ['id', 'dna_sequence']
                  })[0]

        data = ret['genomes'][0]['data']
        self.assertEqual(len(ret['genomes']), 1)
        self.assertTrue('features' in data)
        self.assertEqual(len(data['features']), 1)
        self.assertEqual(data['features'][0]['id'], 'b0001_CDS_1')
        self.assertEqual(len(data['features'][0]['dna_sequence']), 66)

    @log
    def test_get_all(self):
        ret = self.impl.get_genome_v1(self.ctx, 
                                      {
                                          'genomes': [{
                                              'ref': self.getRhodobacterRef()
                                          }],
                                          'downgrade': 0
                                      })[0]
        no_down = ret['genomes']
        self.assertEqual(len(no_down),1)
        self.assertEqual(no_down[0]['data']['scientific_name'],'Rhodobacter CACIA 14H1')
        self.assertTrue('features' in no_down[0]['data'])
        ret = self.impl.get_genome_v1(self.ctx,
                                      {
                                          'genomes': [{
                                              'ref': self.getRhodobacterRef()
                                          }],
                                          'downgrade': 1
                                      })[0]
        downgraded = ret['genomes']
        self.assertEqual(len(downgraded), 1)
        self.assertEqual(downgraded[0]['data']['scientific_name'],
                         'Rhodobacter CACIA 14H1')
        self.assertTrue('features' in downgraded[0]['data'])
        self.assertDictEqual(downgraded[0]['data'], no_down[0]['data'],
                             "Downgrading an old genome should not change it")

    @log
    def test_get_feature_id_subdata(self):
        ret = self.impl.get_genome_v1(self.ctx, 
            {
                'genomes': [ {
                    'ref' : self.getRhodobacterRef()
                }],
                'included_feature_fields':['id']
            })[0]
        # test stuff
        data = ret['genomes']
        self.assertEqual(data[0]['data']['features'][0]['id'],'kb|g.220339.CDS.1')
        self.assertEqual(len(data[0]['data']['features']),4158)
        self.assertTrue('scientific_name' not in data[0]['data'])

    @log
    def test_get_feature_id_subdata2(self):
        ret = self.impl.get_genome_v1(self.ctx, 
            {
                'genomes': [ {
                    'ref' : self.getRhodobacterRef(),
                    'included_feature_position_index':[3,8]
                }],
                'included_feature_fields':['id']
            })[0]
        # test stuff
        data = ret['genomes']
        self.assertEqual(data[0]['data']['features'][0]['id'],'kb|g.220339.CDS.4')
        self.assertEqual(data[0]['data']['features'][1]['id'],'kb|g.220339.CDS.9')
        self.assertEqual(len(data[0]['data']['features']),2)

    @log
    def test_get_feature_id_subdata_with_some_fields(self):
        ret = self.impl.get_genome_v1(self.ctx, 
            {
                'genomes': [ {
                    'ref' : self.getRhodobacterRef(),
                    'included_feature_position_index':[3,8]
                }],
                'included_feature_fields':['id','function'],
                'included_fields':['domain','scientific_name']
            })[0]
        # test stuff
        data = ret['genomes']
        self.assertEqual(data[0]['data']['scientific_name'],'Rhodobacter CACIA 14H1')
        self.assertEqual(data[0]['data']['domain'],'Bacteria')
        self.assertEqual(data[0]['data']['features'][0]['function'],'FIG01142552: hypothetical protein')
        self.assertEqual(data[0]['data']['features'][0]['id'],'kb|g.220339.CDS.4')

    @log
    def test_get_with_no_meta(self):
        ret = self.impl.get_genome_v1(self.ctx, 
            {
                'genomes': [ {
                    'ref' : self.getRhodobacterRef(),
                    'included_feature_position_index':[3,8]
                }],
                'included_feature_fields':['id','function'],
                'included_fields':['domain','scientific_name'],
                'no_metadata':1
            })[0]
        # test stuff
        data = ret['genomes']
        self.assertTrue('info' not in data[0])
        self.assertTrue('provenance' not in data[0])


    @log
    def test_get_feature_id_subdata_everything(self):
        ret = self.impl.get_genome_v1(self.ctx, 
            {
                'genomes': [ {
                    'ref' : self.getRhodobacterRef(),
                    'included_feature_position_index':[3,8]
                }],
                'included_feature_fields':[],
                'included_fields':['domain','scientific_name']
            })[0]
        # test stuff
        data = ret['genomes']
        self.assertEqual(data[0]['data']['scientific_name'],'Rhodobacter CACIA 14H1')
        self.assertEqual(data[0]['data']['domain'],'Bacteria')
        self.assertEqual(data[0]['data']['features'][0]['function'],'FIG01142552: hypothetical protein')
        self.assertEqual(data[0]['data']['features'][0]['id'],'kb|g.220339.CDS.4')

    @log
    def test_save_genome(self):
        wsName = self.generatePesudoRandomWorkspaceName()
        with open ('data/rhodobacter_contigs.json', 'r') as f1:
            data_str=f1.read()
        data = json.loads(data_str)
        # save to ws
        self.ws.save_objects({
                'workspace':wsName,
                'objects': [{
                    'type':'KBaseGenomes.ContigSet',
                    'data':data,
                    'name':'rhodobacter_contigs.1'
                }]
            })
        # read in the test Rhodobacter genome
        with open ('data/rhodobacter.json', 'r') as f2:
            data_str=f2.read()
        data = json.loads(data_str)
        data['contigset_ref'] = wsName + '/rhodobacter_contigs.1'
        # Let's test dna sequence repare with help of AssemblySequenceAPI service
        for feat in data['features']:
            if 'dna_sequence' in feat:
                del feat['dna_sequence']
        obj_name = 'test_save_new_genome'
        ret = self.impl.save_one_genome_v1(self.ctx, 
            {
                'workspace':wsName,
                'name':obj_name,
                'data':data,
            })[0]
        self.assertEqual(ret['info'][1], obj_name)
        ret = self.impl.get_genome_v1(self.ctx, {'genomes': [{'ref' : wsName + '/' + obj_name}]})[0]
        data = ret['genomes'][0]['data']
        feature_dna_sum = 0
        for feature in data['features']:
            if 'dna_sequence' in feature:
                feature_dna_sum += len(feature['dna_sequence'])
        print("feature_dna_sum=" + str(feature_dna_sum))
        self.assertTrue(feature_dna_sum > 3000000)

    @log
    def test_handles(self):
        wsName = self.generatePesudoRandomWorkspaceName()
        self.ws.set_permissions({'workspace': wsName, 'new_permission': 'w',
                                 'users': [self.ctx2['user_id']]})
        temp_shock_file = "/kb/module/work/tmp/shock1.txt"
        with open(temp_shock_file, "w") as f1:
            f1.write("Test Shock Handle")
        token1 = self.ctx['token']
        dfu = DataFileUtil(os.environ['SDK_CALLBACK_URL'], token=token1)
        handle1 = dfu.file_to_shock({'file_path': temp_shock_file, 'make_handle': 1})['handle']
        hid1 = handle1['hid']
        genome_name = "Genome.1"
        self.impl.save_one_genome_v1(self.ctx, {
            'workspace': wsName, 'name': genome_name, 'data': {
                'id': "qwerty", 'scientific_name': "Qwerty",
                'domain': "Bacteria", 'genetic_code': 11,
                'genbank_handle_ref': hid1}
            })
        genome = self.impl.get_genome_v1(self.ctx2, {'genomes': [{'ref': wsName + '/' + genome_name}
                                                                 ]})[0]['genomes'][0]['data']
        self.impl.save_one_genome_v1(self.ctx2, {'workspace': wsName, 'name': genome_name,
                                                 'data': genome})[0]
        genome = self.impl.get_genome_v1(self.ctx2, {'genomes': [{'ref': wsName + '/' + genome_name}
                                                                 ]})[0]['genomes'][0]['data']
        self.assertTrue('genbank_handle_ref' in genome)
        hid2 = genome['genbank_handle_ref']
        self.assertNotEqual(hid1, hid2)

    @log
    def test_save_genome_with_close_genome(self):
        wsName = self.generatePesudoRandomWorkspaceName()
        with open('data/rhodobacter_contigs.json', 'r') as f1:
            data_str = f1.read()
        data = json.loads(data_str)
        # save to ws
        self.ws.save_objects({
            'workspace': wsName,
            'objects': [{
                'type': 'KBaseGenomes.ContigSet',
                'data': data,
                'name': 'rhodobacter_contigs.1'
            }]
        })
        # read in the test Rhodobacter genome
        with open('data/rhodobacter_close.json', 'r') as f2:
            data_str = f2.read()
        data = json.loads(data_str)
        data['contigset_ref'] = wsName + '/rhodobacter_contigs.1'
        # Let's test dna sequence repare with help of AssemblySequenceAPI service
        for feat in data['features']:
            if 'dna_sequence' in feat:
                del feat['dna_sequence']
        obj_name = 'test_save_new_rhodo_close'
        ret = self.impl.save_one_genome_v1(self.ctx,
                                           {
                                               'workspace': wsName,
                                               'name': obj_name,
                                               'data': data,
                                           })[0]
        self.assertEqual(ret['info'][1], obj_name)
        ret = self.impl.get_genome_v1(self.ctx, {'genomes': [{'ref': wsName + '/' + obj_name}]})[0]
        data = ret['genomes'][0]['data']
        feature_dna_sum = 0
        for feature in data['features']:
            if 'dna_sequence' in feature:
                feature_dna_sum += len(feature['dna_sequence'])
        print("feature_dna_sum=" + str(feature_dna_sum))
        self.assertTrue(feature_dna_sum > 3000000)

    @log
    def test_save_genome_with_close_genome_error(self):
        wsName = self.generatePesudoRandomWorkspaceName()
        with open('data/rhodobacter_contigs.json', 'r') as f1:
            data_str = f1.read()
        data = json.loads(data_str)
        # save to ws
        self.ws.save_objects({
            'workspace': wsName,
            'objects': [{
                'type': 'KBaseGenomes.ContigSet',
                'data': data,
                'name': 'rhodobacter_contigs.2'
            }]
        })
        # read in the test Rhodobacter genome
        with open('data/rhodobacter_close_nonfloat.json', 'r') as f2:
            data_str = f2.read()
        data = json.loads(data_str)
        data['contigset_ref'] = wsName + '/rhodobacter_contigs.2'
        # Let's test dna sequence repare with help of AssemblySequenceAPI service
        for feat in data['features']:
            if 'dna_sequence' in feat:
                del feat['dna_sequence']
        obj_name = 'test_save_new_rhodo_close_nonfloat'

        error = 'Invalid closeness_measure value "fourHundredAndTwo": float expected'
        with self.assertRaises(TypeError) as context:
            ret = self.impl.save_one_genome_v1(self.ctx,
                                           {
                                               'workspace': wsName,
                                               'name': obj_name,
                                               'data': data,
                                           })[0]
        self.assertEqual(error, str(context.exception.message))
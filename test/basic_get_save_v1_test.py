# standard libraries
import ConfigParser
import functools
import logging
import os
import sys
import time
import unittest

import json

from pprint import pprint

# local imports
from biokbase.workspace.client import Workspace
from GenomeAnnotationAPI.GenomeAnnotationAPIImpl import GenomeAnnotationAPI
from GenomeAnnotationAPI.GenomeAnnotationAPIServer import MethodContext

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
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'provenance': [
                            {'service': 'GenomeAnnotationAPI',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})

        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        cls.cfg = {n[0]: n[1] for n in config.items('GenomeAnnotationAPI')}
        cls.ws = Workspace(cls.cfg['workspace-url'], token=token)
        cls.impl = GenomeAnnotationAPI(cls.cfg)

        # create one WS for all tests
        suffix = int(time.time() * 1000)
        wsName = "test_GenomeAnnotationAPI_" + str(suffix)
        ret = cls.ws.create_workspace({'workspace': wsName})
        cls.wsName = wsName

        # preload with reference data
        with open ('data/rhodobacter.json', 'r') as file:
            data_str=file.read()
        data = json.loads(data_str)
        # save to ws
        result = cls.ws.save_objects({
                'workspace':wsName,
                'objects': [{
                    'type':'KBaseGenomes.Genome',
                    'data':data,
                    'name':'rhodobacter'
                }]
            })
        info = result[0]
        cls.rhodobacter_ref = str(info[6]) +'/' + str(info[0]) + '/' + str(info[4])
        print('created rhodobacter test genome: ' + cls.rhodobacter_ref)



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
        with open ('data/rhodobacter.json', 'r') as file:
            data_str=file.read()
        data = json.loads(data_str)
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

    @log
    def test_get_all(self):
        ret = self.impl.get_genome_v1(self.ctx, 
            {
                'genomes': [ {
                    'ref' : self.getRhodobacterRef()
                }]
            })[0]
        # test stuff
        data = ret['genomes']
        self.assertEqual(len(data),1)
        self.assertEqual(data[0]['data']['scientific_name'],'Rhodobacter CACIA 14H1')

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
    def test_get_feature_id_subdata(self):
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
        # read in the test Rhodobacter genome
        with open ('data/rhodobacter.json', 'r') as file:
            data_str=file.read()
        data = json.loads(data_str)
        obj_name = 'test_save_new_genome'
        ret = self.impl.save_one_genome_v1(self.ctx, 
            {
                'workspace':wsName,
                'name':'test_save_new_genome',
                'data':data,
            })[0]
        self.assertEqual(ret['info'][1], obj_name)



    
import unittest
import os
import json
import time

from os import environ
from ConfigParser import ConfigParser
from pprint import pprint

from biokbase.workspace.client import Workspace as workspaceService
from GenomeAnnotationAPI.GenomeAnnotationAPIImpl import GenomeAnnotationAPI
from GenomeAnnotationAPI.GenomeAnnotationAPIServer import MethodContext


class genome_annotation_apiTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
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
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('GenomeAnnotationAPI'):
            cls.cfg[nameval[0]] = nameval[1]
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL, token=token)
        cls.serviceImpl = GenomeAnnotationAPI(cls.cfg)

        cls.obj_name="ReferenceGenomeAnnotations/kb|g.207118"

        cls.obj_name="ReferenceGenomeAnnotations/kb|g.217864"
        cls.feature='kb|g.207118.CDS.3237'
        cls.feature='kb|g.217864.CDS.11485'
        cls.gene='kb|g.217864.locus.10619'

        cls.obj_name="ReferenceGenomeAnnotations/kb|g.140057"
        cls.feature='kb|g.140057.CDS.2901'
        cls.gene='kb|g.140057.locus.2922'
        cls.mrna='kb|g.140057.mRNA.2840'
        cls.taxon= u'1779/523209/1'
        cls.assembly='1837/56/2'

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_GenomeAnnotationAPI_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def test_your_method(self):
        # Prepare test objects in workspace if needed using 
        # self.getWsClient().save_objects({'workspace': self.getWsName(), 'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
        pass

    def test_get_taxon(self):
        ret = self.getImpl().get_taxon(self.getContext(), self.obj_name)
        self.assertEqual(ret[0],self.taxon)
    #
    # funcdef get_assembly(ObjectReference ref) returns (ObjectReference) authentication required;
    def test_get_assembly(self):
        ret = self.getImpl().get_assembly(self.getContext(), self.obj_name)
        self.assertEqual(ret[0],self.assembly)

    def test_get_feature_types(self):
        ret = self.getImpl().get_feature_types(self.getContext(), self.obj_name)
        print ret
        self.assertEqual(ret[0], [u'gene', u'mRNA', u'CDS'] )
        #ObjectReference ref) returns (list<string>) authentication required;

    def test_get_feature_type_descriptions(self):
        ret = self.getImpl().get_feature_type_descriptions(self.getContext(), self.obj_name,['rna'])
        print ret
        self.assertEqual(ret[0],{'rna': 'Ribonucliec Acid (RNA)'})

    def test_get_feature_type_counts(self):
        ret = self.getImpl().get_feature_type_counts(self.getContext(), self.obj_name,['rna'])
        #print ret
        #self.assertEqual(ret[0],{u'protein': 3533, u'rna': 53, u'CDS': 3533})
        self.assertEqual(ret[0], {u'gene': 5106, u'mRNA': 5106, u'CDS': 4998})

    def test_get_feature_ids(self):
        ret = self.getImpl().get_feature_ids(self.getContext(), self.obj_name,{'type_list':['gene']},None)
        assert 'by_type' in ret[0]

    def test_get_features(self):
        ret = self.getImpl().get_features(self.getContext(),self.obj_name,[self.feature])
        print ret
        assert self.feature in ret[0]

    # funcdef get_proteins(ObjectReference ref) returns (mapping<string, Protein_data> ) authentication required;
    def test_get_proteins(self):
        ret = self.getImpl().get_proteins(self.getContext(),self.obj_name)
        assert self.feature in ret[0]

    # funcdef get_feature_locations(ObjectReference ref,list<string> feature_id_list) returns (mapping<string, list<Region>> ) authentication required;
    def test_get_feature_locations(self):
        ret = self.getImpl().get_feature_locations(self.getContext(),self.obj_name,[self.feature])
        print ret
        assert self.feature in ret[0]

    # funcdef get_feature_publications(ObjectReference ref,
    def test_get_feature_publications(self):
        ret = self.getImpl().get_feature_publications(self.getContext(),self.obj_name,[self.feature])
        print ret
        assert self.feature in ret[0]

    # funcdef get_feature_dna(ObjectReference ref,list<string> feature_id_list) returns (mapping<string,string> ) authentication required;
    def test_get_feature_dna(self):
        ret = self.getImpl().get_feature_dna(self.getContext(),self.obj_name,[self.feature])
        print ret
        assert self.feature in ret[0]

    # funcdef get_feature_functions(ObjectReference ref,list<string> feature_id_list) returns (mapping<string,string> ) authentication required;
    def test_get_feature_functions(self):
        ret = self.getImpl().get_feature_functions(self.getContext(),self.obj_name,[self.feature])
        print ret
        assert self.feature in ret[0]

    # funcdef get_feature_aliases(ObjectReference ref,list<string> feature_id_list) returns (mapping<string,list<string>> ) authentication required;
    def test_get_feature_aliases(self):
        ret = self.getImpl().get_feature_aliases(self.getContext(),self.obj_name,[self.feature])
        print ret
        assert self.feature in ret[0]

    # funcdef get_cds_by_gene(ObjectReference ref,
    def test_get_cds_by_gene(self):
        ret = self.getImpl().get_cds_by_gene(self.getContext(),self.obj_name,[self.gene])
        print ret
        assert self.gene in ret[0]

    # funcdef get_cds_by_mrna(ObjectReference ref,
    def test_get_cds_by_mrna(self):
        #t='CDS'
        #x=self.getImpl().get_feature_ids(self.getContext(), self.obj_name,{'type_list':[t]},None)
        #print x
        #list=x[0]['by_type'][t]
        #ret = self.getImpl().get_gene_by_cds(self.getContext(),self.obj_name,list)
        #for i in ret[0]:
        #    if ret[0][i] is not None:
        #      print "......  "+i+":"+ret[0][i]
        #      assert False
        #      break


        ret = self.getImpl().get_cds_by_mrna(self.getContext(),self.obj_name,[self.mrna])
        print ret
        assert self.mrna in ret[0]

    # funcdef get_gene_by_cds(ObjectReference ref,
    def test_get_gene_by_cds(self):
        #x=self.getImpl().get_feature_ids(self.getContext(), self.obj_name,{'type_list':['CDS']},None)
        #cds=x[0]['by_type']['CDS']
        ret = self.getImpl().get_gene_by_cds(self.getContext(),self.obj_name,[self.feature])
        #for i in ret[0]:
        #    if ret[0][i] is not None:
        #      print i+":"+ret[0][i]
        #      break
        assert self.feature in ret[0]
        assert ret[0][self.feature] is not None

    # funcdef get_gene_by_mrna(ObjectReference ref,
    def test_0get_gene_by_mrna(self):
        ret = self.getImpl().get_gene_by_mrna(self.getContext(),self.obj_name,[self.mrna])
        print ret
        assert self.mrna in ret[0]

    # funcdef get_mrna_by_cds(ObjectReference ref,
    def test_get_mrna_by_cds(self):
        ret = self.getImpl().get_gene_by_cds(self.getContext(),self.obj_name,[self.feature])
        print ret
        assert self.feature in ret[0]

    # funcdef get_mrna_by_gene(ObjectReference ref,list<string> gene_id_list) returns (mapping<string, list<string>> ) authentication required;
    def test_get_mrna_by_gene(self):
        ret = self.getImpl().get_mrna_by_gene(self.getContext(),self.obj_name,[self.gene])
        print ret
        assert self.gene in ret[0]

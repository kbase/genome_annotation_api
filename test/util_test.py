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
from GenomeAnnotationAPI.GenomeAnnotationAPIImpl import GenomeAnnotationAPI
from GenomeAnnotationAPI.GenomeAnnotationAPIServer import MethodContext
from GenomeAnnotationAPI.authclient import KBaseAuth as _KBaseAuth
from GenomeAnnotationAPI.GenomeAnnotationUtil import GenomeAnnotationUtil

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
        cls.feat_1 = {
            "function": "hypothetical protein",
            "subsystems": [],
            "atomic_regulons": [],
            "coexpressed_fids": [],
            "co_occurring_fids": [],
            "regulon_data": [],
            "protein_families": [],
            "publications": [],
            "id": "kb|g.220339.CDS.1",
            "location": [
                [
                    "NODE_48_length_21448_cov_4.91263_ID_95",
                    25,
                    "+",
                    330
                ]
            ],
            "subsystem_data": [],
            "dna_sequence_length": 0,
            "orthologs": [],
            "protein_translation_length": 109,
            "aliases": ["kb|g.220339"],
            "type": "CDS",
            "md5": "58b2ba01b9ea4cad48af20eddd39904d"
        }
        cls.feat_2 = {
          "dna_sequence_length": 105,
          "note": "RIP1 (repetitive extragenic palindromic) element; contains 2 REP sequences and 1 IHF site",
          "location": [
            [
              "NC_000913.3",
              5565,
              "+",
              105
            ]
          ],
          "dna_sequence": "GCCTGATGCGACGCTGGCGCGTCTTATCAGGCCTACGTTAATTCTGCAATATATTGAATCTGCATGCTTTTGTAGGCAGGATAAGGCGTTCACGCCGCATCCGGC",
          "type": "repeat_region",
          "id": "repeat_region_1",
          "md5": "b95bfb2d7248be83a1cd1f7845b379a2",
          "aliases": [
                [
                    "locus_tag",
                    "b4402"
                ],
            ]
        }

    def _make_feature_list(self):
        genome = {'features': [self.feat_1], 'non_codeing_features': [self.feat_2]}
        features = GenomeAnnotationUtil._make_feature_list(genome,
                                                           ['functions',
                                                            'type', 'aliases'])
        self.assertEqual(len(features), 2)
        self.assertEqual(features[0]['functions'], ["hypothetical protein"])
        self.assertEqual(features[0]['type'], ["CDS"])
        assert 'md5' not in features[0]
        self.assertEqual(features[1]['aliases'], ["b4402"])
        self.assertEqual(features[1]['type'], ["repeat_region"])
        assert 'id' not in features[1]


    def test_is_feature_in_regions(self):
        region_list = [{"contig_id": 'NC_000913.3', "strand": "+", "start": 0,
                        "length": 5000}]
        self.assertFalse(GenomeAnnotationUtil._is_feature_in_regions(
            {"location": [
                [
                    "NODE_48_length_21448_cov_4.91263_ID_95",
                    25,
                    "+",
                    330
                ]
            ]}, region_list))
        self.assertFalse(GenomeAnnotationUtil._is_feature_in_regions(
            {"location": [
                [
                    "NC_000913.3",
                    400,
                    "-",
                    330
                ]
            ]}, region_list))
        self.assertFalse(GenomeAnnotationUtil._is_feature_in_regions(
            {"location": [
                [
                    "NC_000913.3",
                    5001,
                    "+",
                    330
                ]
            ]}, region_list))
        self.assertTrue(GenomeAnnotationUtil._is_feature_in_regions(
            {"location": [
                [
                    "NC_000913.3",
                    25,
                    "+",
                    330
                ]
            ]}, region_list))

    def test_fill_out_feature(self):
        out_feat = GenomeAnnotationUtil._fill_out_feature(self.feat_1)
        self.assertEqual(out_feat['feature_id'], 'kb|g.220339.CDS.1')
        self.assertEqual(out_feat['feature_type'], 'CDS')
        self.assertEqual(out_feat['feature_function'], 'hypothetical protein')
        self.assertEqual(out_feat['feature_locations'], [
            {"contig_id": 'NODE_48_length_21448_cov_4.91263_ID_95',
             "strand": "+", "start": 25, "length": 330}])
        self.assertEqual(out_feat['feature_dna_sequence'], '')
        self.assertEqual(out_feat['feature_dna_sequence_length'], 0)
        self.assertEqual(out_feat['feature_aliases'], {"kb|g.220339": []})

        out_feat = GenomeAnnotationUtil._fill_out_feature(self.feat_2)
        self.assertEqual(out_feat['feature_id'], 'repeat_region_1')
        self.assertEqual(out_feat['feature_type'], 'repeat_region')
        self.assertEqual(out_feat['feature_function'], '')
        self.assertEqual(out_feat['feature_locations'], [
            {"contig_id": 'NC_000913.3', "strand": "+", "start": 5565,
             "length": 105}])
        self.assertTrue(out_feat['feature_dna_sequence'])
        self.assertTrue(out_feat['feature_notes'])
        self.assertEqual(out_feat['feature_dna_sequence_length'], 105)
        self.assertEqual(out_feat['feature_md5'], 'b95bfb2d7248be83a1cd1f7845b379a2')
        self.assertEqual(out_feat['feature_aliases'], {'locus_tag:b4402': []})

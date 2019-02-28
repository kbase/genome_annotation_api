import logging
from collections import Counter


class Utils:
    def __init__(self, workspace_client):
        self.ws = workspace_client

    @staticmethod
    def validate_params(params, expected, opt_param=set()):
        """Validates that required parameters are present. Warns if unexpected parameters appear"""
        expected = set(expected)
        opt_param = set(opt_param)
        pkeys = set(params)
        if expected - pkeys:
            raise ValueError(
                f"Required keys {', '.join(expected - pkeys)} not in supplied parameters")
        defined_param = expected | opt_param
        for param in params:
            if param not in defined_param:
                logging.warning("Unexpected parameter {} supplied".format(param))

    def _get_field_from_ws(self, params, key):
        self.validate_params(params, {'ref', }, {'feature_id_list', })
        if params.get('feature_id_list'):
            feature_id_list = set(params['feature_id_list'])
        else:
            feature_id_list = False
        feature_fields = ['features', 'mrnas', 'cdss', 'non_coding_features']
        ws_fields = [x + "/[*]/id" for x in feature_fields]
        ws_fields += ["{}/[*]/{}".format(x, key) for x in feature_fields]
        genome = self.ws.get_objects2(
            {'objects': [{'ref': params['ref'], 'included': ws_fields}]}
        )['data'][0]['data']
        return {feature['id']: feature[key]
                for field in feature_fields
                for feature in genome.get(field, [])
                if key in feature and
                (not feature_id_list or feature['id'] in feature_id_list)}

    def get_assembly(self, params):
        self.validate_params(params, {'ref', })
        objreq = {'objects': [{'ref': params['ref'],
                               'included': ['assembly_ref', 'contigset_ref']}]}
        ref = self.ws.get_objects2(objreq)['data'][0]['data']
        if 'assembly_ref' in ref:
            return ref['assembly_ref']
        if 'contigset_ref' in ref:
            return ref['contigset_ref']

    def get_taxon(self, params):
        self.validate_params(params, {'ref', })
        objreq = {'objects': [{'ref': params['ref'], 'included': ['taxon_ref']}]}
        return self.ws.get_objects2(objreq)['data'][0]['data'].get('taxon_ref')

    def get_feature_functions(self, params):
        functions = {}
        self.validate_params(params, {'ref', }, {'feature_id_list', })
        if params.get('feature_id_list'):
            feature_id_list = set(params['feature_id_list'])
        else:
            feature_id_list = False
        feature_fields = ['features', 'mrnas', 'cdss', 'non_coding_features']
        ws_fields = [x + "/[*]/id" for x in feature_fields]
        ws_fields += [x + "/[*]/function" for x in feature_fields]
        ws_fields += [x + "/[*]/functions" for x in feature_fields]
        genome = self.ws.get_objects2(
            {'objects': [{'ref': params['ref'], 'included': ws_fields}]}
                                      )['data'][0]['data']
        for field in feature_fields:
            for feature in genome.get(field, []):
                func = feature.get('function', '')
                func += ", ".join(feature.get('functions', []))
                if not feature_id_list or feature['id'] in feature_id_list:
                    functions[feature['id']] = func
        return functions

    def get_feature_aliases(self, params):
        aliases = {}
        self.validate_params(params, {'ref', }, {'feature_id_list', })
        if params.get('feature_id_list'):
            feature_id_list = set(params['feature_id_list'])
        else:
            feature_id_list = False
        feature_fields = ['features', 'mrnas', 'cdss', 'non_coding_features']
        ws_fields = [x + "/[*]/id" for x in feature_fields]
        ws_fields += [x + "/[*]/aliases" for x in feature_fields]
        ws_fields += [x + "/[*]/db_xrefs" for x in feature_fields]
        genome = self.ws.get_objects2(
            {'objects': [{'ref': params['ref'], 'included': ws_fields}]}
                                      )['data'][0]['data']
        for field in feature_fields:
            for feature in genome.get(field, []):
                a = [": ".join(x) for x in feature.get('db_xrefs', [[]])]
                if feature.get('aliases'):
                    if isinstance(feature['aliases'][0], list):
                        a += [": ".join(x) for x in feature['aliases']]
                    else:
                        a += feature['aliases']
                if not feature_id_list or feature['id'] in feature_id_list:
                    aliases[feature['id']] = a
        return aliases

    def get_feature_type_descriptions(self, params):
        self.validate_params(params, {'ref', }, {'feature_id_list', })
        if params.get('feature_id_list'):
            feature_id_list = set(params['feature_id_list'])
        else:
            feature_id_list = False
        feature_fields = {'features': 'gene', 'mrnas': 'mRNA', 'cdss': 'CDS',
                          'non_coding_features': 'non_coding_feature'}
        ws_fields = [x + "/[*]/id" for x in feature_fields]
        ws_fields += [x + "/[*]/type" for x in feature_fields]
        genome = self.ws.get_objects2(
            {'objects': [{'ref': params['ref'], 'included': ws_fields}]}
                                      )['data'][0]['data']

        return {feature['id']: feature.get('type', default_type)
                for field, default_type in feature_fields.items()
                for feature in genome.get(field, [])
                if 'type' in feature and
                (not feature_id_list or feature['id'] in feature_id_list)}

    def get_feature_type_counts(self, params):
        genome = self.ws.get_objects2(
            {'objects': [{'ref': params['ref'], 'included': ['feature_counts']}]}
        )['data'][0]['data']
        if 'feature_counts' in genome and not params.get('feature_id_list'):
            return genome['feature_counts']
        else:
            return Counter(self.get_feature_type_descriptions(params).values())

    def get_feature_types(self, params):
        return sorted(set(self.get_feature_type_counts(params).keys()))

    def get_feature_locations(self, params):
        return self._get_field_from_ws(params, 'location')

    def get_feature_dna_sequences(self, params):
        return self._get_field_from_ws(params, 'dna_sequence')

    def get_feature_proteins(self, params):
        return self._get_field_from_ws(params, 'protein_translation')


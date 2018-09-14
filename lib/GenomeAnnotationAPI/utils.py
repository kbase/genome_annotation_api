import logging


class Utils:
    def __init__(self, workspace_client, services):
        self.ws = workspace_client
        self.handle_url = services['handle_service_url']
        self.shock_url = services['shock_service_url']
        self.sw_url = services['service_wizard_url']

    @staticmethod
    def validate_params(params, expected, opt_param=set()):
        """Validates that required parameters are present. Warns if unexpected parameters appear"""
        expected = set(expected)
        opt_param = set(opt_param)
        pkeys = set(params)
        if expected - pkeys:
            raise ValueError("Required keys {} not in supplied parameters"
                             .format(", ".join(expected - pkeys)))
        defined_param = expected | opt_param
        for param in params:
            if param not in defined_param:
                logging.warning("Unexpected parameter {} supplied".format(param))

    def get_assembly(self, params):
        self.validate_params(params, {'ref', })
        objreq = {'objects': [{'ref': params['ref'],
                               'included': ['assembly_ref', 'contigset_ref']}]}
        ref = self.ws.get_objects2(objreq)['data'][0]['data']
        if 'assembly_ref' in ref:
            return ref['assembly_ref']
        if 'contigset_ref' in ref:
            return ref['contigset_ref']
        return None

    def get_feature_functions(self, params):
        functions = {}
        self.validate_params(params, {'ref', }, {'feature_id_list', })
        feature_id_list = set(params.get('feature_id_list', []))
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

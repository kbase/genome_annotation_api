

from biokbase.workspace.client import Workspace


from pprint import pprint

class GenomeInterfaceV1:


    def __init__(self, workspace_client):
        self.ws = workspace_client;


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

        getObjParams = { 'objects':object_specifications }

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

        self.validate_proper_ws_type(object_specifications, getObjParams['ignoreErrors'], 'KBaseGenomes.Genome')
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

        provenance = None
        if 'provenance' in params:
            provenance = params['provenance']
        elif 'provenance' in ctx:
            provenance = ctx['provenance']

        hidden = 0
        if 'hidden' in params:
            if params['hidden']==0:
                hidden=0
            elif params['hidden']==1:
                hidden=1
            else:
                raise ValueError('hidden parameter must be set to 0 or 1; it was: '+str(hidden))

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

        return { 'info':results[0] }








# -*- coding: utf-8 -*-
#BEGIN_HEADER
from doekbase.data_api.annotation.genome_annotation.api import GenomeAnnotationAPI as GenomeAnnotationAPI_local
from doekbase.data_api import cache
import logging
from biokbase.workspace.client import Workspace
#END_HEADER


class GenomeAnnotationAPI:
    '''
    Module Name:
    GenomeAnnotationAPI

    Module Description:
    A KBase module: GenomeAnnotationAPI
    '''

    ######## WARNING FOR GEVENT USERS #######
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    #########################################
    VERSION = "0.1.1"
    GIT_URL = "https://github.com/rsutormin/genome_annotation_api"
    GIT_COMMIT_HASH = "71e37b2b56471ca768261a32d431f4a6013673ec"
    
    #BEGIN_CLASS_HEADER
    def _migrate_property_internal(self, from_dict, to_dict, prop_name, to_prop_name = None):
        if not to_prop_name:
            to_prop_name = prop_name
        if to_prop_name not in to_dict and prop_name in from_dict:
            to_dict[to_prop_name] = from_dict[prop_name]
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.logger = logging.getLogger()
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        self.logger.addHandler(log_handler)

        self.services = {
            "workspace_service_url": config['workspace-url'],
            "shock_service_url": config['shock-url'],
            "handle_service_url": config['handle-service-url']
        }

        try:
            cache_dir = config['cache_dir']
        except KeyError:
            cache_dir = None

        try:
            redis_host = config['redis_host']
            redis_port = config['redis_port']
        except KeyError:
            redis_host = None
            redis_port = None

        if redis_host is not None and redis_port is not None:
            self.logger.info("Activating REDIS at host:{} port:{}".format(redis_host, redis_port))
            cache.ObjectCache.cache_class = cache.RedisCache
            cache.ObjectCache.cache_params = {'redis_host': redis_host, 'redis_port': redis_port}
        elif cache_dir is not None:
            self.logger.info("Activating File")
            cache.ObjectCache.cache_class = cache.DBMCache
            cache.ObjectCache.cache_params = {'path':cache_dir,'name':'data_api'}
        else:
            self.logger.info("Not activating REDIS")

        #END_CONSTRUCTOR
        pass
    

    def get_taxon(self, ctx, inputs_get_taxon):
        """
        :param inputs_get_taxon: instance of type "inputs_get_taxon" (* *
           Retrieve the Taxon associated with this GenomeAnnotation. * *
           @return Reference to TaxonAPI object) -> structure: parameter
           "ref" of type "ObjectReference"
        :returns: instance of type "ObjectReference"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_taxon
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], inputs_get_taxon['ref'])
        returnVal = ga.get_taxon(ref_only=True)
        #END get_taxon

        # At some point might do deeper type checking...
        if not isinstance(returnVal, basestring):
            raise ValueError('Method get_taxon return value ' +
                             'returnVal is not type basestring as required.')
        # return the results
        return [returnVal]

    def get_assembly(self, ctx, inputs_get_assembly):
        """
        :param inputs_get_assembly: instance of type "inputs_get_assembly" (*
           * Retrieve the Assembly associated with this GenomeAnnotation. * *
           @return Reference to AssemblyAPI object) -> structure: parameter
           "ref" of type "ObjectReference"
        :returns: instance of type "ObjectReference"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_assembly
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], inputs_get_assembly['ref'])
        returnVal = ga.get_assembly(ref_only=True)
        #END get_assembly

        # At some point might do deeper type checking...
        if not isinstance(returnVal, basestring):
            raise ValueError('Method get_assembly return value ' +
                             'returnVal is not type basestring as required.')
        # return the results
        return [returnVal]

    def get_feature_types(self, ctx, inputs_get_feature_types):
        """
        :param inputs_get_feature_types: instance of type
           "inputs_get_feature_types" (* * Retrieve the list of Feature
           types. * * @return List of feature type identifiers (strings)) ->
           structure: parameter "ref" of type "ObjectReference"
        :returns: instance of list of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_types
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], inputs_get_feature_types['ref'])
        returnVal = ga.get_feature_types()
        #END get_feature_types

        # At some point might do deeper type checking...
        if not isinstance(returnVal, list):
            raise ValueError('Method get_feature_types return value ' +
                             'returnVal is not type list as required.')
        # return the results
        return [returnVal]

    def get_feature_type_descriptions(self, ctx, inputs_get_feature_type_descriptions):
        """
        :param inputs_get_feature_type_descriptions: instance of type
           "inputs_get_feature_type_descriptions" (optional
           feature_type_list) -> structure: parameter "ref" of type
           "ObjectReference", parameter "feature_type_list" of list of String
        :returns: instance of mapping from String to String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_type_descriptions
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], inputs_get_feature_type_descriptions['ref'])

        if 'feature_id_list' in inputs_get_feature_type_descriptions:
            returnVal = ga.get_feature_type_descriptions(inputs_get_feature_type_descriptions['feature_id_list'])
        else:
            returnVal = ga.get_feature_type_descriptions()
        #END get_feature_type_descriptions

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_type_descriptions return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_feature_type_counts(self, ctx, inputs_get_feature_type_counts):
        """
        :param inputs_get_feature_type_counts: instance of type
           "inputs_get_feature_type_counts" (@optional feature_type_list) ->
           structure: parameter "ref" of type "ObjectReference", parameter
           "feature_type_list" of list of String
        :returns: instance of mapping from String to Long
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_type_counts
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], inputs_get_feature_type_counts['ref'])

        if 'feature_type_list' in inputs_get_feature_type_counts:
            returnVal = ga.get_feature_type_counts(inputs_get_feature_type_counts['feature_type_list'])
        else:
            returnVal = ga.get_feature_type_counts()
        #END get_feature_type_counts

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_type_counts return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_feature_ids(self, ctx, inputs_get_feature_ids):
        """
        :param inputs_get_feature_ids: instance of type
           "inputs_get_feature_ids" (@optional filters group_by) ->
           structure: parameter "ref" of type "ObjectReference", parameter
           "filters" of type "Feature_id_filters" (* * Filters passed to
           :meth:`get_feature_ids` * @optional type_list region_list
           function_list alias_list) -> structure: parameter "type_list" of
           list of String, parameter "region_list" of list of type "Region"
           -> structure: parameter "contig_id" of String, parameter "strand"
           of String, parameter "start" of Long, parameter "length" of Long,
           parameter "function_list" of list of String, parameter
           "alias_list" of list of String, parameter "group_by" of String
        :returns: instance of type "Feature_id_mapping" (@optional by_type
           by_region by_function by_alias) -> structure: parameter "by_type"
           of mapping from String to list of String, parameter "by_region" of
           mapping from String to mapping from String to mapping from String
           to list of String, parameter "by_function" of mapping from String
           to list of String, parameter "by_alias" of mapping from String to
           list of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_ids
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], inputs_get_feature_ids['ref'])

        if 'group_type' in inputs_get_feature_ids:
            if 'filters' in inputs_get_feature_ids:
                returnVal = ga.get_feature_ids(inputs_get_feature_ids['filters'],
                                               inputs_get_feature_ids['group_by'])
            else:
                returnVal = ga.get_feature_ids(group_by=inputs_get_feature_ids['group_by'])
        else:
            if 'filters' in inputs_get_feature_ids:
                returnVal = ga.get_feature_ids(inputs_get_feature_ids['filters'])
            else:
                returnVal = ga.get_feature_ids()
        #END get_feature_ids

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_ids return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_features(self, ctx, inputs_get_features):
        """
        :param inputs_get_features: instance of type "inputs_get_features"
           (@optional feature_id_list exclude_sequence) -> structure:
           parameter "ref" of type "ObjectReference", parameter
           "feature_id_list" of list of String, parameter "exclude_sequence"
           of type "boolean" (A boolean - 0 for false, 1 for true. @range (0,
           1))
        :returns: instance of mapping from String to type "Feature_data" ->
           structure: parameter "feature_id" of String, parameter
           "feature_type" of String, parameter "feature_function" of String,
           parameter "feature_aliases" of mapping from String to list of
           String, parameter "feature_dna_sequence_length" of Long, parameter
           "feature_dna_sequence" of String, parameter "feature_md5" of
           String, parameter "feature_locations" of list of type "Region" ->
           structure: parameter "contig_id" of String, parameter "strand" of
           String, parameter "start" of Long, parameter "length" of Long,
           parameter "feature_publications" of list of String, parameter
           "feature_quality_warnings" of list of String, parameter
           "feature_quality_score" of list of String, parameter
           "feature_notes" of String, parameter "feature_inference" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_features
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], inputs_get_features['ref'])

        if 'exclude_sequence' in inputs_get_features:
            exclude_sequence = inputs_get_features['exclude_sequence'] == 1
        else:
            exclude_sequence = False

        if 'feature_id_list' in inputs_get_features:
            returnVal = ga.get_features(inputs_get_features['feature_id_list'], exclude_sequence)
        else:
            returnVal = ga.get_features(exclude_sequence=exclude_sequence)
        #END get_features

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_features return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_features2(self, ctx, params):
        """
        Retrieve Feature data, v2.
        @param feature_id_list List of Features to retrieve.
          If None, returns all Feature data.
        @return Mapping from Feature IDs to dicts of available data.
        :param params: instance of type "GetFeatures2Params"
           (exclude_sequence = set to 1 (true) or 0 (false) to indicate if
           sequences should be included.  Defautl is false.) -> structure:
           parameter "ref" of type "ObjectReference", parameter
           "feature_id_list" of list of String, parameter "exclude_sequence"
           of type "boolean" (A boolean - 0 for false, 1 for true. @range (0,
           1))
        :returns: instance of mapping from String to type "Feature_data" ->
           structure: parameter "feature_id" of String, parameter
           "feature_type" of String, parameter "feature_function" of String,
           parameter "feature_aliases" of mapping from String to list of
           String, parameter "feature_dna_sequence_length" of Long, parameter
           "feature_dna_sequence" of String, parameter "feature_md5" of
           String, parameter "feature_locations" of list of type "Region" ->
           structure: parameter "contig_id" of String, parameter "strand" of
           String, parameter "start" of Long, parameter "length" of Long,
           parameter "feature_publications" of list of String, parameter
           "feature_quality_warnings" of list of String, parameter
           "feature_quality_score" of list of String, parameter
           "feature_notes" of String, parameter "feature_inference" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_features2

        if 'ref' not in params:
          raise ValueError('ref field in parameters object is required')

        feature_id_list = None
        if 'feature_id_list' in params:
          feature_id_list = params['feature_id_list']

        exclude_sequence = False
        if 'exclude_sequence' in params:
          if params['exclude_sequence'] == 1:
            exclude_sequence = True
          elif params['exclude_sequence'] != 0:
            raise ValueError('exclude_sequence field in parameters object must be set to either 1 or 0')

        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], params['ref'])
        returnVal = ga.get_features(
                          feature_id_list=feature_id_list,
                          exclude_sequence=exclude_sequence)

        #END get_features2

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_features2 return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_proteins(self, ctx, inputs_get_proteins):
        """
        :param inputs_get_proteins: instance of type "inputs_get_proteins" (*
           * Retrieve Protein data. * * @return Mapping from protein ID to
           data about the protein.) -> structure: parameter "ref" of type
           "ObjectReference"
        :returns: instance of mapping from String to type "Protein_data" ->
           structure: parameter "protein_id" of String, parameter
           "protein_amino_acid_sequence" of String, parameter
           "protein_function" of String, parameter "protein_aliases" of
           mapping from String to list of String, parameter "protein_md5" of
           String, parameter "protein_domain_locations" of list of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_proteins
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], inputs_get_proteins['ref'])
        returnVal = ga.get_proteins()
        #END get_proteins

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_proteins return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_feature_locations(self, ctx, inputs_get_feature_locations):
        """
        :param inputs_get_feature_locations: instance of type
           "inputs_get_feature_locations" (optional feature_id_list) ->
           structure: parameter "ref" of type "ObjectReference", parameter
           "feature_id_list" of list of String
        :returns: instance of mapping from String to list of type "Region" ->
           structure: parameter "contig_id" of String, parameter "strand" of
           String, parameter "start" of Long, parameter "length" of Long
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_locations
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], inputs_get_feature_locations['ref'])

        if 'feature_id_list' in inputs_get_feature_locations:
            returnVal = ga.get_feature_locations(inputs_get_feature_locations['feature_id_list'])
        else:
            returnVal = ga.get_feature_locations()
        #END get_feature_locations

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_locations return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_feature_publications(self, ctx, inputs_get_feature_publications):
        """
        :param inputs_get_feature_publications: instance of type
           "inputs_get_feature_publications" (optional feature_id_list) ->
           structure: parameter "ref" of type "ObjectReference", parameter
           "feature_id_list" of list of String
        :returns: instance of mapping from String to list of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_publications
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], inputs_get_feature_publications['ref'])

        if 'feature_id_list' in inputs_get_feature_publications:
            returnVal = ga.get_feature_publications(inputs_get_feature_publications['feature_id_list'])
        else:
            returnVal = ga.get_feature_publications()
        #END get_feature_publications

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_publications return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_feature_dna(self, ctx, inputs_get_feature_dna):
        """
        :param inputs_get_feature_dna: instance of type
           "inputs_get_feature_dna" (* * Retrieve Feature DNA sequences. * *
           @param feature_id_list List of Feature IDs for which to retrieve
           sequences. *     If empty, returns data for all features. *
           @return Mapping of Feature IDs to their DNA sequence.) ->
           structure: parameter "ref" of type "ObjectReference", parameter
           "feature_id_list" of list of String
        :returns: instance of mapping from String to String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_dna
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], inputs_get_feature_dna['ref'])

        if 'feature_id_list' in inputs_get_feature_dna:
            returnVal = ga.get_feature_dna(inputs_get_feature_dna['feature_id_list'])
        else:
            returnVal = ga.get_feature_dna()
        #END get_feature_dna

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_dna return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_feature_functions(self, ctx, inputs_get_feature_functions):
        """
        :param inputs_get_feature_functions: instance of type
           "inputs_get_feature_functions" (@optional feature_id_list) ->
           structure: parameter "ref" of type "ObjectReference", parameter
           "feature_id_list" of list of String
        :returns: instance of mapping from String to String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_functions
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], inputs_get_feature_functions['ref'])

        if 'feature_id_list' in inputs_get_feature_functions:
            returnVal = ga.get_feature_functions(inputs_get_feature_functions['feature_id_list'])
        else:
            returnVal = ga.get_feature_functions()
        #END get_feature_functions

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_functions return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_feature_aliases(self, ctx, inputs_get_feature_aliases):
        """
        :param inputs_get_feature_aliases: instance of type
           "inputs_get_feature_aliases" (@optional feature_id_list) ->
           structure: parameter "ref" of type "ObjectReference", parameter
           "feature_id_list" of list of String
        :returns: instance of mapping from String to list of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_aliases
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], inputs_get_feature_aliases['ref'])

        if 'feature_id_list' in inputs_get_feature_aliases:
            returnVal = ga.get_feature_aliases(inputs_get_feature_aliases['feature_id_list'])
        else:
            returnVal = ga.get_feature_aliases()
        #END get_feature_aliases

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_aliases return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_cds_by_gene(self, ctx, inputs_get_cds_by_gene):
        """
        :param inputs_get_cds_by_gene: instance of type
           "inputs_get_cds_by_gene" (* * Retrieves coding sequence Features
           (cds) for given gene Feature IDs. * * @param gene_id_list List of
           gene Feature IDS for which to retrieve CDS. *     If empty,
           returns data for all features. * @return Mapping of gene Feature
           IDs to a list of CDS Feature IDs.) -> structure: parameter "ref"
           of type "ObjectReference", parameter "gene_id_list" of list of
           String
        :returns: instance of mapping from String to list of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_cds_by_gene
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], inputs_get_cds_by_gene['ref'])

        if 'gene_id_list' in inputs_get_cds_by_gene:
            returnVal = ga.get_cds_by_gene(inputs_get_cds_by_gene['gene_id_list'])
        else:
            returnVal = ga.get_cds_by_gene()
        #END get_cds_by_gene

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_cds_by_gene return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_cds_by_mrna(self, ctx, inputs_mrna_id_list):
        """
        :param inputs_mrna_id_list: instance of type "inputs_mrna_id_list"
           (@optional mrna_id_list) -> structure: parameter "ref" of type
           "ObjectReference", parameter "mrna_id_list" of list of String
        :returns: instance of mapping from String to String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_cds_by_mrna
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], inputs_mrna_id_list['ref'])

        if 'mrna_id_list' in inputs_mrna_id_list:
            returnVal = ga.get_cds_by_mrna(inputs_mrna_id_list['mrna_id_list'])
        else:
            returnVal = ga.get_cds_by_mrna()
        #END get_cds_by_mrna

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_cds_by_mrna return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_gene_by_cds(self, ctx, inputs_get_gene_by_cds):
        """
        :param inputs_get_gene_by_cds: instance of type
           "inputs_get_gene_by_cds" (@optional cds_id_list) -> structure:
           parameter "ref" of type "ObjectReference", parameter "cds_id_list"
           of list of String
        :returns: instance of mapping from String to String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_gene_by_cds
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], inputs_get_gene_by_cds['ref'])

        if 'cds_id_list' in inputs_get_gene_by_cds:
            returnVal = ga.get_gene_by_cds(inputs_get_gene_by_cds['cds_id_list'])
        else:
            returnVal = ga.get_gene_by_cds([])
        #END get_gene_by_cds

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_gene_by_cds return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_gene_by_mrna(self, ctx, inputs_get_gene_by_mrna):
        """
        :param inputs_get_gene_by_mrna: instance of type
           "inputs_get_gene_by_mrna" (@optional mrna_id_list) -> structure:
           parameter "ref" of type "ObjectReference", parameter
           "mrna_id_list" of list of String
        :returns: instance of mapping from String to String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_gene_by_mrna
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], inputs_get_gene_by_mrna['ref'])

        if 'mrna_id_list' in inputs_get_gene_by_mrna:
            returnVal = ga.get_gene_by_mrna(inputs_get_gene_by_mrna['mrna_id_list'])
        else:
            returnVal = ga.get_gene_by_mrna([])
        #END get_gene_by_mrna

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_gene_by_mrna return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_mrna_by_cds(self, ctx, inputs_get_mrna_by_cds):
        """
        :param inputs_get_mrna_by_cds: instance of type
           "inputs_get_mrna_by_cds" (@optional cds_id_list) -> structure:
           parameter "ref" of type "ObjectReference", parameter "cds_id_list"
           of list of String
        :returns: instance of mapping from String to String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_mrna_by_cds
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], inputs_get_mrna_by_cds['ref'])

        if 'cds_id_list' in inputs_get_mrna_by_cds:
            returnVal = ga.get_mrna_by_cds(inputs_get_mrna_by_cds['cds_id_list'])
        else:
            returnVal = ga.get_mrna_by_cds()
        #END get_mrna_by_cds

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_mrna_by_cds return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_mrna_by_gene(self, ctx, inputs_get_mrna_by_gene):
        """
        :param inputs_get_mrna_by_gene: instance of type
           "inputs_get_mrna_by_gene" (@optional gene_id_list) -> structure:
           parameter "ref" of type "ObjectReference", parameter
           "gene_id_list" of list of String
        :returns: instance of mapping from String to list of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_mrna_by_gene
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], inputs_get_mrna_by_gene['ref'])

        if 'gene_id_list' in inputs_get_mrna_by_gene:
            returnVal = ga.get_mrna_by_gene(inputs_get_mrna_by_gene['gene_id_list'])
        else:
            returnVal = ga.get_mrna_by_gene()
        #END get_mrna_by_gene

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_mrna_by_gene return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_mrna_exons(self, ctx, inputs_get_mrna_exons):
        """
        :param inputs_get_mrna_exons: instance of type
           "inputs_get_mrna_exons" (@optional mrna_id_list) -> structure:
           parameter "ref" of type "ObjectReference", parameter
           "mrna_id_list" of list of String
        :returns: instance of mapping from String to list of type "Exon_data"
           -> structure: parameter "exon_location" of type "Region" ->
           structure: parameter "contig_id" of String, parameter "strand" of
           String, parameter "start" of Long, parameter "length" of Long,
           parameter "exon_dna_sequence" of String, parameter "exon_ordinal"
           of Long
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_mrna_exons
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], inputs_get_mrna_exons['ref'])

        if 'mrna_id_list' in inputs_get_mrna_exons:
            returnVal = ga.get_mrna_exons(inputs_get_mrna_exons['mrna_id_list'])
        else:
            returnVal = ga.get_mrna_exons()
        #END get_mrna_exons

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_mrna_exons return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_mrna_utrs(self, ctx, inputs_get_mrna_utrs):
        """
        :param inputs_get_mrna_utrs: instance of type "inputs_get_mrna_utrs"
           (@optional mrna_id_list) -> structure: parameter "ref" of type
           "ObjectReference", parameter "mrna_id_list" of list of String
        :returns: instance of mapping from String to mapping from String to
           type "UTR_data" -> structure: parameter "utr_locations" of list of
           type "Region" -> structure: parameter "contig_id" of String,
           parameter "strand" of String, parameter "start" of Long, parameter
           "length" of Long, parameter "utr_dna_sequence" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_mrna_utrs
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], inputs_get_mrna_utrs['ref'])

        if 'mrna_id_list' in inputs_get_mrna_utrs:
            returnVal = ga.get_mrna_utrs(inputs_get_mrna_utrs['mrna_id_list'])
        else:
            returnVal = ga.get_mrna_utrs()
        #END get_mrna_utrs

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_mrna_utrs return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_summary(self, ctx, inputs_get_summary):
        """
        :param inputs_get_summary: instance of type "inputs_get_summary" (* *
           Retrieve a summary representation of this GenomeAnnotation. * *
           @return summary data) -> structure: parameter "ref" of type
           "ObjectReference"
        :returns: instance of type "Summary_data" -> structure: parameter
           "scientific_name" of String, parameter "taxonomy_id" of Long,
           parameter "kingdom" of String, parameter "scientific_lineage" of
           list of String, parameter "genetic_code" of Long, parameter
           "organism_aliases" of list of String, parameter "assembly_source"
           of String, parameter "assembly_source_id" of String, parameter
           "assembly_source_date" of String, parameter "gc_content" of
           Double, parameter "dna_size" of Long, parameter "num_contigs" of
           Long, parameter "contig_ids" of list of String, parameter
           "external_source" of String, parameter "external_source_date" of
           String, parameter "release" of String, parameter
           "original_source_filename" of String, parameter
           "feature_type_counts" of mapping from String to Long
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_summary
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], inputs_get_summary['ref'])
        returnVal = ga.get_summary()
        #END get_summary

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_summary return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def save_summary(self, ctx, inputs_save_summary):
        """
        :param inputs_save_summary: instance of type "inputs_save_summary" (*
           * Retrieve a summary representation of this GenomeAnnotation. * *
           @return (int, Summary_data)) -> structure: parameter "ref" of type
           "ObjectReference"
        :returns: multiple set - (1) instance of Long, (2) instance of type
           "Summary_data" -> structure: parameter "scientific_name" of
           String, parameter "taxonomy_id" of Long, parameter "kingdom" of
           String, parameter "scientific_lineage" of list of String,
           parameter "genetic_code" of Long, parameter "organism_aliases" of
           list of String, parameter "assembly_source" of String, parameter
           "assembly_source_id" of String, parameter "assembly_source_date"
           of String, parameter "gc_content" of Double, parameter "dna_size"
           of Long, parameter "num_contigs" of Long, parameter "contig_ids"
           of list of String, parameter "external_source" of String,
           parameter "external_source_date" of String, parameter "release" of
           String, parameter "original_source_filename" of String, parameter
           "feature_type_counts" of mapping from String to Long
        """
        # ctx is the context object
        # return variables are: return_1, return_2
        #BEGIN save_summary
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], inputs_save_summary['ref'])
        returnVal = ga.save_summary()
        return_1 = returnVal[0]
        return_2 = returnVal[1]
        #END save_summary

        # At some point might do deeper type checking...
        if not isinstance(return_1, int):
            raise ValueError('Method save_summary return value ' +
                             'return_1 is not type int as required.')
        if not isinstance(return_2, dict):
            raise ValueError('Method save_summary return value ' +
                             'return_2 is not type dict as required.')
        # return the results
        return [return_1, return_2]

    def get_combined_data(self, ctx, params):
        """
        Retrieve any part of GenomeAnnotation. Please don't use this method in full mode (with all parts included) in cases
        of large eukaryotic datasets. It may lead to out-of-memory errors.
        :param params: instance of type "GetCombinedDataParams" (* Retrieve
           any part of GenomeAnnotation. * Any of exclude_genes,
           include_mrnas and exclude_cdss flags override values listed in
           include_features_by_type.) -> structure: parameter "ref" of type
           "ObjectReference", parameter "exclude_genes" of type "boolean" (A
           boolean - 0 for false, 1 for true. @range (0, 1)), parameter
           "include_mrnas" of type "boolean" (A boolean - 0 for false, 1 for
           true. @range (0, 1)), parameter "exclude_cdss" of type "boolean"
           (A boolean - 0 for false, 1 for true. @range (0, 1)), parameter
           "include_features_by_type" of list of String, parameter
           "exclude_protein_by_cds_id" of type "boolean" (A boolean - 0 for
           false, 1 for true. @range (0, 1)), parameter
           "include_mrna_ids_by_gene_id" of type "boolean" (A boolean - 0 for
           false, 1 for true. @range (0, 1)), parameter
           "exclude_cds_ids_by_gene_id" of type "boolean" (A boolean - 0 for
           false, 1 for true. @range (0, 1)), parameter
           "include_cds_id_by_mrna_id" of type "boolean" (A boolean - 0 for
           false, 1 for true. @range (0, 1)), parameter
           "include_exons_by_mrna_id" of type "boolean" (A boolean - 0 for
           false, 1 for true. @range (0, 1)), parameter
           "include_utr_by_utr_type_by_mrna_id" of type "boolean" (A boolean
           - 0 for false, 1 for true. @range (0, 1)), parameter
           "exclude_summary" of type "boolean" (A boolean - 0 for false, 1
           for true. @range (0, 1))
        :returns: instance of type "GenomeAnnotation_data" (gene_id is a
           feature id of a gene feature. mrna_id is a feature id of a mrna
           feature. cds_id is a feature id of a cds feature.) -> structure:
           parameter "gene_type" of String, parameter "mrna_type" of String,
           parameter "cds_type" of String, parameter "feature_types" of list
           of String, parameter "feature_by_id_by_type" of mapping from
           String to mapping from String to type "Feature_data" -> structure:
           parameter "feature_id" of String, parameter "feature_type" of
           String, parameter "feature_function" of String, parameter
           "feature_aliases" of mapping from String to list of String,
           parameter "feature_dna_sequence_length" of Long, parameter
           "feature_dna_sequence" of String, parameter "feature_md5" of
           String, parameter "feature_locations" of list of type "Region" ->
           structure: parameter "contig_id" of String, parameter "strand" of
           String, parameter "start" of Long, parameter "length" of Long,
           parameter "feature_publications" of list of String, parameter
           "feature_quality_warnings" of list of String, parameter
           "feature_quality_score" of list of String, parameter
           "feature_notes" of String, parameter "feature_inference" of
           String, parameter "protein_by_cds_id" of mapping from String to
           type "Protein_data" -> structure: parameter "protein_id" of
           String, parameter "protein_amino_acid_sequence" of String,
           parameter "protein_function" of String, parameter
           "protein_aliases" of mapping from String to list of String,
           parameter "protein_md5" of String, parameter
           "protein_domain_locations" of list of String, parameter
           "mrna_ids_by_gene_id" of mapping from String to list of String,
           parameter "cds_ids_by_gene_id" of mapping from String to list of
           String, parameter "cds_id_by_mrna_id" of mapping from String to
           String, parameter "exons_by_mrna_id" of mapping from String to
           list of type "Exon_data" -> structure: parameter "exon_location"
           of type "Region" -> structure: parameter "contig_id" of String,
           parameter "strand" of String, parameter "start" of Long, parameter
           "length" of Long, parameter "exon_dna_sequence" of String,
           parameter "exon_ordinal" of Long, parameter
           "utr_by_utr_type_by_mrna_id" of mapping from String to mapping
           from String to type "UTR_data" -> structure: parameter
           "utr_locations" of list of type "Region" -> structure: parameter
           "contig_id" of String, parameter "strand" of String, parameter
           "start" of Long, parameter "length" of Long, parameter
           "utr_dna_sequence" of String, parameter "summary" of type
           "Summary_data" -> structure: parameter "scientific_name" of
           String, parameter "taxonomy_id" of Long, parameter "kingdom" of
           String, parameter "scientific_lineage" of list of String,
           parameter "genetic_code" of Long, parameter "organism_aliases" of
           list of String, parameter "assembly_source" of String, parameter
           "assembly_source_id" of String, parameter "assembly_source_date"
           of String, parameter "gc_content" of Double, parameter "dna_size"
           of Long, parameter "num_contigs" of Long, parameter "contig_ids"
           of list of String, parameter "external_source" of String,
           parameter "external_source_date" of String, parameter "release" of
           String, parameter "original_source_filename" of String, parameter
           "feature_type_counts" of mapping from String to Long
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_combined_data
        ws = Workspace(self.services['workspace_service_url'], token=ctx['token'])
        input_obj_info = ws.get_object_info_new({'objects': [{'ref': params['ref']}]})[0]
        input_obj_type = input_obj_info[2].split('-')[0]
        is_legacy = input_obj_type == "KBaseGenomes.Genome"
        exclude_genes = 'exclude_genes' in params and params['exclude_genes'] == 1
        include_mrnas = 'include_mrnas' in params and params['include_mrnas'] == 1
        exclude_cdss = 'exclude_cdss' in params and params['exclude_cdss'] == 1
        gene_type = 'gene'
        mrna_type = 'mRNA'
        cds_type = 'CDS'
        load_features_by_type = None
        if 'include_features_by_type' in params:
            load_features_by_type = set(params['include_features_by_type'])
        else:
            load_features_by_type = set([gene_type, cds_type])
        if exclude_genes and gene_type in load_features_by_type:
            load_features_by_type.remove(gene_type)
        if include_mrnas:
            load_features_by_type.add(mrna_type)
        if exclude_cdss and cds_type in load_features_by_type:
            load_features_by_type.remove(cds_type)
        load_protein_by_cds_id = not ('exclude_protein_by_cds_id' in params and params['exclude_protein_by_cds_id'] == 1)
        load_mrna_ids_by_gene_id = 'include_mrna_ids_by_gene_id' in params and params['include_mrna_ids_by_gene_id'] == 1
        load_cds_ids_by_gene_id = not ('exclude_cds_ids_by_gene_id' in params and params['exclude_cds_ids_by_gene_id'] == 1)
        load_cds_id_by_mrna_id = 'include_cds_id_by_mrna_id' in params and params['include_cds_id_by_mrna_id'] == 1
        load_exons_by_mrna_id = 'include_exons_by_mrna_id' in params and params['include_exons_by_mrna_id'] == 1
        load_utr_by_utr_type_by_mrna_id = 'include_utr_by_utr_type_by_mrna_id' in params and params['include_utr_by_utr_type_by_mrna_id'] == 1
        load_summary = not ('exclude_summary' in params and params['exclude_summary'] == 1)
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], params['ref'])
        genome_data = {'gene_type': gene_type, 'mrna_type': mrna_type, 'cds_type': cds_type}
        all_feature_types = ga.get_feature_types()
        genome_data['feature_types'] = all_feature_types
        feature_types_to_load = list(load_features_by_type)
        feature_ids_by_type = ga.get_feature_ids({"type_list": all_feature_types})['by_type']
        feature_ids = []
        for feature_type in feature_types_to_load:
            feature_ids.extend(feature_ids_by_type[feature_type])
        feature_map = None
        if len(feature_ids) > 0:
            feature_map = ga.get_features(feature_ids)
        else:
            feature_map = {}
        feature_by_id_by_type = {}
        for feature_type in feature_types_to_load:
            id_to_feature = {}
            for feature_id in feature_ids_by_type[feature_type]:
                id_to_feature[feature_id] = feature_map[feature_id]
            feature_by_id_by_type[feature_type] = id_to_feature
        genome_data['feature_by_id_by_type'] = feature_by_id_by_type
        if load_protein_by_cds_id:
            genome_data['protein_by_cds_id'] = ga.get_proteins()
        if load_mrna_ids_by_gene_id:
            if is_legacy:
                genome_data['mrna_ids_by_gene_id'] = {}
            else:
                genome_data['mrna_ids_by_gene_id'] = ga.get_mrna_by_gene(feature_ids_by_type[gene_type])
        if load_cds_ids_by_gene_id:
            if is_legacy:
                genome_data['cds_ids_by_gene_id'] = {}
            else:
                genome_data['cds_ids_by_gene_id'] = ga.get_cds_by_gene(feature_ids_by_type[gene_type])
        if load_cds_id_by_mrna_id:
            if is_legacy:
                genome_data['cds_id_by_mrna_id'] = {}
            else:
                genome_data['cds_id_by_mrna_id'] = ga.get_cds_by_mrna()
        if load_exons_by_mrna_id:
            genome_data['exons_by_mrna_id'] = ga.get_mrna_exons()
        if load_utr_by_utr_type_by_mrna_id:
            genome_data['utr_by_utr_type_by_mrna_id'] = ga.get_mrna_utrs()
        if load_summary:
            if is_legacy:
                genome = ws.get_objects2({'objects': [{'ref': params['ref'], 'included': [
                    "/scientific_name", "/tax_id", "/contig_ids", "/dna_size", "/gc_content",
                    "/genetic_code", "/num_contigs", "/source", "/source_id"]}]})['data'][0]['data']
                summary = {}
                self._migrate_property_internal(genome, summary, 'scientific_name')
                self._migrate_property_internal(genome, summary, 'tax_id', 'taxonomy_id')
                self._migrate_property_internal(genome, summary, 'contig_ids')
                self._migrate_property_internal(genome, summary, 'dna_size')
                self._migrate_property_internal(genome, summary, 'gc_content')
                self._migrate_property_internal(genome, summary, 'genetic_code')
                self._migrate_property_internal(genome, summary, 'num_contigs')
                self._migrate_property_internal(genome, summary, 'source', 'assembly_source')
                self._migrate_property_internal(genome, summary, 'source_id', 'assembly_source_id')
                genome_data['summary'] = summary
            else:
                summary = ga.get_summary()
                if 'taxonomy' in summary:
                    taxonomy = summary['taxonomy']
                    self._migrate_property_internal(taxonomy, summary, 'scientific_name')
                    self._migrate_property_internal(taxonomy, summary, 'taxonomy_id')
                    self._migrate_property_internal(taxonomy, summary, 'kingdom')
                    self._migrate_property_internal(taxonomy, summary, 'scientific_lineage')
                    self._migrate_property_internal(taxonomy, summary, 'genetic_code')
                    self._migrate_property_internal(taxonomy, summary, 'organism_aliases')
                    del summary['taxonomy']
                if 'assembly' in summary:
                    assembly = summary['assembly']
                    self._migrate_property_internal(assembly, summary, 'assembly_source')
                    self._migrate_property_internal(assembly, summary, 'assembly_source_id')
                    self._migrate_property_internal(assembly, summary, 'assembly_source_date')
                    self._migrate_property_internal(assembly, summary, 'gc_content')
                    self._migrate_property_internal(assembly, summary, 'dna_size')
                    self._migrate_property_internal(assembly, summary, 'num_contigs')
                    self._migrate_property_internal(assembly, summary, 'contig_ids')
                    del summary['assembly']
                if 'annotation' in summary:
                    annotation = summary['annotation']
                    self._migrate_property_internal(annotation, summary, 'external_source')
                    self._migrate_property_internal(annotation, summary, 'external_source_date')
                    self._migrate_property_internal(annotation, summary, 'release')
                    self._migrate_property_internal(annotation, summary, 'original_source_filename')
                    self._migrate_property_internal(annotation, summary, 'feature_type_counts')
                    del summary['annotation']
                genome_data['summary'] = summary
        returnVal = genome_data
        #END get_combined_data

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_combined_data return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK", 'message': "", 'version': self.VERSION,
                     'git_url': self.GIT_URL, 'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]

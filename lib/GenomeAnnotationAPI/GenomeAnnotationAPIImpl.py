#BEGIN_HEADER
from doekbase.data_api.annotation.genome_annotation.api import GenomeAnnotationAPI as GenomeAnnotationAPI_local
from doekbase.data_api import cache
import logging
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
    VERSION = "0.0.2"
    GIT_URL = "https://github.com/mlhenderson/genome_annotation_api"
    GIT_COMMIT_HASH = "c7377dce18a91153fc47f4ec970f9b7b744bdef8"
    
    #BEGIN_CLASS_HEADER
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
           "protein_function" of String, parameter "protein_aliases" of list
           of String, parameter "protein_md5" of String, parameter
           "protein_domain_locations" of list of String
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

    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK", 'message': "", 'version': self.VERSION,
                     'git_url': self.GIT_URL, 'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]

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
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/mlhenderson/genome_annotation_api"
    GIT_COMMIT_HASH = "2dd7f7597f587370ba0826ad36389737eccf861a"
    
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
    

    def get_taxon(self, ctx, ref):
        """
        Retrieve the Taxon associated with this GenomeAnnotation.
        @return Reference to TaxonAPI object
        :param ref: instance of type "ObjectReference"
        :returns: instance of type "ObjectReference"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_taxon
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], ref)
        returnVal = ga.get_taxon(ref_only=True)
        #END get_taxon

        # At some point might do deeper type checking...
        if not isinstance(returnVal, basestring):
            raise ValueError('Method get_taxon return value ' +
                             'returnVal is not type basestring as required.')
        # return the results
        return [returnVal]

    def get_assembly(self, ctx, ref):
        """
        Retrieve the Assembly associated with this GenomeAnnotation.
        @return Reference to AssemblyAPI object
        :param ref: instance of type "ObjectReference"
        :returns: instance of type "ObjectReference"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_assembly
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], ref)
        returnVal = ga.get_assembly(ref_only=True)
        #END get_assembly

        # At some point might do deeper type checking...
        if not isinstance(returnVal, basestring):
            raise ValueError('Method get_assembly return value ' +
                             'returnVal is not type basestring as required.')
        # return the results
        return [returnVal]

    def get_feature_types(self, ctx, ref):
        """
        Retrieve the list of Feature types.
        @return List of feature type identifiers (strings)
        :param ref: instance of type "ObjectReference"
        :returns: instance of list of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_types
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], ref)
        returnVal = ga.get_feature_types()
        #END get_feature_types

        # At some point might do deeper type checking...
        if not isinstance(returnVal, list):
            raise ValueError('Method get_feature_types return value ' +
                             'returnVal is not type list as required.')
        # return the results
        return [returnVal]

    def get_feature_type_descriptions(self, ctx, ref, feature_type_list):
        """
        Retrieve the descriptions for each Feature type in
        this GenomeAnnotation.
        @param feature_type_list List of Feature types. If this list
         is empty or None,
         the whole mapping will be returned.
        @return Name and description for each requested Feature Type
        :param ref: instance of type "ObjectReference"
        :param feature_type_list: instance of list of String
        :returns: instance of mapping from String to String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_type_descriptions
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], ref)
        returnVal = ga.get_feature_type_descriptions(feature_type_list)
        #END get_feature_type_descriptions

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_type_descriptions return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_feature_type_counts(self, ctx, ref, feature_type_list):
        """
        Retrieve the count of each Feature type.
        @param feature_type_list  List of Feature Types. If empty,
          this will retrieve  counts for all Feature Types.
        :param ref: instance of type "ObjectReference"
        :param feature_type_list: instance of list of String
        :returns: instance of mapping from String to Long
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_type_counts
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], ref)
        returnVal = ga.get_feature_type_counts(feature_type_list)
        #END get_feature_type_counts

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_type_counts return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_feature_ids(self, ctx, ref, filters, group_type):
        """
        Retrieve Feature IDs, optionally filtered by type, region, function, alias.
        @param filters Dictionary of filters that can be applied to contents.
          If this is empty or missing, all Feature IDs will be returned.
        @param group_type How to group results, which is a single string matching one
          of the values for the ``filters`` parameter.
        @return Grouped mapping of features.
        :param ref: instance of type "ObjectReference"
        :param filters: instance of type "Feature_id_filters" (* * Filters
           passed to :meth:`get_feature_ids`) -> structure: parameter
           "type_list" of list of String, parameter "region_list" of list of
           type "Region" -> structure: parameter "contig_id" of String,
           parameter "strand" of String, parameter "start" of Long, parameter
           "length" of Long, parameter "function_list" of list of String,
           parameter "alias_list" of list of String
        :param group_type: instance of String
        :returns: instance of type "Feature_id_mapping" -> structure:
           parameter "by_type" of mapping from String to list of String,
           parameter "by_region" of mapping from String to mapping from
           String to mapping from String to list of String, parameter
           "by_function" of mapping from String to list of String, parameter
           "by_alias" of mapping from String to list of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_ids
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], ref)

        if group_type is None:
            returnVal = ga.get_feature_ids(filters)
        else:
            returnVal = ga.get_feature_ids(filters, group_type)
        #END get_feature_ids

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_ids return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_features(self, ctx, ref, feature_id_list):
        """
        Retrieve Feature data.
        @param feature_id_list List of Features to retrieve.
          If None, returns all Feature data.
        @return Mapping from Feature IDs to dicts of available data.
        :param ref: instance of type "ObjectReference"
        :param feature_id_list: instance of list of String
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
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], ref)
        returnVal = ga.get_features(feature_id_list)
        #END get_features

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_features return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_proteins(self, ctx, ref):
        """
        Retrieve Protein data.
        @return Mapping from protein ID to data about the protein.
        :param ref: instance of type "ObjectReference"
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
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], ref)
        returnVal = ga.get_proteins()
        #END get_proteins

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_proteins return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_feature_locations(self, ctx, ref, feature_id_list):
        """
        Retrieve Feature locations.
        @param feature_id_list List of Feature IDs for which to retrieve locations.
            If empty, returns data for all features.
        @return Mapping from Feature IDs to location information for each.
        :param ref: instance of type "ObjectReference"
        :param feature_id_list: instance of list of String
        :returns: instance of mapping from String to list of type "Region" ->
           structure: parameter "contig_id" of String, parameter "strand" of
           String, parameter "start" of Long, parameter "length" of Long
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_locations
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], ref)
        returnVal = ga.get_feature_locations(feature_id_list)
        #END get_feature_locations

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_locations return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_feature_publications(self, ctx, ref, feature_id_list):
        """
        Retrieve Feature publications.
        @param feature_id_list List of Feature IDs for which to retrieve publications.
            If empty, returns data for all features.
        @return Mapping from Feature IDs to publication info for each.
        :param ref: instance of type "ObjectReference"
        :param feature_id_list: instance of list of String
        :returns: instance of mapping from String to list of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_publications
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], ref)
        returnVal = ga.get_feature_publications(feature_id_list)
        #END get_feature_publications

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_publications return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_feature_dna(self, ctx, ref, feature_id_list):
        """
        Retrieve Feature DNA sequences.
        @param feature_id_list List of Feature IDs for which to retrieve sequences.
            If empty, returns data for all features.
        @return Mapping of Feature IDs to their DNA sequence.
        :param ref: instance of type "ObjectReference"
        :param feature_id_list: instance of list of String
        :returns: instance of mapping from String to String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_dna
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], ref)
        returnVal = ga.get_feature_dna(feature_id_list)
        #END get_feature_dna

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_dna return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_feature_functions(self, ctx, ref, feature_id_list):
        """
        Retrieve Feature functions.
        @param feature_id_list List of Feature IDs for which to retrieve functions.
            If empty, returns data for all features.
        @return Mapping of Feature IDs to their functions.
        :param ref: instance of type "ObjectReference"
        :param feature_id_list: instance of list of String
        :returns: instance of mapping from String to String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_functions
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], ref)
        returnVal = ga.get_feature_functions(feature_id_list)
        #END get_feature_functions

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_functions return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_feature_aliases(self, ctx, ref, feature_id_list):
        """
        Retrieve Feature aliases.
        @param feature_id_list List of Feature IDS for which to retrieve aliases.
            If empty, returns data for all features.
        @return Mapping of Feature IDs to a list of aliases.
        :param ref: instance of type "ObjectReference"
        :param feature_id_list: instance of list of String
        :returns: instance of mapping from String to list of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_aliases
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], ref)
        returnVal = ga.get_feature_aliases(feature_id_list)
        #END get_feature_aliases

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_aliases return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_cds_by_gene(self, ctx, ref, gene_id_list):
        """
        Retrieves coding sequence Features (cds) for given gene Feature IDs.
        @param gene_id_list List of gene Feature IDS for which to retrieve CDS.
            If empty, returns data for all features.
        @return Mapping of gene Feature IDs to a list of CDS Feature IDs.
        :param ref: instance of type "ObjectReference"
        :param gene_id_list: instance of list of String
        :returns: instance of mapping from String to list of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_cds_by_gene
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], ref)

        if not gene_id_list:
            returnVal = ga.get_cds_by_gene([])
        else:
            returnVal = ga.get_cds_by_gene(gene_id_list)
        #END get_cds_by_gene

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_cds_by_gene return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_cds_by_mrna(self, ctx, ref, mrna_id_list):
        """
        Retrieves coding sequence (cds) Feature IDs for given mRNA Feature IDs.
        @param mrna_id_list List of mRNA Feature IDS for which to retrieve CDS.
            If empty, returns data for all features.
        @return Mapping of mRNA Feature IDs to a list of CDS Feature IDs.
        :param ref: instance of type "ObjectReference"
        :param mrna_id_list: instance of list of String
        :returns: instance of mapping from String to String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_cds_by_mrna
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], ref)

        if not mrna_id_list:
            returnVal = ga.get_cds_by_mrna([])
        else:
            returnVal = ga.get_cds_by_mrna(mrna_id_list)
        #END get_cds_by_mrna

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_cds_by_mrna return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_gene_by_cds(self, ctx, ref, cds_id_list):
        """
        Retrieves gene Feature IDs for given coding sequence (cds) Feature IDs.
        @param cds_id_list List of cds Feature IDS for which to retrieve gene IDs.
            If empty, returns all cds/gene mappings.
        @return Mapping of cds Feature IDs to gene Feature IDs.
        :param ref: instance of type "ObjectReference"
        :param cds_id_list: instance of list of String
        :returns: instance of mapping from String to String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_gene_by_cds
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], ref)

        if not cds_id_list:
            returnVal = ga.get_gene_by_cds([])
        else:
            returnVal = ga.get_gene_by_cds(cds_id_list)
        #END get_gene_by_cds

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_gene_by_cds return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_gene_by_mrna(self, ctx, ref, mrna_id_list):
        """
        Retrieves gene Feature IDs for given mRNA Feature IDs.
        @param mrna_id_list List of mRNA Feature IDS for which to retrieve gene IDs.
            If empty, returns all mRNA/gene mappings.
        @return Mapping of mRNA Feature IDs to gene Feature IDs.
        :param ref: instance of type "ObjectReference"
        :param mrna_id_list: instance of list of String
        :returns: instance of mapping from String to String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_gene_by_mrna
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], ref)

        if not mrna_id_list:
            returnVal = ga.get_gene_by_mrna([])
        else:
            returnVal = ga.get_gene_by_mrna(mrna_id_list)
        #END get_gene_by_mrna

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_gene_by_mrna return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_mrna_by_cds(self, ctx, ref, cds_id_list):
        """
        Retrieves mRNA Features for given coding sequences (cds) Feature IDs.
        @param cds_id_list List of cds Feature IDS for which to retrieve mRNA IDs.
            If empty, returns all cds/mRNA mappings.
        @return Mapping of cds Feature IDs to mRNA Feature IDs.
        :param ref: instance of type "ObjectReference"
        :param cds_id_list: instance of list of String
        :returns: instance of mapping from String to String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_mrna_by_cds
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], ref)

        if not cds_id_list:
            returnVal = ga.get_mrna_by_cds([])
        else:
            returnVal = ga.get_mrna_by_cds(cds_id_list)
        #END get_mrna_by_cds

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_mrna_by_cds return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_mrna_by_gene(self, ctx, ref, gene_id_list):
        """
        Retrieve the mRNA IDs for given gene IDs.
        @param gene_id_list List of gene Feature IDS for which to retrieve mRNA IDs.
            If empty, returns all gene/mRNA mappings.
        @return Mapping of gene Feature IDs to a list of mRNA Feature IDs.
        :param ref: instance of type "ObjectReference"
        :param gene_id_list: instance of list of String
        :returns: instance of mapping from String to list of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_mrna_by_gene
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], ref)

        if not gene_id_list:
            returnVal = ga.get_mrna_by_gene([])
        else:
            returnVal = ga.get_mrna_by_gene(gene_id_list)
        #END get_mrna_by_gene

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_mrna_by_gene return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_mrna_exons(self, ctx, ref, mrna_id_list):
        """
        Retrieve Exon information for each mRNA ID.
        @param mrna_id_list List of mRNA Feature IDS for which to retrieve exons.
            If empty, returns data for all exons.
        @return Mapping of mRNA Feature IDs to a list of exons (:js:data:`Exon_data`).
        :param ref: instance of type "ObjectReference"
        :param mrna_id_list: instance of list of String
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
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], ref)
        returnVal = ga.get_mrna_by_exons(mrna_id_list)
        #END get_mrna_exons

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_mrna_exons return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_mrna_utrs(self, ctx, ref, mrna_id_list):
        """
        Retrieve UTR information for each mRNA Feature ID.
         UTRs are calculated between mRNA features and corresponding CDS features.
         The return value for each mRNA can contain either:
            - no UTRs found (empty dict)
            -  5' UTR only
            -  3' UTR only
            -  5' and 3' UTRs
         Note: The Genome data type does not contain interfeature
         relationship information. Calling this method for Genome objects
         will raise a :js:throws:`exc.TypeException`.
        @param feature_id_list List of mRNA Feature IDS for which to retrieve UTRs.
        If empty, returns data for all UTRs.
        @return Mapping of mRNA Feature IDs to a mapping that contains
        both 5' and 3' UTRs::
            { "5'UTR": :js:data:`UTR_data`, "3'UTR": :js:data:`UTR_data` }
        :param ref: instance of type "ObjectReference"
        :param mrna_id_list: instance of list of String
        :returns: instance of mapping from String to mapping from String to
           type "UTR_data" -> structure: parameter "utr_locations" of list of
           type "Region" -> structure: parameter "contig_id" of String,
           parameter "strand" of String, parameter "start" of Long, parameter
           "length" of Long, parameter "utr_dna_sequence" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_mrna_utrs
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], ref)
        returnVal = ga.get_mrna_by_utrs(mrna_id_list)
        #END get_mrna_utrs

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_mrna_utrs return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_summary(self, ctx, ref):
        """
        Retrieve a summary representation of this GenomeAnnotation.
        @return summary data
        :param ref: instance of type "ObjectReference"
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
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], ref)
        returnVal = ga.get_summary()
        #END get_summary

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_summary return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def save_summary(self, ctx, ref):
        """
        Retrieve a summary representation of this GenomeAnnotation.
        @return summary data
        :param ref: instance of type "ObjectReference"
        :returns: instance of Long
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN save_summary
        ga = GenomeAnnotationAPI_local(self.services, ctx['token'], ref)
        returnVal = ga.save_summary()
        #END save_summary

        # At some point might do deeper type checking...
        if not isinstance(returnVal, int):
            raise ValueError('Method save_summary return value ' +
                             'returnVal is not type int as required.')
        # return the results
        return [returnVal]

    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK", 'message': "", 'version': self.VERSION,
                     'git_url': self.GIT_URL, 'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]

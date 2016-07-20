#BEGIN_HEADER
from biokbase.workspace.client import Workspace as workspaceService
import doekbase.data_api.annotation.genome_annotation.api
from doekbase.data_api import cache
import logging
#END_HEADER


class GenomeAnnotationAPI:
    '''
    Module Name:
    GenomeAnnotationAPI

    Module Description:
    
    '''

    ######## WARNING FOR GEVENT USERS #######
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    #########################################
    VERSION = "0.0.1"
    GIT_URL = "git@github.com:scanon/testgenomeannotationapi.git"
    GIT_COMMIT_HASH = "8245ff789c3d6150d7ff4b40d1afd537d522d25d"
    
    #BEGIN_CLASS_HEADER
    workspaceURL = None
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.workspaceURL = config['workspace-url']
        self.shockURL = config['shock-url']
        self.logger = logging.getLogger()
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        self.logger.addHandler(log_handler)


        self.services = {
                "workspace_service_url": self.workspaceURL,
                "shock_service_url": self.shockURL,
            }
        try:
            cache_dir = config['cache_dir']
        except:
            cache_dir = None
        try:
            redis_host = config['redis_host']
            redis_port = config['redis_port']
        except:
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
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_taxon
        genome_annotation_api = doekbase.data_api.annotation.genome_annotation.api.GenomeAnnotationAPI(self.services, ctx['token'], ref)
        returnVal=genome_annotation_api.get_taxon(ref_only=True)
        #END get_taxon

        # At some point might do deeper type checking...
        if not isinstance(returnVal, basestring):
            raise ValueError('Method get_taxon return value ' +
                             'returnVal is not type basestring as required.')
        # return the results
        return [returnVal]

    def get_assembly(self, ctx, ref):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_assembly
        genome_annotation_api = doekbase.data_api.annotation.genome_annotation.api.GenomeAnnotationAPI(self.services, ctx['token'], ref)
        returnVal=genome_annotation_api.get_assembly(ref_only=True)
        #END get_assembly

        # At some point might do deeper type checking...
        if not isinstance(returnVal, basestring):
            raise ValueError('Method get_assembly return value ' +
                             'returnVal is not type basestring as required.')
        # return the results
        return [returnVal]

    def get_feature_types(self, ctx, ref):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_types
        genome_annotation_api = doekbase.data_api.annotation.genome_annotation.api.GenomeAnnotationAPI(self.services, ctx['token'], ref)
        returnVal=genome_annotation_api.get_feature_types()
        #END get_feature_types

        # At some point might do deeper type checking...
        if not isinstance(returnVal, list):
            raise ValueError('Method get_feature_types return value ' +
                             'returnVal is not type list as required.')
        # return the results
        return [returnVal]

    def get_feature_type_descriptions(self, ctx, ref, feature_type_list):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_type_descriptions
        genome_annotation_api = doekbase.data_api.annotation.genome_annotation.api.GenomeAnnotationAPI(self.services, ctx['token'], ref)
        returnVal=genome_annotation_api.get_feature_type_descriptions(feature_type_list)
        #END get_feature_type_descriptions

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_type_descriptions return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_feature_type_counts(self, ctx, ref, feature_type_list):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_type_counts
        genome_annotation_api = doekbase.data_api.annotation.genome_annotation.api.GenomeAnnotationAPI(self.services, ctx['token'], ref)
        returnVal=genome_annotation_api.get_feature_type_counts(feature_type_list)
        #END get_feature_type_counts

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_type_counts return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_feature_ids(self, ctx, ref, filters, group_type):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_ids
        genome_annotation_api = doekbase.data_api.annotation.genome_annotation.api.GenomeAnnotationAPI(self.services, ctx['token'], ref)
        if group_type is None:
            returnVal=genome_annotation_api.get_feature_ids(filters)
        else:
            returnVal=genome_annotation_api.get_feature_ids(filters,group_type)
        #END get_feature_ids

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_ids return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_features(self, ctx, ref, feature_id_list):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_features
        genome_annotation_api = doekbase.data_api.annotation.genome_annotation.api.GenomeAnnotationAPI(self.services, ctx['token'], ref)
        returnVal=genome_annotation_api.get_features(feature_id_list)
        #END get_features

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_features return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_proteins(self, ctx, ref):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_proteins
        genome_annotation_api = doekbase.data_api.annotation.genome_annotation.api.GenomeAnnotationAPI(self.services, ctx['token'], ref)
        returnVal=genome_annotation_api.get_proteins()
        #END get_proteins

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_proteins return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_feature_locations(self, ctx, ref, feature_id_list):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_locations
        genome_annotation_api = doekbase.data_api.annotation.genome_annotation.api.GenomeAnnotationAPI(self.services, ctx['token'], ref)
        returnVal=genome_annotation_api.get_feature_locations(feature_id_list)
        #END get_feature_locations

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_locations return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_feature_publications(self, ctx, ref, feature_id_list):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_publications
        genome_annotation_api = doekbase.data_api.annotation.genome_annotation.api.GenomeAnnotationAPI(self.services, ctx['token'], ref)
        returnVal=genome_annotation_api.get_feature_publications(feature_id_list)
        #END get_feature_publications

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_publications return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_feature_dna(self, ctx, ref, feature_id_list):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_dna
        genome_annotation_api = doekbase.data_api.annotation.genome_annotation.api.GenomeAnnotationAPI(self.services, ctx['token'], ref)
        returnVal=genome_annotation_api.get_feature_dna(feature_id_list)
        #END get_feature_dna

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_dna return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_feature_functions(self, ctx, ref, feature_id_list):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_functions
        genome_annotation_api = doekbase.data_api.annotation.genome_annotation.api.GenomeAnnotationAPI(self.services, ctx['token'], ref)
        returnVal=genome_annotation_api.get_feature_functions(feature_id_list)
        #END get_feature_functions

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_functions return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_feature_aliases(self, ctx, ref, feature_id_list):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_feature_aliases
        genome_annotation_api = doekbase.data_api.annotation.genome_annotation.api.GenomeAnnotationAPI(self.services, ctx['token'], ref)
        returnVal=genome_annotation_api.get_feature_aliases(feature_id_list)
        #END get_feature_aliases

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_aliases return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_cds_by_gene(self, ctx, ref, gene_id_list):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_cds_by_gene
        genome_annotation_api = doekbase.data_api.annotation.genome_annotation.api.GenomeAnnotationAPI(self.services, ctx['token'], ref)
        returnVal=genome_annotation_api.get_cds_by_gene(gene_id_list)
        #END get_cds_by_gene

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_cds_by_gene return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_cds_by_mrna(self, ctx, ref, mrna_id_list):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_cds_by_mrna
        genome_annotation_api = doekbase.data_api.annotation.genome_annotation.api.GenomeAnnotationAPI(self.services, ctx['token'], ref)
        returnVal=genome_annotation_api.get_cds_by_mrna(mrna_id_list)
        #END get_cds_by_mrna

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_cds_by_mrna return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_gene_by_cds(self, ctx, ref, cds_id_list):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_gene_by_cds
        genome_annotation_api = doekbase.data_api.annotation.genome_annotation.api.GenomeAnnotationAPI(self.services, ctx['token'], ref)
        returnVal=genome_annotation_api.get_gene_by_cds(cds_id_list)
        #END get_gene_by_cds

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_gene_by_cds return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_gene_by_mrna(self, ctx, ref, mrna_id_list):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_gene_by_mrna
        genome_annotation_api = doekbase.data_api.annotation.genome_annotation.api.GenomeAnnotationAPI(self.services, ctx['token'], ref)
        returnVal=genome_annotation_api.get_gene_by_mrna(mrna_id_list)
        #END get_gene_by_mrna

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_gene_by_mrna return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_mrna_by_cds(self, ctx, ref, cds_id_list):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_mrna_by_cds
        genome_annotation_api = doekbase.data_api.annotation.genome_annotation.api.GenomeAnnotationAPI(self.services, ctx['token'], ref)
        returnVal=genome_annotation_api.get_mrna_by_cds(cds_id_list)
        #END get_mrna_by_cds

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_mrna_by_cds return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_mrna_by_gene(self, ctx, ref, gene_id_list):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_mrna_by_gene
        genome_annotation_api = doekbase.data_api.annotation.genome_annotation.api.GenomeAnnotationAPI(self.services, ctx['token'], ref)
        returnVal=genome_annotation_api.get_mrna_by_gene(gene_id_list)
        #END get_mrna_by_gene

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_mrna_by_gene return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_mrna_exons(self, ctx, ref, mrna_id_list):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_mrna_exons
        genome_annotation_api = doekbase.data_api.annotation.genome_annotation.api.GenomeAnnotationAPI(self.services, ctx['token'], ref)
        returnVal=genome_annotation_api.get_mrna_by_exons(gene_id_list)
        #END get_mrna_exons

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_mrna_exons return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_mrna_utrs(self, ctx, ref, mrna_id_list):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN get_mrna_utrs
        genome_annotation_api = doekbase.data_api.annotation.genome_annotation.api.GenomeAnnotationAPI(self.services, ctx['token'], ref)
        returnVal=genome_annotation_api.get_mrna_by_utrs(gene_id_list)
        #END get_mrna_utrs

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_mrna_utrs return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK", 'message': "", 'version': self.VERSION,
                     'git_url': self.GIT_URL, 'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]

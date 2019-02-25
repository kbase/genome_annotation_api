# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging

from GenomeAnnotationAPI.GenomeInterfaceV1 import GenomeInterfaceV1
from GenomeAnnotationAPI.utils import Utils
from installed_clients.WorkspaceClient import Workspace
#END_HEADER


class GenomeAnnotationAPI:
    '''
    Module Name:
    GenomeAnnotationAPI

    Module Description:
    
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "1.0.1"
    GIT_URL = "git@github.com:kbase/genome_annotation_api.git"
    GIT_COMMIT_HASH = "8b8c111d492688ae9ea671ec278fdeaab7864331"

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
            "handle_service_url": config['handle-service-url'],
            "service_wizard_url": config['service-wizard-url']
        }
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
        ws = Workspace(self.services['workspace_service_url'], token=ctx['token'])
        utils = Utils(ws)
        returnVal = utils.get_taxon(inputs_get_taxon)
        #END get_taxon

        # At some point might do deeper type checking...
        if not isinstance(returnVal, str):
            raise ValueError('Method get_taxon return value ' +
                             'returnVal is not type str as required.')
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
        ws = Workspace(self.services['workspace_service_url'], token=ctx['token'])
        utils = Utils(ws)
        returnVal = utils.get_assembly(inputs_get_assembly)
        #END get_assembly

        # At some point might do deeper type checking...
        if not isinstance(returnVal, str):
            raise ValueError('Method get_assembly return value ' +
                             'returnVal is not type str as required.')
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
        ws = Workspace(self.services['workspace_service_url'], token=ctx['token'])
        utils = Utils(ws)
        returnVal = utils.get_feature_types(inputs_get_feature_types)
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
        ws = Workspace(self.services['workspace_service_url'], token=ctx['token'])
        utils = Utils(ws)
        returnVal = utils.get_feature_type_descriptions(inputs_get_feature_type_descriptions)
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
        ws = Workspace(self.services['workspace_service_url'], token=ctx['token'])
        utils = Utils(ws)
        returnVal = utils.get_feature_type_counts(inputs_get_feature_type_counts)
        #END get_feature_type_counts

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_type_counts return value ' +
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
        ws = Workspace(self.services['workspace_service_url'], token=ctx['token'])
        utils = Utils(ws)
        returnVal = utils.get_feature_proteins(inputs_get_proteins)
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
        ws = Workspace(self.services['workspace_service_url'], token=ctx['token'])
        utils = Utils(ws)
        returnVal = utils.get_feature_locations(inputs_get_feature_locations)
        #END get_feature_locations

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_locations return value ' +
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
        ws = Workspace(self.services['workspace_service_url'], token=ctx['token'])
        utils = Utils(ws)
        returnVal = utils.get_feature_dna_sequences(inputs_get_feature_dna)
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
        ws = Workspace(self.services['workspace_service_url'], token=ctx['token'])
        utils = Utils(ws)
        returnVal = utils.get_feature_functions(inputs_get_feature_functions)
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
        ws = Workspace(self.services['workspace_service_url'], token=ctx['token'])
        utils = Utils(ws)
        returnVal = utils.get_feature_aliases(inputs_get_feature_aliases)
        #END get_feature_aliases

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method get_feature_aliases return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def get_genome_v1(self, ctx, params):
        """
        A reasonably simple wrapper on get_objects2, but with Genome specific
        filters instead of arbitrary get subdata included paths.
        :param params: instance of type "GetGenomeParamsV1" (downgrade -
           optional, defaults to true. Convert new genome features into a
           back-compatible representation. no_merge - optional, defaults to
           false. If a new genome is being downgraded, do not merge new
           fields into the features field.) -> structure: parameter "genomes"
           of list of type "GenomeSelectorV1" (ref - genome refference
           feature array - optional, which array the
           included_feature_position_index refer to. defaults to "features".
           included_feature_position_index - optional, only include features
           at the specified indices ref_path_to_genome - optional, a
           reference path to the genome.) -> structure: parameter "ref" of
           String, parameter "feature_array" of String, parameter
           "included_feature_position_index" of list of Long, parameter
           "ref_path_to_genome" of list of String, parameter
           "included_fields" of list of String, parameter
           "included_feature_fields" of list of String, parameter "downgrade"
           of type "boolean" (A boolean - 0 for false, 1 for true. @range (0,
           1)), parameter "no_merge" of type "boolean" (A boolean - 0 for
           false, 1 for true. @range (0, 1)), parameter "ignore_errors" of
           type "boolean" (A boolean - 0 for false, 1 for true. @range (0,
           1)), parameter "no_data" of type "boolean" (A boolean - 0 for
           false, 1 for true. @range (0, 1)), parameter "no_metadata" of type
           "boolean" (A boolean - 0 for false, 1 for true. @range (0, 1))
        :returns: instance of type "GenomeDataSetV1" -> structure: parameter
           "genomes" of list of type "GenomeDataV1" -> structure: parameter
           "data" of type "Genome" (Genome object holds much of the data
           relevant for a genome in KBase Genome publications should be
           papers about the genome, not papers about certain features of the
           genome (which go into the Feature object) Should the Genome object
           have a list of feature ids? (in addition to having a list of
           feature_refs) Should the Genome object contain a list of
           contig_ids too? @optional assembly_ref quality close_genomes
           analysis_events features source_id source contigs contig_ids
           publications md5 taxonomy gc_content complete dna_size num_contigs
           contig_lengths contigset_ref @metadata ws gc_content as GC content
           @metadata ws taxonomy as Taxonomy @metadata ws md5 as MD5
           @metadata ws dna_size as Size @metadata ws genetic_code as Genetic
           code @metadata ws domain as Domain @metadata ws source_id as
           Source ID @metadata ws source as Source @metadata ws
           scientific_name as Name @metadata ws length(close_genomes) as
           Close genomes @metadata ws length(features) as Number features
           @metadata ws num_contigs as Number contigs) -> structure:
           parameter "id" of type "Genome_id" (KBase genome ID @id kb),
           parameter "scientific_name" of String, parameter "domain" of
           String, parameter "genetic_code" of Long, parameter "dna_size" of
           Long, parameter "num_contigs" of Long, parameter "contigs" of list
           of type "Contig" (Type spec for a "Contig" subobject in the
           "ContigSet" object Contig_id id - ID of contig in contigset string
           md5 - unique hash of contig sequence string sequence - sequence of
           the contig string description - Description of the contig (e.g.
           everything after the ID in a FASTA file) @optional length md5
           genetic_code cell_compartment replicon_geometry replicon_type name
           description complete) -> structure: parameter "id" of type
           "Contig_id" (ContigSet contig ID @id external), parameter "length"
           of Long, parameter "md5" of String, parameter "sequence" of
           String, parameter "genetic_code" of Long, parameter
           "cell_compartment" of String, parameter "replicon_type" of String,
           parameter "replicon_geometry" of String, parameter "name" of
           String, parameter "description" of String, parameter "complete" of
           type "Bool", parameter "contig_lengths" of list of Long, parameter
           "contig_ids" of list of type "Contig_id" (ContigSet contig ID @id
           external), parameter "source" of String, parameter "source_id" of
           type "source_id" (Reference to a source_id @id external),
           parameter "md5" of String, parameter "taxonomy" of String,
           parameter "gc_content" of Double, parameter "complete" of Long,
           parameter "publications" of list of type "publication" (Structure
           for a publication (from ER API) also want to capture authors,
           journal name (not in ER)) -> tuple of size 7: parameter "id" of
           Long, parameter "source_db" of String, parameter "article_title"
           of String, parameter "link" of String, parameter "pubdate" of
           String, parameter "authors" of String, parameter "journal_name" of
           String, parameter "features" of list of type "Feature" (Structure
           for a single feature of a genome Should genome_id contain the
           genome_id in the Genome object, the workspace id of the Genome
           object, a genomeref, something else? Should sequence be in
           separate objects too? We may want to add additional fields for
           other CDM functions (e.g., atomic regulons, coexpressed fids,
           co_occurring fids,...) @optional orthologs quality
           feature_creation_event md5 location function ontology_terms
           protein_translation protein_families subsystems publications
           subsystem_data aliases annotations regulon_data atomic_regulons
           coexpressed_fids co_occurring_fids dna_sequence
           protein_translation_length dna_sequence_length) -> structure:
           parameter "id" of type "Feature_id" (KBase Feature ID @id
           external), parameter "location" of list of tuple of size 4: type
           "Contig_id" (ContigSet contig ID @id external), Long, String,
           Long, parameter "type" of String, parameter "function" of String,
           parameter "ontology_terms" of mapping from String to mapping from
           String to type "OntologyData" -> structure: parameter "id" of
           String, parameter "ontology_ref" of String, parameter
           "term_lineage" of list of String, parameter "term_name" of String,
           parameter "evidence" of list of type "OntologyEvidence" (@optional
           translation_provenance alignment_evidence) -> structure: parameter
           "method" of String, parameter "method_version" of String,
           parameter "timestamp" of String, parameter
           "translation_provenance" of tuple of size 3: parameter
           "ontologytranslation_ref" of String, parameter "namespace" of
           String, parameter "source_term" of String, parameter
           "alignment_evidence" of list of tuple of size 4: parameter "start"
           of Long, parameter "stop" of Long, parameter "align_length" of
           Long, parameter "identify" of Double, parameter "md5" of String,
           parameter "protein_translation" of String, parameter
           "dna_sequence" of String, parameter "protein_translation_length"
           of Long, parameter "dna_sequence_length" of Long, parameter
           "publications" of list of type "publication" (Structure for a
           publication (from ER API) also want to capture authors, journal
           name (not in ER)) -> tuple of size 7: parameter "id" of Long,
           parameter "source_db" of String, parameter "article_title" of
           String, parameter "link" of String, parameter "pubdate" of String,
           parameter "authors" of String, parameter "journal_name" of String,
           parameter "subsystems" of list of String, parameter
           "protein_families" of list of type "ProteinFamily" (Structure for
           a protein family @optional query_begin query_end subject_begin
           subject_end score evalue subject_description release_version) ->
           structure: parameter "id" of String, parameter "subject_db" of
           String, parameter "release_version" of String, parameter
           "subject_description" of String, parameter "query_begin" of Long,
           parameter "query_end" of Long, parameter "subject_begin" of Long,
           parameter "subject_end" of Long, parameter "score" of Double,
           parameter "evalue" of Double, parameter "aliases" of list of
           String, parameter "orthologs" of list of tuple of size 2: String,
           Double, parameter "annotations" of list of type "annotation" (a
           notation by a curator of the genome object) -> tuple of size 3:
           parameter "comment" of String, parameter "annotator" of String,
           parameter "annotation_time" of Double, parameter "subsystem_data"
           of list of type "subsystem_data" (Structure for subsystem data
           (from CDMI API)) -> tuple of size 3: parameter "subsystem" of
           String, parameter "variant" of String, parameter "role" of String,
           parameter "regulon_data" of list of type "regulon_data" (Structure
           for regulon data (from CDMI API)) -> tuple of size 3: parameter
           "regulon_id" of String, parameter "regulon_set" of list of type
           "Feature_id" (KBase Feature ID @id external), parameter "tfs" of
           list of type "Feature_id" (KBase Feature ID @id external),
           parameter "atomic_regulons" of list of type "atomic_regulon"
           (Structure for an atomic regulon (from CDMI API)) -> tuple of size
           2: parameter "atomic_regulon_id" of String, parameter
           "atomic_regulon_size" of Long, parameter "coexpressed_fids" of
           list of type "coexpressed_fid" (Structure for coexpressed fids
           (from CDMI API)) -> tuple of size 2: parameter "scored_fid" of
           type "Feature_id" (KBase Feature ID @id external), parameter
           "score" of Double, parameter "co_occurring_fids" of list of type
           "co_occurring_fid" (Structure for co-occurring fids (from CDMI
           API)) -> tuple of size 2: parameter "scored_fid" of type
           "Feature_id" (KBase Feature ID @id external), parameter "score" of
           Double, parameter "quality" of type "Feature_quality_measure"
           (@optional weighted_hit_count hit_count existence_priority
           overlap_rules pyrrolysylprotein truncated_begin truncated_end
           existence_confidence frameshifted selenoprotein) -> structure:
           parameter "truncated_begin" of type "Bool", parameter
           "truncated_end" of type "Bool", parameter "existence_confidence"
           of Double, parameter "frameshifted" of type "Bool", parameter
           "selenoprotein" of type "Bool", parameter "pyrrolysylprotein" of
           type "Bool", parameter "overlap_rules" of list of String,
           parameter "existence_priority" of Double, parameter "hit_count" of
           Double, parameter "weighted_hit_count" of Double, parameter
           "feature_creation_event" of type "Analysis_event" (@optional
           tool_name execution_time parameters hostname) -> structure:
           parameter "id" of type "Analysis_event_id", parameter "tool_name"
           of String, parameter "execution_time" of Double, parameter
           "parameters" of list of String, parameter "hostname" of String,
           parameter "contigset_ref" of type "ContigSet_ref" (Reference to a
           ContigSet object containing the contigs for this genome in the
           workspace @id ws KBaseGenomes.ContigSet), parameter "assembly_ref"
           of type "Assembly_ref" (Reference to an Assembly object in the
           workspace @id ws KBaseGenomeAnnotations.Assembly), parameter
           "quality" of type "Genome_quality_measure" (@optional
           frameshift_error_rate sequence_error_rate) -> structure: parameter
           "frameshift_error_rate" of Double, parameter "sequence_error_rate"
           of Double, parameter "close_genomes" of list of type
           "Close_genome" (@optional genome closeness_measure) -> structure:
           parameter "genome" of type "Genome_id" (KBase genome ID @id kb),
           parameter "closeness_measure" of Double, parameter
           "analysis_events" of list of type "Analysis_event" (@optional
           tool_name execution_time parameters hostname) -> structure:
           parameter "id" of type "Analysis_event_id", parameter "tool_name"
           of String, parameter "execution_time" of Double, parameter
           "parameters" of list of String, parameter "hostname" of String,
           parameter "info" of type "object_info" (Information about an
           object, including user provided metadata. obj_id objid - the
           numerical id of the object. obj_name name - the name of the
           object. type_string type - the type of the object. timestamp
           save_date - the save date of the object. obj_ver ver - the version
           of the object. username saved_by - the user that saved or copied
           the object. ws_id wsid - the workspace containing the object.
           ws_name workspace - the workspace containing the object. string
           chsum - the md5 checksum of the object. int size - the size of the
           object in bytes. usermeta meta - arbitrary user-supplied metadata
           about the object.) -> tuple of size 11: parameter "objid" of type
           "obj_id" (The unique, permanent numerical ID of an object.),
           parameter "name" of type "obj_name" (A string used as a name for
           an object. Any string consisting of alphanumeric characters and
           the characters |._- that is not an integer is acceptable.),
           parameter "type" of type "type_string" (A type string. Specifies
           the type and its version in a single string in the format
           [module].[typename]-[major].[minor]: module - a string. The module
           name of the typespec containing the type. typename - a string. The
           name of the type as assigned by the typedef statement. major - an
           integer. The major version of the type. A change in the major
           version implies the type has changed in a non-backwards compatible
           way. minor - an integer. The minor version of the type. A change
           in the minor version implies that the type has changed in a way
           that is backwards compatible with previous type definitions. In
           many cases, the major and minor versions are optional, and if not
           provided the most recent version will be used. Example:
           MyModule.MyType-3.1), parameter "save_date" of type "timestamp" (A
           time in the format YYYY-MM-DDThh:mm:ssZ, where Z is either the
           character Z (representing the UTC timezone) or the difference in
           time to UTC in the format +/-HHMM, eg: 2012-12-17T23:24:06-0500
           (EST time) 2013-04-03T08:56:32+0000 (UTC time)
           2013-04-03T08:56:32Z (UTC time)), parameter "version" of Long,
           parameter "saved_by" of type "username" (Login name of a KBase
           user account.), parameter "wsid" of type "ws_id" (The unique,
           permanent numerical ID of a workspace.), parameter "workspace" of
           type "ws_name" (A string used as a name for a workspace. Any
           string consisting of alphanumeric characters and "_", ".", or "-"
           that is not an integer is acceptable. The name may optionally be
           prefixed with the workspace owner's user name and a colon, e.g.
           kbasetest:my_workspace.), parameter "chsum" of String, parameter
           "size" of Long, parameter "meta" of type "usermeta" (User provided
           metadata about an object. Arbitrary key-value pairs provided by
           the user.) -> mapping from String to String, parameter
           "provenance" of list of type "ProvenanceAction" (A provenance
           action. A provenance action (PA) is an action taken while
           transforming one data object to another. There may be several PAs
           taken in series. A PA is typically running a script, running an
           api command, etc. All of the following fields are optional, but
           more information provided equates to better data provenance.
           resolved_ws_objects should never be set by the user; it is set by
           the workspace service when returning data. On input, only one of
           the time or epoch may be supplied. Both are supplied on output.
           The maximum size of the entire provenance object, including all
           actions, is 1MB. timestamp time - the time the action was started
           epoch epoch - the time the action was started. string caller - the
           name or id of the invoker of this provenance action. In most
           cases, this will be the same for all PAs. string service - the
           name of the service that performed this action. string service_ver
           - the version of the service that performed this action. string
           method - the method of the service that performed this action.
           list<UnspecifiedObject> method_params - the parameters of the
           method that performed this action. If an object in the parameters
           is a workspace object, also put the object reference in the
           input_ws_object list. string script - the name of the script that
           performed this action. string script_ver - the version of the
           script that performed this action. string script_command_line -
           the command line provided to the script that performed this
           action. If workspace objects were provided in the command line,
           also put the object reference in the input_ws_object list.
           list<obj_ref> input_ws_objects - the workspace objects that were
           used as input to this action; typically these will also be present
           as parts of the method_params or the script_command_line
           arguments. list<obj_ref> resolved_ws_objects - the workspace
           objects ids from input_ws_objects resolved to permanent workspace
           object references by the workspace service. list<string>
           intermediate_incoming - if the previous action produced output
           that 1) was not stored in a referrable way, and 2) is used as
           input for this action, provide it with an arbitrary and unique ID
           here, in the order of the input arguments to this action. These
           IDs can be used in the method_params argument. list<string>
           intermediate_outgoing - if this action produced output that 1) was
           not stored in a referrable way, and 2) is used as input for the
           next action, provide it with an arbitrary and unique ID here, in
           the order of the output values from this action. These IDs can be
           used in the intermediate_incoming argument in the next action.
           list<ExternalDataUnit> external_data - data external to the
           workspace that was either imported to the workspace or used to
           create a workspace object. list<SubAction> subactions - the
           subactions taken as a part of this action. mapping<string, string>
           custom - user definable custom provenance fields and their values.
           string description - a free text description of this action.) ->
           structure: parameter "time" of type "timestamp" (A time in the
           format YYYY-MM-DDThh:mm:ssZ, where Z is either the character Z
           (representing the UTC timezone) or the difference in time to UTC
           in the format +/-HHMM, eg: 2012-12-17T23:24:06-0500 (EST time)
           2013-04-03T08:56:32+0000 (UTC time) 2013-04-03T08:56:32Z (UTC
           time)), parameter "epoch" of type "epoch" (A Unix epoch (the time
           since 00:00:00 1/1/1970 UTC) in milliseconds.), parameter "caller"
           of String, parameter "service" of String, parameter "service_ver"
           of String, parameter "method" of String, parameter "method_params"
           of list of unspecified object, parameter "script" of String,
           parameter "script_ver" of String, parameter "script_command_line"
           of String, parameter "input_ws_objects" of list of type "obj_ref"
           (A string that uniquely identifies an object in the workspace
           service. There are two ways to uniquely identify an object in one
           string: "[ws_name or id]/[obj_name or id]/[obj_ver]" - for
           example, "MyFirstWorkspace/MyFirstObject/3" would identify the
           third version of an object called MyFirstObject in the workspace
           called MyFirstWorkspace. 42/Panic/1 would identify the first
           version of the object name Panic in workspace with id 42.
           Towel/1/6 would identify the 6th version of the object with id 1
           in the Towel workspace. "kb|ws.[ws_id].obj.[obj_id].ver.[obj_ver]"
           - for example, "kb|ws.23.obj.567.ver.2" would identify the second
           version of an object with id 567 in a workspace with id 23. In all
           cases, if the version number is omitted, the latest version of the
           object is assumed.), parameter "resolved_ws_objects" of list of
           type "obj_ref" (A string that uniquely identifies an object in the
           workspace service. There are two ways to uniquely identify an
           object in one string: "[ws_name or id]/[obj_name or id]/[obj_ver]"
           - for example, "MyFirstWorkspace/MyFirstObject/3" would identify
           the third version of an object called MyFirstObject in the
           workspace called MyFirstWorkspace. 42/Panic/1 would identify the
           first version of the object name Panic in workspace with id 42.
           Towel/1/6 would identify the 6th version of the object with id 1
           in the Towel workspace. "kb|ws.[ws_id].obj.[obj_id].ver.[obj_ver]"
           - for example, "kb|ws.23.obj.567.ver.2" would identify the second
           version of an object with id 567 in a workspace with id 23. In all
           cases, if the version number is omitted, the latest version of the
           object is assumed.), parameter "intermediate_incoming" of list of
           String, parameter "intermediate_outgoing" of list of String,
           parameter "external_data" of list of type "ExternalDataUnit" (An
           external data unit. A piece of data from a source outside the
           Workspace. On input, only one of the resource_release_date or
           resource_release_epoch may be supplied. Both are supplied on
           output. string resource_name - the name of the resource, for
           example JGI. string resource_url - the url of the resource, for
           example http://genome.jgi.doe.gov string resource_version -
           version of the resource timestamp resource_release_date - the
           release date of the resource epoch resource_release_epoch - the
           release date of the resource string data_url - the url of the
           data, for example
           http://genome.jgi.doe.gov/pages/dynamicOrganismDownload.jsf?
           organism=BlaspURHD0036 string data_id - the id of the data, for
           example 7625.2.79179.AGTTCC.adnq.fastq.gz string description - a
           free text description of the data.) -> structure: parameter
           "resource_name" of String, parameter "resource_url" of String,
           parameter "resource_version" of String, parameter
           "resource_release_date" of type "timestamp" (A time in the format
           YYYY-MM-DDThh:mm:ssZ, where Z is either the character Z
           (representing the UTC timezone) or the difference in time to UTC
           in the format +/-HHMM, eg: 2012-12-17T23:24:06-0500 (EST time)
           2013-04-03T08:56:32+0000 (UTC time) 2013-04-03T08:56:32Z (UTC
           time)), parameter "resource_release_epoch" of type "epoch" (A Unix
           epoch (the time since 00:00:00 1/1/1970 UTC) in milliseconds.),
           parameter "data_url" of String, parameter "data_id" of String,
           parameter "description" of String, parameter "subactions" of list
           of type "SubAction" (Information about a subaction that is invoked
           by a provenance action. A provenance action (PA) may invoke
           subactions (SA), e.g. calling a separate piece of code, a service,
           or a script. In most cases these calls are the same from PA to PA
           and so do not need to be listed in the provenance since providing
           information about the PA alone provides reproducibility. In some
           cases, however, SAs may change over time, such that invoking the
           same PA with the same parameters may produce different results.
           For example, if a PA calls a remote server, that server may be
           updated between a PA invoked on day T and another PA invoked on
           day T+1. The SubAction structure allows for specifying information
           about SAs that may dynamically change from PA invocation to PA
           invocation. string name - the name of the SA. string ver - the
           version of SA. string code_url - a url pointing to the SA's
           codebase. string commit - a version control commit ID for the SA.
           string endpoint_url - a url pointing to the access point for the
           SA - a server url, for instance.) -> structure: parameter "name"
           of String, parameter "ver" of String, parameter "code_url" of
           String, parameter "commit" of String, parameter "endpoint_url" of
           String, parameter "custom" of mapping from String to String,
           parameter "description" of String, parameter "creator" of String,
           parameter "orig_wsid" of String, parameter "copied" of String,
           parameter "copy_source_inaccessible" of type "boolean" (A boolean
           - 0 for false, 1 for true. @range (0, 1)), parameter "created" of
           type "timestamp" (A time in the format YYYY-MM-DDThh:mm:ssZ, where
           Z is either the character Z (representing the UTC timezone) or the
           difference in time to UTC in the format +/-HHMM, eg:
           2012-12-17T23:24:06-0500 (EST time) 2013-04-03T08:56:32+0000 (UTC
           time) 2013-04-03T08:56:32Z (UTC time)), parameter "epoch" of type
           "epoch" (A Unix epoch (the time since 00:00:00 1/1/1970 UTC) in
           milliseconds.), parameter "refs" of list of String, parameter
           "extracted_ids" of mapping from type "id_type" (An id type (e.g.
           from a typespec @id annotation: @id [idtype])) to list of type
           "extracted_id" (An id extracted from an object.), parameter
           "handle_error" of String, parameter "handle_stacktrace" of String
        """
        # ctx is the context object
        # return variables are: data
        #BEGIN get_genome_v1
        ws = Workspace(self.services['workspace_service_url'], token=ctx['token'])
        genome_interface_v1 = GenomeInterfaceV1(ws, self.services)
        data = genome_interface_v1.get_genome(ctx, params)
        #END get_genome_v1

        # At some point might do deeper type checking...
        if not isinstance(data, dict):
            raise ValueError('Method get_genome_v1 return value ' +
                             'data is not type dict as required.')
        # return the results
        return [data]

    def save_one_genome_v1(self, ctx, params):
        """
        @deprecated: GenomeFileUtil.save_one_genome
        :param params: instance of type "SaveOneGenomeParamsV1" -> structure:
           parameter "workspace" of String, parameter "name" of String,
           parameter "data" of type "Genome" (Genome object holds much of the
           data relevant for a genome in KBase Genome publications should be
           papers about the genome, not papers about certain features of the
           genome (which go into the Feature object) Should the Genome object
           have a list of feature ids? (in addition to having a list of
           feature_refs) Should the Genome object contain a list of
           contig_ids too? @optional assembly_ref quality close_genomes
           analysis_events features source_id source contigs contig_ids
           publications md5 taxonomy gc_content complete dna_size num_contigs
           contig_lengths contigset_ref @metadata ws gc_content as GC content
           @metadata ws taxonomy as Taxonomy @metadata ws md5 as MD5
           @metadata ws dna_size as Size @metadata ws genetic_code as Genetic
           code @metadata ws domain as Domain @metadata ws source_id as
           Source ID @metadata ws source as Source @metadata ws
           scientific_name as Name @metadata ws length(close_genomes) as
           Close genomes @metadata ws length(features) as Number features
           @metadata ws num_contigs as Number contigs) -> structure:
           parameter "id" of type "Genome_id" (KBase genome ID @id kb),
           parameter "scientific_name" of String, parameter "domain" of
           String, parameter "genetic_code" of Long, parameter "dna_size" of
           Long, parameter "num_contigs" of Long, parameter "contigs" of list
           of type "Contig" (Type spec for a "Contig" subobject in the
           "ContigSet" object Contig_id id - ID of contig in contigset string
           md5 - unique hash of contig sequence string sequence - sequence of
           the contig string description - Description of the contig (e.g.
           everything after the ID in a FASTA file) @optional length md5
           genetic_code cell_compartment replicon_geometry replicon_type name
           description complete) -> structure: parameter "id" of type
           "Contig_id" (ContigSet contig ID @id external), parameter "length"
           of Long, parameter "md5" of String, parameter "sequence" of
           String, parameter "genetic_code" of Long, parameter
           "cell_compartment" of String, parameter "replicon_type" of String,
           parameter "replicon_geometry" of String, parameter "name" of
           String, parameter "description" of String, parameter "complete" of
           type "Bool", parameter "contig_lengths" of list of Long, parameter
           "contig_ids" of list of type "Contig_id" (ContigSet contig ID @id
           external), parameter "source" of String, parameter "source_id" of
           type "source_id" (Reference to a source_id @id external),
           parameter "md5" of String, parameter "taxonomy" of String,
           parameter "gc_content" of Double, parameter "complete" of Long,
           parameter "publications" of list of type "publication" (Structure
           for a publication (from ER API) also want to capture authors,
           journal name (not in ER)) -> tuple of size 7: parameter "id" of
           Long, parameter "source_db" of String, parameter "article_title"
           of String, parameter "link" of String, parameter "pubdate" of
           String, parameter "authors" of String, parameter "journal_name" of
           String, parameter "features" of list of type "Feature" (Structure
           for a single feature of a genome Should genome_id contain the
           genome_id in the Genome object, the workspace id of the Genome
           object, a genomeref, something else? Should sequence be in
           separate objects too? We may want to add additional fields for
           other CDM functions (e.g., atomic regulons, coexpressed fids,
           co_occurring fids,...) @optional orthologs quality
           feature_creation_event md5 location function ontology_terms
           protein_translation protein_families subsystems publications
           subsystem_data aliases annotations regulon_data atomic_regulons
           coexpressed_fids co_occurring_fids dna_sequence
           protein_translation_length dna_sequence_length) -> structure:
           parameter "id" of type "Feature_id" (KBase Feature ID @id
           external), parameter "location" of list of tuple of size 4: type
           "Contig_id" (ContigSet contig ID @id external), Long, String,
           Long, parameter "type" of String, parameter "function" of String,
           parameter "ontology_terms" of mapping from String to mapping from
           String to type "OntologyData" -> structure: parameter "id" of
           String, parameter "ontology_ref" of String, parameter
           "term_lineage" of list of String, parameter "term_name" of String,
           parameter "evidence" of list of type "OntologyEvidence" (@optional
           translation_provenance alignment_evidence) -> structure: parameter
           "method" of String, parameter "method_version" of String,
           parameter "timestamp" of String, parameter
           "translation_provenance" of tuple of size 3: parameter
           "ontologytranslation_ref" of String, parameter "namespace" of
           String, parameter "source_term" of String, parameter
           "alignment_evidence" of list of tuple of size 4: parameter "start"
           of Long, parameter "stop" of Long, parameter "align_length" of
           Long, parameter "identify" of Double, parameter "md5" of String,
           parameter "protein_translation" of String, parameter
           "dna_sequence" of String, parameter "protein_translation_length"
           of Long, parameter "dna_sequence_length" of Long, parameter
           "publications" of list of type "publication" (Structure for a
           publication (from ER API) also want to capture authors, journal
           name (not in ER)) -> tuple of size 7: parameter "id" of Long,
           parameter "source_db" of String, parameter "article_title" of
           String, parameter "link" of String, parameter "pubdate" of String,
           parameter "authors" of String, parameter "journal_name" of String,
           parameter "subsystems" of list of String, parameter
           "protein_families" of list of type "ProteinFamily" (Structure for
           a protein family @optional query_begin query_end subject_begin
           subject_end score evalue subject_description release_version) ->
           structure: parameter "id" of String, parameter "subject_db" of
           String, parameter "release_version" of String, parameter
           "subject_description" of String, parameter "query_begin" of Long,
           parameter "query_end" of Long, parameter "subject_begin" of Long,
           parameter "subject_end" of Long, parameter "score" of Double,
           parameter "evalue" of Double, parameter "aliases" of list of
           String, parameter "orthologs" of list of tuple of size 2: String,
           Double, parameter "annotations" of list of type "annotation" (a
           notation by a curator of the genome object) -> tuple of size 3:
           parameter "comment" of String, parameter "annotator" of String,
           parameter "annotation_time" of Double, parameter "subsystem_data"
           of list of type "subsystem_data" (Structure for subsystem data
           (from CDMI API)) -> tuple of size 3: parameter "subsystem" of
           String, parameter "variant" of String, parameter "role" of String,
           parameter "regulon_data" of list of type "regulon_data" (Structure
           for regulon data (from CDMI API)) -> tuple of size 3: parameter
           "regulon_id" of String, parameter "regulon_set" of list of type
           "Feature_id" (KBase Feature ID @id external), parameter "tfs" of
           list of type "Feature_id" (KBase Feature ID @id external),
           parameter "atomic_regulons" of list of type "atomic_regulon"
           (Structure for an atomic regulon (from CDMI API)) -> tuple of size
           2: parameter "atomic_regulon_id" of String, parameter
           "atomic_regulon_size" of Long, parameter "coexpressed_fids" of
           list of type "coexpressed_fid" (Structure for coexpressed fids
           (from CDMI API)) -> tuple of size 2: parameter "scored_fid" of
           type "Feature_id" (KBase Feature ID @id external), parameter
           "score" of Double, parameter "co_occurring_fids" of list of type
           "co_occurring_fid" (Structure for co-occurring fids (from CDMI
           API)) -> tuple of size 2: parameter "scored_fid" of type
           "Feature_id" (KBase Feature ID @id external), parameter "score" of
           Double, parameter "quality" of type "Feature_quality_measure"
           (@optional weighted_hit_count hit_count existence_priority
           overlap_rules pyrrolysylprotein truncated_begin truncated_end
           existence_confidence frameshifted selenoprotein) -> structure:
           parameter "truncated_begin" of type "Bool", parameter
           "truncated_end" of type "Bool", parameter "existence_confidence"
           of Double, parameter "frameshifted" of type "Bool", parameter
           "selenoprotein" of type "Bool", parameter "pyrrolysylprotein" of
           type "Bool", parameter "overlap_rules" of list of String,
           parameter "existence_priority" of Double, parameter "hit_count" of
           Double, parameter "weighted_hit_count" of Double, parameter
           "feature_creation_event" of type "Analysis_event" (@optional
           tool_name execution_time parameters hostname) -> structure:
           parameter "id" of type "Analysis_event_id", parameter "tool_name"
           of String, parameter "execution_time" of Double, parameter
           "parameters" of list of String, parameter "hostname" of String,
           parameter "contigset_ref" of type "ContigSet_ref" (Reference to a
           ContigSet object containing the contigs for this genome in the
           workspace @id ws KBaseGenomes.ContigSet), parameter "assembly_ref"
           of type "Assembly_ref" (Reference to an Assembly object in the
           workspace @id ws KBaseGenomeAnnotations.Assembly), parameter
           "quality" of type "Genome_quality_measure" (@optional
           frameshift_error_rate sequence_error_rate) -> structure: parameter
           "frameshift_error_rate" of Double, parameter "sequence_error_rate"
           of Double, parameter "close_genomes" of list of type
           "Close_genome" (@optional genome closeness_measure) -> structure:
           parameter "genome" of type "Genome_id" (KBase genome ID @id kb),
           parameter "closeness_measure" of Double, parameter
           "analysis_events" of list of type "Analysis_event" (@optional
           tool_name execution_time parameters hostname) -> structure:
           parameter "id" of type "Analysis_event_id", parameter "tool_name"
           of String, parameter "execution_time" of Double, parameter
           "parameters" of list of String, parameter "hostname" of String,
           parameter "provenance" of list of type "ProvenanceAction" (A
           provenance action. A provenance action (PA) is an action taken
           while transforming one data object to another. There may be
           several PAs taken in series. A PA is typically running a script,
           running an api command, etc. All of the following fields are
           optional, but more information provided equates to better data
           provenance. resolved_ws_objects should never be set by the user;
           it is set by the workspace service when returning data. On input,
           only one of the time or epoch may be supplied. Both are supplied
           on output. The maximum size of the entire provenance object,
           including all actions, is 1MB. timestamp time - the time the
           action was started epoch epoch - the time the action was started.
           string caller - the name or id of the invoker of this provenance
           action. In most cases, this will be the same for all PAs. string
           service - the name of the service that performed this action.
           string service_ver - the version of the service that performed
           this action. string method - the method of the service that
           performed this action. list<UnspecifiedObject> method_params - the
           parameters of the method that performed this action. If an object
           in the parameters is a workspace object, also put the object
           reference in the input_ws_object list. string script - the name of
           the script that performed this action. string script_ver - the
           version of the script that performed this action. string
           script_command_line - the command line provided to the script that
           performed this action. If workspace objects were provided in the
           command line, also put the object reference in the input_ws_object
           list. list<obj_ref> input_ws_objects - the workspace objects that
           were used as input to this action; typically these will also be
           present as parts of the method_params or the script_command_line
           arguments. list<obj_ref> resolved_ws_objects - the workspace
           objects ids from input_ws_objects resolved to permanent workspace
           object references by the workspace service. list<string>
           intermediate_incoming - if the previous action produced output
           that 1) was not stored in a referrable way, and 2) is used as
           input for this action, provide it with an arbitrary and unique ID
           here, in the order of the input arguments to this action. These
           IDs can be used in the method_params argument. list<string>
           intermediate_outgoing - if this action produced output that 1) was
           not stored in a referrable way, and 2) is used as input for the
           next action, provide it with an arbitrary and unique ID here, in
           the order of the output values from this action. These IDs can be
           used in the intermediate_incoming argument in the next action.
           list<ExternalDataUnit> external_data - data external to the
           workspace that was either imported to the workspace or used to
           create a workspace object. list<SubAction> subactions - the
           subactions taken as a part of this action. mapping<string, string>
           custom - user definable custom provenance fields and their values.
           string description - a free text description of this action.) ->
           structure: parameter "time" of type "timestamp" (A time in the
           format YYYY-MM-DDThh:mm:ssZ, where Z is either the character Z
           (representing the UTC timezone) or the difference in time to UTC
           in the format +/-HHMM, eg: 2012-12-17T23:24:06-0500 (EST time)
           2013-04-03T08:56:32+0000 (UTC time) 2013-04-03T08:56:32Z (UTC
           time)), parameter "epoch" of type "epoch" (A Unix epoch (the time
           since 00:00:00 1/1/1970 UTC) in milliseconds.), parameter "caller"
           of String, parameter "service" of String, parameter "service_ver"
           of String, parameter "method" of String, parameter "method_params"
           of list of unspecified object, parameter "script" of String,
           parameter "script_ver" of String, parameter "script_command_line"
           of String, parameter "input_ws_objects" of list of type "obj_ref"
           (A string that uniquely identifies an object in the workspace
           service. There are two ways to uniquely identify an object in one
           string: "[ws_name or id]/[obj_name or id]/[obj_ver]" - for
           example, "MyFirstWorkspace/MyFirstObject/3" would identify the
           third version of an object called MyFirstObject in the workspace
           called MyFirstWorkspace. 42/Panic/1 would identify the first
           version of the object name Panic in workspace with id 42.
           Towel/1/6 would identify the 6th version of the object with id 1
           in the Towel workspace. "kb|ws.[ws_id].obj.[obj_id].ver.[obj_ver]"
           - for example, "kb|ws.23.obj.567.ver.2" would identify the second
           version of an object with id 567 in a workspace with id 23. In all
           cases, if the version number is omitted, the latest version of the
           object is assumed.), parameter "resolved_ws_objects" of list of
           type "obj_ref" (A string that uniquely identifies an object in the
           workspace service. There are two ways to uniquely identify an
           object in one string: "[ws_name or id]/[obj_name or id]/[obj_ver]"
           - for example, "MyFirstWorkspace/MyFirstObject/3" would identify
           the third version of an object called MyFirstObject in the
           workspace called MyFirstWorkspace. 42/Panic/1 would identify the
           first version of the object name Panic in workspace with id 42.
           Towel/1/6 would identify the 6th version of the object with id 1
           in the Towel workspace. "kb|ws.[ws_id].obj.[obj_id].ver.[obj_ver]"
           - for example, "kb|ws.23.obj.567.ver.2" would identify the second
           version of an object with id 567 in a workspace with id 23. In all
           cases, if the version number is omitted, the latest version of the
           object is assumed.), parameter "intermediate_incoming" of list of
           String, parameter "intermediate_outgoing" of list of String,
           parameter "external_data" of list of type "ExternalDataUnit" (An
           external data unit. A piece of data from a source outside the
           Workspace. On input, only one of the resource_release_date or
           resource_release_epoch may be supplied. Both are supplied on
           output. string resource_name - the name of the resource, for
           example JGI. string resource_url - the url of the resource, for
           example http://genome.jgi.doe.gov string resource_version -
           version of the resource timestamp resource_release_date - the
           release date of the resource epoch resource_release_epoch - the
           release date of the resource string data_url - the url of the
           data, for example
           http://genome.jgi.doe.gov/pages/dynamicOrganismDownload.jsf?
           organism=BlaspURHD0036 string data_id - the id of the data, for
           example 7625.2.79179.AGTTCC.adnq.fastq.gz string description - a
           free text description of the data.) -> structure: parameter
           "resource_name" of String, parameter "resource_url" of String,
           parameter "resource_version" of String, parameter
           "resource_release_date" of type "timestamp" (A time in the format
           YYYY-MM-DDThh:mm:ssZ, where Z is either the character Z
           (representing the UTC timezone) or the difference in time to UTC
           in the format +/-HHMM, eg: 2012-12-17T23:24:06-0500 (EST time)
           2013-04-03T08:56:32+0000 (UTC time) 2013-04-03T08:56:32Z (UTC
           time)), parameter "resource_release_epoch" of type "epoch" (A Unix
           epoch (the time since 00:00:00 1/1/1970 UTC) in milliseconds.),
           parameter "data_url" of String, parameter "data_id" of String,
           parameter "description" of String, parameter "subactions" of list
           of type "SubAction" (Information about a subaction that is invoked
           by a provenance action. A provenance action (PA) may invoke
           subactions (SA), e.g. calling a separate piece of code, a service,
           or a script. In most cases these calls are the same from PA to PA
           and so do not need to be listed in the provenance since providing
           information about the PA alone provides reproducibility. In some
           cases, however, SAs may change over time, such that invoking the
           same PA with the same parameters may produce different results.
           For example, if a PA calls a remote server, that server may be
           updated between a PA invoked on day T and another PA invoked on
           day T+1. The SubAction structure allows for specifying information
           about SAs that may dynamically change from PA invocation to PA
           invocation. string name - the name of the SA. string ver - the
           version of SA. string code_url - a url pointing to the SA's
           codebase. string commit - a version control commit ID for the SA.
           string endpoint_url - a url pointing to the access point for the
           SA - a server url, for instance.) -> structure: parameter "name"
           of String, parameter "ver" of String, parameter "code_url" of
           String, parameter "commit" of String, parameter "endpoint_url" of
           String, parameter "custom" of mapping from String to String,
           parameter "description" of String, parameter "hidden" of type
           "boolean" (A boolean - 0 for false, 1 for true. @range (0, 1))
        :returns: instance of type "SaveGenomeResultV1" -> structure:
           parameter "info" of type "object_info" (Information about an
           object, including user provided metadata. obj_id objid - the
           numerical id of the object. obj_name name - the name of the
           object. type_string type - the type of the object. timestamp
           save_date - the save date of the object. obj_ver ver - the version
           of the object. username saved_by - the user that saved or copied
           the object. ws_id wsid - the workspace containing the object.
           ws_name workspace - the workspace containing the object. string
           chsum - the md5 checksum of the object. int size - the size of the
           object in bytes. usermeta meta - arbitrary user-supplied metadata
           about the object.) -> tuple of size 11: parameter "objid" of type
           "obj_id" (The unique, permanent numerical ID of an object.),
           parameter "name" of type "obj_name" (A string used as a name for
           an object. Any string consisting of alphanumeric characters and
           the characters |._- that is not an integer is acceptable.),
           parameter "type" of type "type_string" (A type string. Specifies
           the type and its version in a single string in the format
           [module].[typename]-[major].[minor]: module - a string. The module
           name of the typespec containing the type. typename - a string. The
           name of the type as assigned by the typedef statement. major - an
           integer. The major version of the type. A change in the major
           version implies the type has changed in a non-backwards compatible
           way. minor - an integer. The minor version of the type. A change
           in the minor version implies that the type has changed in a way
           that is backwards compatible with previous type definitions. In
           many cases, the major and minor versions are optional, and if not
           provided the most recent version will be used. Example:
           MyModule.MyType-3.1), parameter "save_date" of type "timestamp" (A
           time in the format YYYY-MM-DDThh:mm:ssZ, where Z is either the
           character Z (representing the UTC timezone) or the difference in
           time to UTC in the format +/-HHMM, eg: 2012-12-17T23:24:06-0500
           (EST time) 2013-04-03T08:56:32+0000 (UTC time)
           2013-04-03T08:56:32Z (UTC time)), parameter "version" of Long,
           parameter "saved_by" of type "username" (Login name of a KBase
           user account.), parameter "wsid" of type "ws_id" (The unique,
           permanent numerical ID of a workspace.), parameter "workspace" of
           type "ws_name" (A string used as a name for a workspace. Any
           string consisting of alphanumeric characters and "_", ".", or "-"
           that is not an integer is acceptable. The name may optionally be
           prefixed with the workspace owner's user name and a colon, e.g.
           kbasetest:my_workspace.), parameter "chsum" of String, parameter
           "size" of Long, parameter "meta" of type "usermeta" (User provided
           metadata about an object. Arbitrary key-value pairs provided by
           the user.) -> mapping from String to String
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN save_one_genome_v1
        ws = Workspace(self.services['workspace_service_url'], token=ctx['token'])
        genome_interface_v1 = GenomeInterfaceV1(ws, self.services)
        result = genome_interface_v1.save_one_genome(ctx, params)
        #END save_one_genome_v1

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method save_one_genome_v1 return value ' +
                             'result is not type dict as required.')
        # return the results
        return [result]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK", 'message': "", 'version': self.VERSION,
                     'git_url': self.GIT_URL, 'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]

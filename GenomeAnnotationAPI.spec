/*
A KBase module: GenomeAnnotationAPI
*/

#include <workspace.spec>
#include <KBaseGenomes.spec>


module GenomeAnnotationAPI {
    typedef string ObjectReference;

    /* A boolean - 0 for false, 1 for true.
       @range (0, 1)
    */
    typedef int boolean;

    typedef structure {
        /** The identifier for the contig to which this region corresponds. */
        string contig_id;
        /** Either a "+" or a "-", for the strand on which the region is located. */
        string strand;
        /** Starting position for this region. */
        int start;
        /** Distance from the start position that bounds the end of the region. */
        int length;
    }  Region;

    /**
     * Filters passed to :meth:`get_feature_ids`
     * @optional type_list region_list function_list alias_list
     */
    typedef structure {
        /**
         * List of Feature type strings.
         */
        list<string> type_list;
        /**
         * List of region specs.
         * For example::
         *     [{"contig_id": str, "strand": "+"|"-",
         *       "start": int, "length": int},...]
         *
         * The Feature sequence begin and end are calculated as follows:
         *   - [start, start) for "+" strand
         *   - (start - length, start] for "-" strand
         */
        list<Region> region_list;
        /**
         * List of function strings.
         */
        list<string> function_list;
        /**
         *  List of alias strings.
         */
        list<string> alias_list;
    }  Feature_id_filters;

    /* @optional by_type by_region by_function by_alias */
    typedef structure {
        /** Mapping of Feature type string to a list of Feature IDs */
        mapping<string, list<string>> by_type;
        /**
         * Mapping of contig ID, strand "+" or "-", and range "start--end" to
         * a list of Feature IDs. For example::
         *    {'contig1': {'+': {'123--456': ['feature1', 'feature2'] }}}
         */
        mapping<string, mapping<string, mapping<string, list<string>>>> by_region;
        /** Mapping of function string to a list of Feature IDs */
        mapping<string, list<string>> by_function;
        /** Mapping of alias string to a list of Feature IDs */
        mapping<string, list<string>> by_alias;
    }  Feature_id_mapping;

    typedef structure {
        /** Identifier for this feature */
        string feature_id;
        /** The Feature type e.g., "mRNA", "CDS", "gene", ... */
        string feature_type;
        /** The functional annotation description */
        string feature_function;
        /** Dictionary of Alias string to List of source string identifiers */
        mapping<string, list<string>> feature_aliases;
        /** Integer representing the length of the DNA sequence for convenience */
        int feature_dna_sequence_length;
        /** String containing the DNA sequence of the Feature */
        string feature_dna_sequence;
        /** String containing the MD5 of the sequence, calculated from the uppercase string */
        string feature_md5;
        /**
         * List of dictionaries::
         *     { "contig_id": str,
         *       "start": int,
         *       "strand": str,
         *       "length": int  }
         *
         * List of Feature regions, where the Feature bounds are
         * calculated as follows:
         *
         * - For "+" strand, [start, start + length)
         * - For "-" strand, (start - length, start]
        */
        list<Region> feature_locations;
        /**
         * List of any known publications related to this Feature
         */
        list<string> feature_publications;
        /**
         * List of strings indicating known data quality issues.
         * Note: not used for Genome type, but is used for
         * GenomeAnnotation
         */
        list<string> feature_quality_warnings;
        /**
         * Quality value with unknown algorithm for Genomes,
         * not calculated yet for GenomeAnnotations.
         */
        list<string> feature_quality_score;
        /** Notes recorded about this Feature */
        string feature_notes;
        /** Inference information */
        string feature_inference;
    }  Feature_data;

    typedef structure {
        /** Protein identifier, which is feature ID plus ".protein" */
        string protein_id;
        /** Amino acid sequence for this protein */
        string protein_amino_acid_sequence;
        /** Function of protein */
        string protein_function;
        /** List of aliases for the protein */
        mapping<string, list<string>> protein_aliases;
        /** MD5 hash of the protein translation (uppercase) */
        string protein_md5;
        list<string> protein_domain_locations;
    }  Protein_data;

    typedef structure {
        /** Location of the exon in the contig. */
        Region exon_location;
        /** DNA Sequence string. */
        string exon_dna_sequence;
        /** The position of the exon, ordered 5' to 3'. */
        int exon_ordinal;
    }  Exon_data;

    typedef structure {
        /** Locations of this UTR */
        list<Region> utr_locations;
        /** DNA sequence string for this UTR */
        string utr_dna_sequence;
    }  UTR_data;

    typedef structure {
        /** Scientific name of the organism. */
        string scientific_name;
        /** NCBI taxonomic id of the organism. */
        int taxonomy_id;
        /** Taxonomic kingdom of the organism. */
        string kingdom;
        /** Scientific lineage of the organism. */
        list<string> scientific_lineage;
        /** Scientific name of the organism. */
        int genetic_code;
        /** Aliases for the organism associated with this GenomeAnnotation. */
        list<string> organism_aliases;
        /** Source organization for the Assembly. */
        string assembly_source;
        /** Identifier for the Assembly used by the source organization. */
        string assembly_source_id;
        /** Date of origin the source indicates for the Assembly. */
        string assembly_source_date;
        /** GC content for the entire Assembly. */
        float gc_content;
        /** Total DNA size for the Assembly. */
        int dna_size;
        /** Number of contigs in the Assembly. */
        int num_contigs;
        /** Contig identifier strings for the Assembly. */
        list<string> contig_ids;
        /** Name of the external source. */
        string external_source;
        /** Date of origin the external source indicates for this GenomeAnnotation. */
        string external_source_date;
        /** Release version for this GenomeAnnotation data. */
        string release;
        /** Name of the file used to generate this GenomeAnnotation. */
        string original_source_filename;
        /** Number of features of each type. */
        mapping<string, int> feature_type_counts;
    } Summary_data;

    /*
        gene_id is a feature id of a gene feature.
        mrna_id is a feature id of a mrna feature.
        cds_id is a feature id of a cds feature.
    */
    typedef structure {
        string gene_type;
        string mrna_type;
        string cds_type;
        list<string> feature_types;
        mapping<string, mapping<string, Feature_data>> feature_by_id_by_type;
        mapping<string, Protein_data> protein_by_cds_id;
        mapping<string, list<string>> mrna_ids_by_gene_id;
        mapping<string, list<string>> cds_ids_by_gene_id;
        mapping<string, string> cds_id_by_mrna_id;
        mapping<string, list<Exon_data>> exons_by_mrna_id;
        mapping<string, mapping<string, UTR_data>> utr_by_utr_type_by_mrna_id;
        Summary_data summary;
    } GenomeAnnotation_data;

    /**
     * Retrieve the Taxon associated with this GenomeAnnotation.
     *
     * @return Reference to TaxonAPI object
     */

    typedef structure {
        ObjectReference ref;
    } inputs_get_taxon;

    funcdef get_taxon(inputs_get_taxon) returns (ObjectReference) authentication required;

    /**
     * Retrieve the Assembly associated with this GenomeAnnotation.
     *
     * @return Reference to AssemblyAPI object
     */

    typedef structure {
        ObjectReference ref;
    } inputs_get_assembly;

    funcdef get_assembly(inputs_get_assembly) returns (ObjectReference) authentication required;

    /**
     * Retrieve the list of Feature types.
     *
     * @return List of feature type identifiers (strings)
     */

    typedef structure {
        ObjectReference ref;
    } inputs_get_feature_types;

    funcdef get_feature_types(inputs_get_feature_types) returns (list<string>) authentication required;

    /**
     * Retrieve the descriptions for each Feature type in
     * this GenomeAnnotation.
     *
     * @param feature_type_list List of Feature types. If this list
     *  is empty or None,
     *  the whole mapping will be returned.
     * @return Name and description for each requested Feature Type
     */

    /* optional feature_type_list */
    typedef structure {
        ObjectReference ref;
        list<string> feature_type_list;
    } inputs_get_feature_type_descriptions;

    funcdef get_feature_type_descriptions(inputs_get_feature_type_descriptions)
        returns (mapping<string, string>) authentication required;

    /**
     * Retrieve the count of each Feature type.
     *
     * @param feature_type_list  List of Feature Types. If empty,
     *   this will retrieve  counts for all Feature Types.
     */

    /* @optional feature_type_list */
    typedef structure {
        ObjectReference ref;
        list<string> feature_type_list;
    } inputs_get_feature_type_counts;

    funcdef get_feature_type_counts(inputs_get_feature_type_counts)
        returns (mapping<string,int>) authentication required;

    /**
     * Retrieve Protein data.
     *
     * @return Mapping from protein ID to data about the protein.
     */

    typedef structure {
        ObjectReference ref;
    } inputs_get_proteins;

    funcdef get_proteins(inputs_get_proteins) returns (mapping<string, Protein_data>) authentication required;

    /**
     * Retrieve Feature locations.
     *
     * @param feature_id_list List of Feature IDs for which to retrieve locations.
     *     If empty, returns data for all features.
     * @return Mapping from Feature IDs to location information for each.
     */

    /* optional feature_id_list */
    typedef structure {
        ObjectReference ref;
        list<string> feature_id_list;
    } inputs_get_feature_locations;

    funcdef get_feature_locations(inputs_get_feature_locations)
        returns (mapping<string, list<Region>>) authentication required;

    /**
     * Retrieve Feature DNA sequences.
     *
     * @param feature_id_list List of Feature IDs for which to retrieve sequences.
     *     If empty, returns data for all features.
     * @return Mapping of Feature IDs to their DNA sequence.
     */

    typedef structure {
        ObjectReference ref;
        list<string> feature_id_list;
    } inputs_get_feature_dna;

    funcdef get_feature_dna(inputs_get_feature_dna)
        returns (mapping<string, string>) authentication required;

    /**
     * Retrieve Feature functions.
     *
     * @param feature_id_list List of Feature IDs for which to retrieve functions.
     *     If empty, returns data for all features.
     * @return Mapping of Feature IDs to their functions.
     */

    /* @optional feature_id_list */
    typedef structure {
        ObjectReference ref;
        list<string> feature_id_list;
    } inputs_get_feature_functions;

    funcdef get_feature_functions(inputs_get_feature_functions)
        returns (mapping<string, string>) authentication required;

    /**
     * Retrieve Feature aliases.
     *
     * @param feature_id_list List of Feature IDS for which to retrieve aliases.
     *     If empty, returns data for all features.
     * @return Mapping of Feature IDs to a list of aliases.
     */

    /* @optional feature_id_list */
    typedef structure {
        ObjectReference ref;
        list<string> feature_id_list;
    } inputs_get_feature_aliases;

    funcdef get_feature_aliases(inputs_get_feature_aliases)
        returns (mapping<string, list<string>>) authentication required;

    /*
        ref - genome refference
        feature array - optional, which array the included_feature_position_index
            refer to. defaults to "features".
        included_feature_position_index - optional, only include features at
            the specified indices
        ref_path_to_genome - optional, a reference path to the genome.
    */
    typedef structure {
        string ref;
        string feature_array;
        list <int> included_feature_position_index;
        list <string> ref_path_to_genome;
    } GenomeSelectorV1;


    /*
        downgrade - optional, defaults to true. Convert new genome features into
            a back-compatible representation.
        no_merge - optional, defaults to false. If a new genome is being downgraded, do not merge
            new fields into the features field.
    */
    typedef structure {
        list <GenomeSelectorV1> genomes;

        list <string> included_fields;
        list <string> included_feature_fields;

        boolean downgrade;
        boolean no_merge;
        boolean ignore_errors;
        boolean no_data;
        boolean no_metadata;
    } GetGenomeParamsV1;


    /* */
    typedef structure {
        KBaseGenomes.Genome data;

        Workspace.object_info info;
        list<Workspace.ProvenanceAction> provenance;

        string creator;
        string orig_wsid;
        string copied;
        boolean copy_source_inaccessible;

        Workspace.timestamp created;
        Workspace.epoch epoch;

        list<string> refs;
        mapping<Workspace.id_type, list<Workspace.extracted_id>> extracted_ids;

        string handle_error;
        string handle_stacktrace;
    } GenomeDataV1;


    typedef structure {
        list<GenomeDataV1> genomes;
    } GenomeDataSetV1;

    /* A reasonably simple wrapper on get_objects2, but with Genome specific
        filters instead of arbitrary get subdata included paths.
    */
    funcdef get_genome_v1(GetGenomeParamsV1 params)
                returns (GenomeDataSetV1 data) authentication optional;

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
    /*
        @deprecated: GenomeFileUtil.save_one_genome
    */

    funcdef save_one_genome_v1(SaveOneGenomeParamsV1 params)
                returns (SaveGenomeResultV1 result) authentication required;


};

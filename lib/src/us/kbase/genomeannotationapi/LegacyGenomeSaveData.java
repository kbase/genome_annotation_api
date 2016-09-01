
package us.kbase.genomeannotationapi;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import us.kbase.kbasegenomes.Genome;
import us.kbase.workspace.ProvenanceAction;


/**
 * <p>Original spec-file type: LegacyGenomeSaveData</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "data",
    "hidden",
    "provenance"
})
public class LegacyGenomeSaveData {

    /**
     * <p>Original spec-file type: Genome</p>
     * <pre>
     * Genome object holds much of the data relevant for a genome in KBase
     *         Genome publications should be papers about the genome, not
     *         papers about certain features of the genome (which go into the
     *         Feature object)
     *         Should the Genome object have a list of feature ids? (in
     *         addition to having a list of feature_refs)
     *         Should the Genome object contain a list of contig_ids too?
     * @optional assembly_ref quality close_genomes analysis_events features source_id source contigs contig_ids publications md5 taxonomy gc_content complete dna_size num_contigs contig_lengths contigset_ref
     * @metadata ws gc_content as GC content
     * @metadata ws taxonomy as Taxonomy
     * @metadata ws md5 as MD5
     * @metadata ws dna_size as Size
     * @metadata ws genetic_code as Genetic code
     * @metadata ws domain as Domain
     *     @metadata ws source_id as Source ID
     *     @metadata ws source as Source
     *     @metadata ws scientific_name as Name
     *     @metadata ws length(close_genomes) as Close genomes
     *     @metadata ws length(features) as Number features
     *     @metadata ws num_contigs as Number contigs
     * </pre>
     * 
     */
    @JsonProperty("data")
    private Genome data;
    @JsonProperty("hidden")
    private Long hidden;
    @JsonProperty("provenance")
    private List<ProvenanceAction> provenance;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    /**
     * <p>Original spec-file type: Genome</p>
     * <pre>
     * Genome object holds much of the data relevant for a genome in KBase
     *         Genome publications should be papers about the genome, not
     *         papers about certain features of the genome (which go into the
     *         Feature object)
     *         Should the Genome object have a list of feature ids? (in
     *         addition to having a list of feature_refs)
     *         Should the Genome object contain a list of contig_ids too?
     * @optional assembly_ref quality close_genomes analysis_events features source_id source contigs contig_ids publications md5 taxonomy gc_content complete dna_size num_contigs contig_lengths contigset_ref
     * @metadata ws gc_content as GC content
     * @metadata ws taxonomy as Taxonomy
     * @metadata ws md5 as MD5
     * @metadata ws dna_size as Size
     * @metadata ws genetic_code as Genetic code
     * @metadata ws domain as Domain
     *     @metadata ws source_id as Source ID
     *     @metadata ws source as Source
     *     @metadata ws scientific_name as Name
     *     @metadata ws length(close_genomes) as Close genomes
     *     @metadata ws length(features) as Number features
     *     @metadata ws num_contigs as Number contigs
     * </pre>
     * 
     */
    @JsonProperty("data")
    public Genome getData() {
        return data;
    }

    /**
     * <p>Original spec-file type: Genome</p>
     * <pre>
     * Genome object holds much of the data relevant for a genome in KBase
     *         Genome publications should be papers about the genome, not
     *         papers about certain features of the genome (which go into the
     *         Feature object)
     *         Should the Genome object have a list of feature ids? (in
     *         addition to having a list of feature_refs)
     *         Should the Genome object contain a list of contig_ids too?
     * @optional assembly_ref quality close_genomes analysis_events features source_id source contigs contig_ids publications md5 taxonomy gc_content complete dna_size num_contigs contig_lengths contigset_ref
     * @metadata ws gc_content as GC content
     * @metadata ws taxonomy as Taxonomy
     * @metadata ws md5 as MD5
     * @metadata ws dna_size as Size
     * @metadata ws genetic_code as Genetic code
     * @metadata ws domain as Domain
     *     @metadata ws source_id as Source ID
     *     @metadata ws source as Source
     *     @metadata ws scientific_name as Name
     *     @metadata ws length(close_genomes) as Close genomes
     *     @metadata ws length(features) as Number features
     *     @metadata ws num_contigs as Number contigs
     * </pre>
     * 
     */
    @JsonProperty("data")
    public void setData(Genome data) {
        this.data = data;
    }

    public LegacyGenomeSaveData withData(Genome data) {
        this.data = data;
        return this;
    }

    @JsonProperty("hidden")
    public Long getHidden() {
        return hidden;
    }

    @JsonProperty("hidden")
    public void setHidden(Long hidden) {
        this.hidden = hidden;
    }

    public LegacyGenomeSaveData withHidden(Long hidden) {
        this.hidden = hidden;
        return this;
    }

    @JsonProperty("provenance")
    public List<ProvenanceAction> getProvenance() {
        return provenance;
    }

    @JsonProperty("provenance")
    public void setProvenance(List<ProvenanceAction> provenance) {
        this.provenance = provenance;
    }

    public LegacyGenomeSaveData withProvenance(List<ProvenanceAction> provenance) {
        this.provenance = provenance;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((("LegacyGenomeSaveData"+" [data=")+ data)+", hidden=")+ hidden)+", provenance=")+ provenance)+", additionalProperties=")+ additionalProperties)+"]");
    }

}

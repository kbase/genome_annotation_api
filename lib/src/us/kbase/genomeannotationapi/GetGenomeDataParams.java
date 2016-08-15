
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


/**
 * <p>Original spec-file type: GetGenomeDataParams</p>
 * <pre>
 * * Retrieve any part of GenomeAnnotation.
 * * Any of load_genes, load_mrnas and load_cdss flags are additional to load_features_by_type list of types;
 * * By default load_genes=1, load_cdss=1, load_proteins=1, load_gene_id_to_cds_ids=1, load_summary=1.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "ref",
    "load_genes",
    "load_mrnas",
    "load_cdss",
    "load_features_by_type",
    "load_proteins",
    "load_gene_id_to_mrna_ids",
    "load_gene_id_to_cds_ids",
    "load_mrna_id_to_cds_id",
    "load_mrna_id_to_exons",
    "load_mrna_id_to_utr_type_to_utr",
    "load_summary"
})
public class GetGenomeDataParams {

    @JsonProperty("ref")
    private java.lang.String ref;
    @JsonProperty("load_genes")
    private Long loadGenes;
    @JsonProperty("load_mrnas")
    private Long loadMrnas;
    @JsonProperty("load_cdss")
    private Long loadCdss;
    @JsonProperty("load_features_by_type")
    private List<String> loadFeaturesByType;
    @JsonProperty("load_proteins")
    private Long loadProteins;
    @JsonProperty("load_gene_id_to_mrna_ids")
    private Long loadGeneIdToMrnaIds;
    @JsonProperty("load_gene_id_to_cds_ids")
    private Long loadGeneIdToCdsIds;
    @JsonProperty("load_mrna_id_to_cds_id")
    private Long loadMrnaIdToCdsId;
    @JsonProperty("load_mrna_id_to_exons")
    private Long loadMrnaIdToExons;
    @JsonProperty("load_mrna_id_to_utr_type_to_utr")
    private Long loadMrnaIdToUtrTypeToUtr;
    @JsonProperty("load_summary")
    private Long loadSummary;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("ref")
    public java.lang.String getRef() {
        return ref;
    }

    @JsonProperty("ref")
    public void setRef(java.lang.String ref) {
        this.ref = ref;
    }

    public GetGenomeDataParams withRef(java.lang.String ref) {
        this.ref = ref;
        return this;
    }

    @JsonProperty("load_genes")
    public Long getLoadGenes() {
        return loadGenes;
    }

    @JsonProperty("load_genes")
    public void setLoadGenes(Long loadGenes) {
        this.loadGenes = loadGenes;
    }

    public GetGenomeDataParams withLoadGenes(Long loadGenes) {
        this.loadGenes = loadGenes;
        return this;
    }

    @JsonProperty("load_mrnas")
    public Long getLoadMrnas() {
        return loadMrnas;
    }

    @JsonProperty("load_mrnas")
    public void setLoadMrnas(Long loadMrnas) {
        this.loadMrnas = loadMrnas;
    }

    public GetGenomeDataParams withLoadMrnas(Long loadMrnas) {
        this.loadMrnas = loadMrnas;
        return this;
    }

    @JsonProperty("load_cdss")
    public Long getLoadCdss() {
        return loadCdss;
    }

    @JsonProperty("load_cdss")
    public void setLoadCdss(Long loadCdss) {
        this.loadCdss = loadCdss;
    }

    public GetGenomeDataParams withLoadCdss(Long loadCdss) {
        this.loadCdss = loadCdss;
        return this;
    }

    @JsonProperty("load_features_by_type")
    public List<String> getLoadFeaturesByType() {
        return loadFeaturesByType;
    }

    @JsonProperty("load_features_by_type")
    public void setLoadFeaturesByType(List<String> loadFeaturesByType) {
        this.loadFeaturesByType = loadFeaturesByType;
    }

    public GetGenomeDataParams withLoadFeaturesByType(List<String> loadFeaturesByType) {
        this.loadFeaturesByType = loadFeaturesByType;
        return this;
    }

    @JsonProperty("load_proteins")
    public Long getLoadProteins() {
        return loadProteins;
    }

    @JsonProperty("load_proteins")
    public void setLoadProteins(Long loadProteins) {
        this.loadProteins = loadProteins;
    }

    public GetGenomeDataParams withLoadProteins(Long loadProteins) {
        this.loadProteins = loadProteins;
        return this;
    }

    @JsonProperty("load_gene_id_to_mrna_ids")
    public Long getLoadGeneIdToMrnaIds() {
        return loadGeneIdToMrnaIds;
    }

    @JsonProperty("load_gene_id_to_mrna_ids")
    public void setLoadGeneIdToMrnaIds(Long loadGeneIdToMrnaIds) {
        this.loadGeneIdToMrnaIds = loadGeneIdToMrnaIds;
    }

    public GetGenomeDataParams withLoadGeneIdToMrnaIds(Long loadGeneIdToMrnaIds) {
        this.loadGeneIdToMrnaIds = loadGeneIdToMrnaIds;
        return this;
    }

    @JsonProperty("load_gene_id_to_cds_ids")
    public Long getLoadGeneIdToCdsIds() {
        return loadGeneIdToCdsIds;
    }

    @JsonProperty("load_gene_id_to_cds_ids")
    public void setLoadGeneIdToCdsIds(Long loadGeneIdToCdsIds) {
        this.loadGeneIdToCdsIds = loadGeneIdToCdsIds;
    }

    public GetGenomeDataParams withLoadGeneIdToCdsIds(Long loadGeneIdToCdsIds) {
        this.loadGeneIdToCdsIds = loadGeneIdToCdsIds;
        return this;
    }

    @JsonProperty("load_mrna_id_to_cds_id")
    public Long getLoadMrnaIdToCdsId() {
        return loadMrnaIdToCdsId;
    }

    @JsonProperty("load_mrna_id_to_cds_id")
    public void setLoadMrnaIdToCdsId(Long loadMrnaIdToCdsId) {
        this.loadMrnaIdToCdsId = loadMrnaIdToCdsId;
    }

    public GetGenomeDataParams withLoadMrnaIdToCdsId(Long loadMrnaIdToCdsId) {
        this.loadMrnaIdToCdsId = loadMrnaIdToCdsId;
        return this;
    }

    @JsonProperty("load_mrna_id_to_exons")
    public Long getLoadMrnaIdToExons() {
        return loadMrnaIdToExons;
    }

    @JsonProperty("load_mrna_id_to_exons")
    public void setLoadMrnaIdToExons(Long loadMrnaIdToExons) {
        this.loadMrnaIdToExons = loadMrnaIdToExons;
    }

    public GetGenomeDataParams withLoadMrnaIdToExons(Long loadMrnaIdToExons) {
        this.loadMrnaIdToExons = loadMrnaIdToExons;
        return this;
    }

    @JsonProperty("load_mrna_id_to_utr_type_to_utr")
    public Long getLoadMrnaIdToUtrTypeToUtr() {
        return loadMrnaIdToUtrTypeToUtr;
    }

    @JsonProperty("load_mrna_id_to_utr_type_to_utr")
    public void setLoadMrnaIdToUtrTypeToUtr(Long loadMrnaIdToUtrTypeToUtr) {
        this.loadMrnaIdToUtrTypeToUtr = loadMrnaIdToUtrTypeToUtr;
    }

    public GetGenomeDataParams withLoadMrnaIdToUtrTypeToUtr(Long loadMrnaIdToUtrTypeToUtr) {
        this.loadMrnaIdToUtrTypeToUtr = loadMrnaIdToUtrTypeToUtr;
        return this;
    }

    @JsonProperty("load_summary")
    public Long getLoadSummary() {
        return loadSummary;
    }

    @JsonProperty("load_summary")
    public void setLoadSummary(Long loadSummary) {
        this.loadSummary = loadSummary;
    }

    public GetGenomeDataParams withLoadSummary(Long loadSummary) {
        this.loadSummary = loadSummary;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((((((((((((((((((((((("GetGenomeDataParams"+" [ref=")+ ref)+", loadGenes=")+ loadGenes)+", loadMrnas=")+ loadMrnas)+", loadCdss=")+ loadCdss)+", loadFeaturesByType=")+ loadFeaturesByType)+", loadProteins=")+ loadProteins)+", loadGeneIdToMrnaIds=")+ loadGeneIdToMrnaIds)+", loadGeneIdToCdsIds=")+ loadGeneIdToCdsIds)+", loadMrnaIdToCdsId=")+ loadMrnaIdToCdsId)+", loadMrnaIdToExons=")+ loadMrnaIdToExons)+", loadMrnaIdToUtrTypeToUtr=")+ loadMrnaIdToUtrTypeToUtr)+", loadSummary=")+ loadSummary)+", additionalProperties=")+ additionalProperties)+"]");
    }

}

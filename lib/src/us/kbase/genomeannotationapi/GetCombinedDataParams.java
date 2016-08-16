
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
 * <p>Original spec-file type: GetCombinedDataParams</p>
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
    "load_protein_by_cds_id",
    "load_mrna_ids_by_gene_id",
    "load_cds_ids_by_gene_id",
    "load_cds_id_by_mrna_id",
    "load_exons_by_mrna_id",
    "load_utr_by_utr_type_by_mrna_id",
    "load_summary"
})
public class GetCombinedDataParams {

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
    @JsonProperty("load_protein_by_cds_id")
    private Long loadProteinByCdsId;
    @JsonProperty("load_mrna_ids_by_gene_id")
    private Long loadMrnaIdsByGeneId;
    @JsonProperty("load_cds_ids_by_gene_id")
    private Long loadCdsIdsByGeneId;
    @JsonProperty("load_cds_id_by_mrna_id")
    private Long loadCdsIdByMrnaId;
    @JsonProperty("load_exons_by_mrna_id")
    private Long loadExonsByMrnaId;
    @JsonProperty("load_utr_by_utr_type_by_mrna_id")
    private Long loadUtrByUtrTypeByMrnaId;
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

    public GetCombinedDataParams withRef(java.lang.String ref) {
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

    public GetCombinedDataParams withLoadGenes(Long loadGenes) {
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

    public GetCombinedDataParams withLoadMrnas(Long loadMrnas) {
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

    public GetCombinedDataParams withLoadCdss(Long loadCdss) {
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

    public GetCombinedDataParams withLoadFeaturesByType(List<String> loadFeaturesByType) {
        this.loadFeaturesByType = loadFeaturesByType;
        return this;
    }

    @JsonProperty("load_protein_by_cds_id")
    public Long getLoadProteinByCdsId() {
        return loadProteinByCdsId;
    }

    @JsonProperty("load_protein_by_cds_id")
    public void setLoadProteinByCdsId(Long loadProteinByCdsId) {
        this.loadProteinByCdsId = loadProteinByCdsId;
    }

    public GetCombinedDataParams withLoadProteinByCdsId(Long loadProteinByCdsId) {
        this.loadProteinByCdsId = loadProteinByCdsId;
        return this;
    }

    @JsonProperty("load_mrna_ids_by_gene_id")
    public Long getLoadMrnaIdsByGeneId() {
        return loadMrnaIdsByGeneId;
    }

    @JsonProperty("load_mrna_ids_by_gene_id")
    public void setLoadMrnaIdsByGeneId(Long loadMrnaIdsByGeneId) {
        this.loadMrnaIdsByGeneId = loadMrnaIdsByGeneId;
    }

    public GetCombinedDataParams withLoadMrnaIdsByGeneId(Long loadMrnaIdsByGeneId) {
        this.loadMrnaIdsByGeneId = loadMrnaIdsByGeneId;
        return this;
    }

    @JsonProperty("load_cds_ids_by_gene_id")
    public Long getLoadCdsIdsByGeneId() {
        return loadCdsIdsByGeneId;
    }

    @JsonProperty("load_cds_ids_by_gene_id")
    public void setLoadCdsIdsByGeneId(Long loadCdsIdsByGeneId) {
        this.loadCdsIdsByGeneId = loadCdsIdsByGeneId;
    }

    public GetCombinedDataParams withLoadCdsIdsByGeneId(Long loadCdsIdsByGeneId) {
        this.loadCdsIdsByGeneId = loadCdsIdsByGeneId;
        return this;
    }

    @JsonProperty("load_cds_id_by_mrna_id")
    public Long getLoadCdsIdByMrnaId() {
        return loadCdsIdByMrnaId;
    }

    @JsonProperty("load_cds_id_by_mrna_id")
    public void setLoadCdsIdByMrnaId(Long loadCdsIdByMrnaId) {
        this.loadCdsIdByMrnaId = loadCdsIdByMrnaId;
    }

    public GetCombinedDataParams withLoadCdsIdByMrnaId(Long loadCdsIdByMrnaId) {
        this.loadCdsIdByMrnaId = loadCdsIdByMrnaId;
        return this;
    }

    @JsonProperty("load_exons_by_mrna_id")
    public Long getLoadExonsByMrnaId() {
        return loadExonsByMrnaId;
    }

    @JsonProperty("load_exons_by_mrna_id")
    public void setLoadExonsByMrnaId(Long loadExonsByMrnaId) {
        this.loadExonsByMrnaId = loadExonsByMrnaId;
    }

    public GetCombinedDataParams withLoadExonsByMrnaId(Long loadExonsByMrnaId) {
        this.loadExonsByMrnaId = loadExonsByMrnaId;
        return this;
    }

    @JsonProperty("load_utr_by_utr_type_by_mrna_id")
    public Long getLoadUtrByUtrTypeByMrnaId() {
        return loadUtrByUtrTypeByMrnaId;
    }

    @JsonProperty("load_utr_by_utr_type_by_mrna_id")
    public void setLoadUtrByUtrTypeByMrnaId(Long loadUtrByUtrTypeByMrnaId) {
        this.loadUtrByUtrTypeByMrnaId = loadUtrByUtrTypeByMrnaId;
    }

    public GetCombinedDataParams withLoadUtrByUtrTypeByMrnaId(Long loadUtrByUtrTypeByMrnaId) {
        this.loadUtrByUtrTypeByMrnaId = loadUtrByUtrTypeByMrnaId;
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

    public GetCombinedDataParams withLoadSummary(Long loadSummary) {
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
        return ((((((((((((((((((((((((((("GetCombinedDataParams"+" [ref=")+ ref)+", loadGenes=")+ loadGenes)+", loadMrnas=")+ loadMrnas)+", loadCdss=")+ loadCdss)+", loadFeaturesByType=")+ loadFeaturesByType)+", loadProteinByCdsId=")+ loadProteinByCdsId)+", loadMrnaIdsByGeneId=")+ loadMrnaIdsByGeneId)+", loadCdsIdsByGeneId=")+ loadCdsIdsByGeneId)+", loadCdsIdByMrnaId=")+ loadCdsIdByMrnaId)+", loadExonsByMrnaId=")+ loadExonsByMrnaId)+", loadUtrByUtrTypeByMrnaId=")+ loadUtrByUtrTypeByMrnaId)+", loadSummary=")+ loadSummary)+", additionalProperties=")+ additionalProperties)+"]");
    }

}

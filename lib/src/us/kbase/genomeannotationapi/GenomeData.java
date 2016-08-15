
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
 * <p>Original spec-file type: Genome_data</p>
 * <pre>
 * gene_id is a feature id of a gene feature.
 * mrna_id is a feature id of a mrna feature.
 * cds_id is a feature id of a cds feature.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "gene_type",
    "mrna_type",
    "cds_type",
    "feature_types",
    "type_to_id_to_feature",
    "cds_id_to_protein",
    "gene_id_to_mrna_ids",
    "gene_id_to_cds_ids",
    "mrna_id_to_cds_id",
    "mrna_id_to_exons",
    "mrna_id_to_utr_type_to_utr",
    "summary"
})
public class GenomeData {

    @JsonProperty("gene_type")
    private java.lang.String geneType;
    @JsonProperty("mrna_type")
    private java.lang.String mrnaType;
    @JsonProperty("cds_type")
    private java.lang.String cdsType;
    @JsonProperty("feature_types")
    private List<String> featureTypes;
    @JsonProperty("type_to_id_to_feature")
    private Map<String, Map<String, FeatureData>> typeToIdToFeature;
    @JsonProperty("cds_id_to_protein")
    private Map<String, ProteinData> cdsIdToProtein;
    @JsonProperty("gene_id_to_mrna_ids")
    private Map<String, List<String>> geneIdToMrnaIds;
    @JsonProperty("gene_id_to_cds_ids")
    private Map<String, List<String>> geneIdToCdsIds;
    @JsonProperty("mrna_id_to_cds_id")
    private Map<String, String> mrnaIdToCdsId;
    @JsonProperty("mrna_id_to_exons")
    private Map<String, List<ExonData>> mrnaIdToExons;
    @JsonProperty("mrna_id_to_utr_type_to_utr")
    private Map<String, Map<String, UTRData>> mrnaIdToUtrTypeToUtr;
    /**
     * <p>Original spec-file type: Summary_data</p>
     * 
     * 
     */
    @JsonProperty("summary")
    private SummaryData summary;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("gene_type")
    public java.lang.String getGeneType() {
        return geneType;
    }

    @JsonProperty("gene_type")
    public void setGeneType(java.lang.String geneType) {
        this.geneType = geneType;
    }

    public GenomeData withGeneType(java.lang.String geneType) {
        this.geneType = geneType;
        return this;
    }

    @JsonProperty("mrna_type")
    public java.lang.String getMrnaType() {
        return mrnaType;
    }

    @JsonProperty("mrna_type")
    public void setMrnaType(java.lang.String mrnaType) {
        this.mrnaType = mrnaType;
    }

    public GenomeData withMrnaType(java.lang.String mrnaType) {
        this.mrnaType = mrnaType;
        return this;
    }

    @JsonProperty("cds_type")
    public java.lang.String getCdsType() {
        return cdsType;
    }

    @JsonProperty("cds_type")
    public void setCdsType(java.lang.String cdsType) {
        this.cdsType = cdsType;
    }

    public GenomeData withCdsType(java.lang.String cdsType) {
        this.cdsType = cdsType;
        return this;
    }

    @JsonProperty("feature_types")
    public List<String> getFeatureTypes() {
        return featureTypes;
    }

    @JsonProperty("feature_types")
    public void setFeatureTypes(List<String> featureTypes) {
        this.featureTypes = featureTypes;
    }

    public GenomeData withFeatureTypes(List<String> featureTypes) {
        this.featureTypes = featureTypes;
        return this;
    }

    @JsonProperty("type_to_id_to_feature")
    public Map<String, Map<String, FeatureData>> getTypeToIdToFeature() {
        return typeToIdToFeature;
    }

    @JsonProperty("type_to_id_to_feature")
    public void setTypeToIdToFeature(Map<String, Map<String, FeatureData>> typeToIdToFeature) {
        this.typeToIdToFeature = typeToIdToFeature;
    }

    public GenomeData withTypeToIdToFeature(Map<String, Map<String, FeatureData>> typeToIdToFeature) {
        this.typeToIdToFeature = typeToIdToFeature;
        return this;
    }

    @JsonProperty("cds_id_to_protein")
    public Map<String, ProteinData> getCdsIdToProtein() {
        return cdsIdToProtein;
    }

    @JsonProperty("cds_id_to_protein")
    public void setCdsIdToProtein(Map<String, ProteinData> cdsIdToProtein) {
        this.cdsIdToProtein = cdsIdToProtein;
    }

    public GenomeData withCdsIdToProtein(Map<String, ProteinData> cdsIdToProtein) {
        this.cdsIdToProtein = cdsIdToProtein;
        return this;
    }

    @JsonProperty("gene_id_to_mrna_ids")
    public Map<String, List<String>> getGeneIdToMrnaIds() {
        return geneIdToMrnaIds;
    }

    @JsonProperty("gene_id_to_mrna_ids")
    public void setGeneIdToMrnaIds(Map<String, List<String>> geneIdToMrnaIds) {
        this.geneIdToMrnaIds = geneIdToMrnaIds;
    }

    public GenomeData withGeneIdToMrnaIds(Map<String, List<String>> geneIdToMrnaIds) {
        this.geneIdToMrnaIds = geneIdToMrnaIds;
        return this;
    }

    @JsonProperty("gene_id_to_cds_ids")
    public Map<String, List<String>> getGeneIdToCdsIds() {
        return geneIdToCdsIds;
    }

    @JsonProperty("gene_id_to_cds_ids")
    public void setGeneIdToCdsIds(Map<String, List<String>> geneIdToCdsIds) {
        this.geneIdToCdsIds = geneIdToCdsIds;
    }

    public GenomeData withGeneIdToCdsIds(Map<String, List<String>> geneIdToCdsIds) {
        this.geneIdToCdsIds = geneIdToCdsIds;
        return this;
    }

    @JsonProperty("mrna_id_to_cds_id")
    public Map<String, String> getMrnaIdToCdsId() {
        return mrnaIdToCdsId;
    }

    @JsonProperty("mrna_id_to_cds_id")
    public void setMrnaIdToCdsId(Map<String, String> mrnaIdToCdsId) {
        this.mrnaIdToCdsId = mrnaIdToCdsId;
    }

    public GenomeData withMrnaIdToCdsId(Map<String, String> mrnaIdToCdsId) {
        this.mrnaIdToCdsId = mrnaIdToCdsId;
        return this;
    }

    @JsonProperty("mrna_id_to_exons")
    public Map<String, List<ExonData>> getMrnaIdToExons() {
        return mrnaIdToExons;
    }

    @JsonProperty("mrna_id_to_exons")
    public void setMrnaIdToExons(Map<String, List<ExonData>> mrnaIdToExons) {
        this.mrnaIdToExons = mrnaIdToExons;
    }

    public GenomeData withMrnaIdToExons(Map<String, List<ExonData>> mrnaIdToExons) {
        this.mrnaIdToExons = mrnaIdToExons;
        return this;
    }

    @JsonProperty("mrna_id_to_utr_type_to_utr")
    public Map<String, Map<String, UTRData>> getMrnaIdToUtrTypeToUtr() {
        return mrnaIdToUtrTypeToUtr;
    }

    @JsonProperty("mrna_id_to_utr_type_to_utr")
    public void setMrnaIdToUtrTypeToUtr(Map<String, Map<String, UTRData>> mrnaIdToUtrTypeToUtr) {
        this.mrnaIdToUtrTypeToUtr = mrnaIdToUtrTypeToUtr;
    }

    public GenomeData withMrnaIdToUtrTypeToUtr(Map<String, Map<String, UTRData>> mrnaIdToUtrTypeToUtr) {
        this.mrnaIdToUtrTypeToUtr = mrnaIdToUtrTypeToUtr;
        return this;
    }

    /**
     * <p>Original spec-file type: Summary_data</p>
     * 
     * 
     */
    @JsonProperty("summary")
    public SummaryData getSummary() {
        return summary;
    }

    /**
     * <p>Original spec-file type: Summary_data</p>
     * 
     * 
     */
    @JsonProperty("summary")
    public void setSummary(SummaryData summary) {
        this.summary = summary;
    }

    public GenomeData withSummary(SummaryData summary) {
        this.summary = summary;
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
        return ((((((((((((((((((((((((((("GenomeData"+" [geneType=")+ geneType)+", mrnaType=")+ mrnaType)+", cdsType=")+ cdsType)+", featureTypes=")+ featureTypes)+", typeToIdToFeature=")+ typeToIdToFeature)+", cdsIdToProtein=")+ cdsIdToProtein)+", geneIdToMrnaIds=")+ geneIdToMrnaIds)+", geneIdToCdsIds=")+ geneIdToCdsIds)+", mrnaIdToCdsId=")+ mrnaIdToCdsId)+", mrnaIdToExons=")+ mrnaIdToExons)+", mrnaIdToUtrTypeToUtr=")+ mrnaIdToUtrTypeToUtr)+", summary=")+ summary)+", additionalProperties=")+ additionalProperties)+"]");
    }

}


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
 * <p>Original spec-file type: LegacyGenomeSelector</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "ref",
    "included",
    "ref_path_to_genome"
})
public class LegacyGenomeSelector {

    @JsonProperty("ref")
    private java.lang.String ref;
    @JsonProperty("included")
    private List<String> included;
    @JsonProperty("ref_path_to_genome")
    private List<String> refPathToGenome;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("ref")
    public java.lang.String getRef() {
        return ref;
    }

    @JsonProperty("ref")
    public void setRef(java.lang.String ref) {
        this.ref = ref;
    }

    public LegacyGenomeSelector withRef(java.lang.String ref) {
        this.ref = ref;
        return this;
    }

    @JsonProperty("included")
    public List<String> getIncluded() {
        return included;
    }

    @JsonProperty("included")
    public void setIncluded(List<String> included) {
        this.included = included;
    }

    public LegacyGenomeSelector withIncluded(List<String> included) {
        this.included = included;
        return this;
    }

    @JsonProperty("ref_path_to_genome")
    public List<String> getRefPathToGenome() {
        return refPathToGenome;
    }

    @JsonProperty("ref_path_to_genome")
    public void setRefPathToGenome(List<String> refPathToGenome) {
        this.refPathToGenome = refPathToGenome;
    }

    public LegacyGenomeSelector withRefPathToGenome(List<String> refPathToGenome) {
        this.refPathToGenome = refPathToGenome;
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
        return ((((((((("LegacyGenomeSelector"+" [ref=")+ ref)+", included=")+ included)+", refPathToGenome=")+ refPathToGenome)+", additionalProperties=")+ additionalProperties)+"]");
    }

}

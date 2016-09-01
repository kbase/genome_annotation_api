
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
 * <p>Original spec-file type: LegacyGenomeDataSet</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "genomes"
})
public class LegacyGenomeDataSet {

    @JsonProperty("genomes")
    private List<LegacyGenomeData> genomes;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("genomes")
    public List<LegacyGenomeData> getGenomes() {
        return genomes;
    }

    @JsonProperty("genomes")
    public void setGenomes(List<LegacyGenomeData> genomes) {
        this.genomes = genomes;
    }

    public LegacyGenomeDataSet withGenomes(List<LegacyGenomeData> genomes) {
        this.genomes = genomes;
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
        return ((((("LegacyGenomeDataSet"+" [genomes=")+ genomes)+", additionalProperties=")+ additionalProperties)+"]");
    }

}

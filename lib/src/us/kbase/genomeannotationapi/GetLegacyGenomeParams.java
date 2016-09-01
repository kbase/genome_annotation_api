
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
 * <p>Original spec-file type: GetLegacyGenomeParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "genomes",
    "ignore_errors",
    "no_data"
})
public class GetLegacyGenomeParams {

    @JsonProperty("genomes")
    private List<LegacyGenomeSelector> genomes;
    @JsonProperty("ignore_errors")
    private Long ignoreErrors;
    @JsonProperty("no_data")
    private Long noData;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("genomes")
    public List<LegacyGenomeSelector> getGenomes() {
        return genomes;
    }

    @JsonProperty("genomes")
    public void setGenomes(List<LegacyGenomeSelector> genomes) {
        this.genomes = genomes;
    }

    public GetLegacyGenomeParams withGenomes(List<LegacyGenomeSelector> genomes) {
        this.genomes = genomes;
        return this;
    }

    @JsonProperty("ignore_errors")
    public Long getIgnoreErrors() {
        return ignoreErrors;
    }

    @JsonProperty("ignore_errors")
    public void setIgnoreErrors(Long ignoreErrors) {
        this.ignoreErrors = ignoreErrors;
    }

    public GetLegacyGenomeParams withIgnoreErrors(Long ignoreErrors) {
        this.ignoreErrors = ignoreErrors;
        return this;
    }

    @JsonProperty("no_data")
    public Long getNoData() {
        return noData;
    }

    @JsonProperty("no_data")
    public void setNoData(Long noData) {
        this.noData = noData;
    }

    public GetLegacyGenomeParams withNoData(Long noData) {
        this.noData = noData;
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
        return ((((((((("GetLegacyGenomeParams"+" [genomes=")+ genomes)+", ignoreErrors=")+ ignoreErrors)+", noData=")+ noData)+", additionalProperties=")+ additionalProperties)+"]");
    }

}

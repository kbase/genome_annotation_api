
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
import us.kbase.common.service.Tuple11;


/**
 * <p>Original spec-file type: SaveLegacyGenomeResult</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "info"
})
public class SaveLegacyGenomeResult {

    @JsonProperty("info")
    private List<Tuple11 <Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>>> info;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("info")
    public List<Tuple11 <Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>>> getInfo() {
        return info;
    }

    @JsonProperty("info")
    public void setInfo(List<Tuple11 <Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>>> info) {
        this.info = info;
    }

    public SaveLegacyGenomeResult withInfo(List<Tuple11 <Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>>> info) {
        this.info = info;
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
        return ((((("SaveLegacyGenomeResult"+" [info=")+ info)+", additionalProperties=")+ additionalProperties)+"]");
    }

}

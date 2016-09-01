
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
 * <p>Original spec-file type: SaveLegacyGenomeParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace",
    "name",
    "genomes"
})
public class SaveLegacyGenomeParams {

    @JsonProperty("workspace")
    private String workspace;
    @JsonProperty("name")
    private String name;
    @JsonProperty("genomes")
    private List<LegacyGenomeSaveData> genomes;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace")
    public String getWorkspace() {
        return workspace;
    }

    @JsonProperty("workspace")
    public void setWorkspace(String workspace) {
        this.workspace = workspace;
    }

    public SaveLegacyGenomeParams withWorkspace(String workspace) {
        this.workspace = workspace;
        return this;
    }

    @JsonProperty("name")
    public String getName() {
        return name;
    }

    @JsonProperty("name")
    public void setName(String name) {
        this.name = name;
    }

    public SaveLegacyGenomeParams withName(String name) {
        this.name = name;
        return this;
    }

    @JsonProperty("genomes")
    public List<LegacyGenomeSaveData> getGenomes() {
        return genomes;
    }

    @JsonProperty("genomes")
    public void setGenomes(List<LegacyGenomeSaveData> genomes) {
        this.genomes = genomes;
    }

    public SaveLegacyGenomeParams withGenomes(List<LegacyGenomeSaveData> genomes) {
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
        return ((((((((("SaveLegacyGenomeParams"+" [workspace=")+ workspace)+", name=")+ name)+", genomes=")+ genomes)+", additionalProperties=")+ additionalProperties)+"]");
    }

}

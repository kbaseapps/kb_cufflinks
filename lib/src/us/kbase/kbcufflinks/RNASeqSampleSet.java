
package us.kbase.kbcufflinks;

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
 * <p>Original spec-file type: RNASeqSampleSet</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "sampleset_id",
    "sampleset_desc",
    "domain",
    "platform",
    "num_samples",
    "num_replicates",
    "sample_ids",
    "condition",
    "source",
    "Library_type",
    "publication_Id",
    "external_source_date"
})
public class RNASeqSampleSet {

    @JsonProperty("sampleset_id")
    private java.lang.String samplesetId;
    @JsonProperty("sampleset_desc")
    private java.lang.String samplesetDesc;
    @JsonProperty("domain")
    private java.lang.String domain;
    @JsonProperty("platform")
    private java.lang.String platform;
    @JsonProperty("num_samples")
    private Long numSamples;
    @JsonProperty("num_replicates")
    private Long numReplicates;
    @JsonProperty("sample_ids")
    private List<String> sampleIds;
    @JsonProperty("condition")
    private List<String> condition;
    @JsonProperty("source")
    private java.lang.String source;
    @JsonProperty("Library_type")
    private java.lang.String LibraryType;
    @JsonProperty("publication_Id")
    private java.lang.String publicationId;
    @JsonProperty("external_source_date")
    private java.lang.String externalSourceDate;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("sampleset_id")
    public java.lang.String getSamplesetId() {
        return samplesetId;
    }

    @JsonProperty("sampleset_id")
    public void setSamplesetId(java.lang.String samplesetId) {
        this.samplesetId = samplesetId;
    }

    public RNASeqSampleSet withSamplesetId(java.lang.String samplesetId) {
        this.samplesetId = samplesetId;
        return this;
    }

    @JsonProperty("sampleset_desc")
    public java.lang.String getSamplesetDesc() {
        return samplesetDesc;
    }

    @JsonProperty("sampleset_desc")
    public void setSamplesetDesc(java.lang.String samplesetDesc) {
        this.samplesetDesc = samplesetDesc;
    }

    public RNASeqSampleSet withSamplesetDesc(java.lang.String samplesetDesc) {
        this.samplesetDesc = samplesetDesc;
        return this;
    }

    @JsonProperty("domain")
    public java.lang.String getDomain() {
        return domain;
    }

    @JsonProperty("domain")
    public void setDomain(java.lang.String domain) {
        this.domain = domain;
    }

    public RNASeqSampleSet withDomain(java.lang.String domain) {
        this.domain = domain;
        return this;
    }

    @JsonProperty("platform")
    public java.lang.String getPlatform() {
        return platform;
    }

    @JsonProperty("platform")
    public void setPlatform(java.lang.String platform) {
        this.platform = platform;
    }

    public RNASeqSampleSet withPlatform(java.lang.String platform) {
        this.platform = platform;
        return this;
    }

    @JsonProperty("num_samples")
    public Long getNumSamples() {
        return numSamples;
    }

    @JsonProperty("num_samples")
    public void setNumSamples(Long numSamples) {
        this.numSamples = numSamples;
    }

    public RNASeqSampleSet withNumSamples(Long numSamples) {
        this.numSamples = numSamples;
        return this;
    }

    @JsonProperty("num_replicates")
    public Long getNumReplicates() {
        return numReplicates;
    }

    @JsonProperty("num_replicates")
    public void setNumReplicates(Long numReplicates) {
        this.numReplicates = numReplicates;
    }

    public RNASeqSampleSet withNumReplicates(Long numReplicates) {
        this.numReplicates = numReplicates;
        return this;
    }

    @JsonProperty("sample_ids")
    public List<String> getSampleIds() {
        return sampleIds;
    }

    @JsonProperty("sample_ids")
    public void setSampleIds(List<String> sampleIds) {
        this.sampleIds = sampleIds;
    }

    public RNASeqSampleSet withSampleIds(List<String> sampleIds) {
        this.sampleIds = sampleIds;
        return this;
    }

    @JsonProperty("condition")
    public List<String> getCondition() {
        return condition;
    }

    @JsonProperty("condition")
    public void setCondition(List<String> condition) {
        this.condition = condition;
    }

    public RNASeqSampleSet withCondition(List<String> condition) {
        this.condition = condition;
        return this;
    }

    @JsonProperty("source")
    public java.lang.String getSource() {
        return source;
    }

    @JsonProperty("source")
    public void setSource(java.lang.String source) {
        this.source = source;
    }

    public RNASeqSampleSet withSource(java.lang.String source) {
        this.source = source;
        return this;
    }

    @JsonProperty("Library_type")
    public java.lang.String getLibraryType() {
        return LibraryType;
    }

    @JsonProperty("Library_type")
    public void setLibraryType(java.lang.String LibraryType) {
        this.LibraryType = LibraryType;
    }

    public RNASeqSampleSet withLibraryType(java.lang.String LibraryType) {
        this.LibraryType = LibraryType;
        return this;
    }

    @JsonProperty("publication_Id")
    public java.lang.String getPublicationId() {
        return publicationId;
    }

    @JsonProperty("publication_Id")
    public void setPublicationId(java.lang.String publicationId) {
        this.publicationId = publicationId;
    }

    public RNASeqSampleSet withPublicationId(java.lang.String publicationId) {
        this.publicationId = publicationId;
        return this;
    }

    @JsonProperty("external_source_date")
    public java.lang.String getExternalSourceDate() {
        return externalSourceDate;
    }

    @JsonProperty("external_source_date")
    public void setExternalSourceDate(java.lang.String externalSourceDate) {
        this.externalSourceDate = externalSourceDate;
    }

    public RNASeqSampleSet withExternalSourceDate(java.lang.String externalSourceDate) {
        this.externalSourceDate = externalSourceDate;
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
        return ((((((((((((((((((((((((((("RNASeqSampleSet"+" [samplesetId=")+ samplesetId)+", samplesetDesc=")+ samplesetDesc)+", domain=")+ domain)+", platform=")+ platform)+", numSamples=")+ numSamples)+", numReplicates=")+ numReplicates)+", sampleIds=")+ sampleIds)+", condition=")+ condition)+", source=")+ source)+", LibraryType=")+ LibraryType)+", publicationId=")+ publicationId)+", externalSourceDate=")+ externalSourceDate)+", additionalProperties=")+ additionalProperties)+"]");
    }

}

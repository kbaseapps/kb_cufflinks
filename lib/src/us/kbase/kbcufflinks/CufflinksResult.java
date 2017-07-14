
package us.kbase.kbcufflinks;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: CufflinksResult</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "result_directory",
    "expression_obj_ref",
    "report_name",
    "report_ref"
})
public class CufflinksResult {

    @JsonProperty("result_directory")
    private String resultDirectory;
    @JsonProperty("expression_obj_ref")
    private String expressionObjRef;
    @JsonProperty("report_name")
    private String reportName;
    @JsonProperty("report_ref")
    private String reportRef;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("result_directory")
    public String getResultDirectory() {
        return resultDirectory;
    }

    @JsonProperty("result_directory")
    public void setResultDirectory(String resultDirectory) {
        this.resultDirectory = resultDirectory;
    }

    public CufflinksResult withResultDirectory(String resultDirectory) {
        this.resultDirectory = resultDirectory;
        return this;
    }

    @JsonProperty("expression_obj_ref")
    public String getExpressionObjRef() {
        return expressionObjRef;
    }

    @JsonProperty("expression_obj_ref")
    public void setExpressionObjRef(String expressionObjRef) {
        this.expressionObjRef = expressionObjRef;
    }

    public CufflinksResult withExpressionObjRef(String expressionObjRef) {
        this.expressionObjRef = expressionObjRef;
        return this;
    }

    @JsonProperty("report_name")
    public String getReportName() {
        return reportName;
    }

    @JsonProperty("report_name")
    public void setReportName(String reportName) {
        this.reportName = reportName;
    }

    public CufflinksResult withReportName(String reportName) {
        this.reportName = reportName;
        return this;
    }

    @JsonProperty("report_ref")
    public String getReportRef() {
        return reportRef;
    }

    @JsonProperty("report_ref")
    public void setReportRef(String reportRef) {
        this.reportRef = reportRef;
    }

    public CufflinksResult withReportRef(String reportRef) {
        this.reportRef = reportRef;
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
        return ((((((((((("CufflinksResult"+" [resultDirectory=")+ resultDirectory)+", expressionObjRef=")+ expressionObjRef)+", reportName=")+ reportName)+", reportRef=")+ reportRef)+", additionalProperties=")+ additionalProperties)+"]");
    }

}

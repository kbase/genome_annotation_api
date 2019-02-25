package us.kbase.genomeannotationapi;

import com.fasterxml.jackson.core.type.TypeReference;
import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import us.kbase.auth.AuthToken;
import us.kbase.common.service.JsonClientCaller;
import us.kbase.common.service.JsonClientException;
import us.kbase.common.service.RpcContext;
import us.kbase.common.service.UnauthorizedException;

/**
 * <p>Original spec-file module name: GenomeAnnotationAPI</p>
 * <pre>
 * </pre>
 */
public class GenomeAnnotationAPIClient {
    private JsonClientCaller caller;
    private String serviceVersion = null;


    /** Constructs a client with a custom URL and no user credentials.
     * @param url the URL of the service.
     */
    public GenomeAnnotationAPIClient(URL url) {
        caller = new JsonClientCaller(url);
    }
    /** Constructs a client with a custom URL.
     * @param url the URL of the service.
     * @param token the user's authorization token.
     * @throws UnauthorizedException if the token is not valid.
     * @throws IOException if an IOException occurs when checking the token's
     * validity.
     */
    public GenomeAnnotationAPIClient(URL url, AuthToken token) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, token);
    }

    /** Constructs a client with a custom URL.
     * @param url the URL of the service.
     * @param user the user name.
     * @param password the password for the user name.
     * @throws UnauthorizedException if the credentials are not valid.
     * @throws IOException if an IOException occurs when checking the user's
     * credentials.
     */
    public GenomeAnnotationAPIClient(URL url, String user, String password) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, user, password);
    }

    /** Constructs a client with a custom URL
     * and a custom authorization service URL.
     * @param url the URL of the service.
     * @param user the user name.
     * @param password the password for the user name.
     * @param auth the URL of the authorization server.
     * @throws UnauthorizedException if the credentials are not valid.
     * @throws IOException if an IOException occurs when checking the user's
     * credentials.
     */
    public GenomeAnnotationAPIClient(URL url, String user, String password, URL auth) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, user, password, auth);
    }

    /** Get the token this client uses to communicate with the server.
     * @return the authorization token.
     */
    public AuthToken getToken() {
        return caller.getToken();
    }

    /** Get the URL of the service with which this client communicates.
     * @return the service URL.
     */
    public URL getURL() {
        return caller.getURL();
    }

    /** Set the timeout between establishing a connection to a server and
     * receiving a response. A value of zero or null implies no timeout.
     * @param milliseconds the milliseconds to wait before timing out when
     * attempting to read from a server.
     */
    public void setConnectionReadTimeOut(Integer milliseconds) {
        this.caller.setConnectionReadTimeOut(milliseconds);
    }

    /** Check if this client allows insecure http (vs https) connections.
     * @return true if insecure connections are allowed.
     */
    public boolean isInsecureHttpConnectionAllowed() {
        return caller.isInsecureHttpConnectionAllowed();
    }

    /** Deprecated. Use isInsecureHttpConnectionAllowed().
     * @deprecated
     */
    public boolean isAuthAllowedForHttp() {
        return caller.isAuthAllowedForHttp();
    }

    /** Set whether insecure http (vs https) connections should be allowed by
     * this client.
     * @param allowed true to allow insecure connections. Default false
     */
    public void setIsInsecureHttpConnectionAllowed(boolean allowed) {
        caller.setInsecureHttpConnectionAllowed(allowed);
    }

    /** Deprecated. Use setIsInsecureHttpConnectionAllowed().
     * @deprecated
     */
    public void setAuthAllowedForHttp(boolean isAuthAllowedForHttp) {
        caller.setAuthAllowedForHttp(isAuthAllowedForHttp);
    }

    /** Set whether all SSL certificates, including self-signed certificates,
     * should be trusted.
     * @param trustAll true to trust all certificates. Default false.
     */
    public void setAllSSLCertificatesTrusted(final boolean trustAll) {
        caller.setAllSSLCertificatesTrusted(trustAll);
    }
    
    /** Check if this client trusts all SSL certificates, including
     * self-signed certificates.
     * @return true if all certificates are trusted.
     */
    public boolean isAllSSLCertificatesTrusted() {
        return caller.isAllSSLCertificatesTrusted();
    }
    /** Sets streaming mode on. In this case, the data will be streamed to
     * the server in chunks as it is read from disk rather than buffered in
     * memory. Many servers are not compatible with this feature.
     * @param streamRequest true to set streaming mode on, false otherwise.
     */
    public void setStreamingModeOn(boolean streamRequest) {
        caller.setStreamingModeOn(streamRequest);
    }

    /** Returns true if streaming mode is on.
     * @return true if streaming mode is on.
     */
    public boolean isStreamingModeOn() {
        return caller.isStreamingModeOn();
    }

    public void _setFileForNextRpcResponse(File f) {
        caller.setFileForNextRpcResponse(f);
    }

    public String getServiceVersion() {
        return this.serviceVersion;
    }

    public void setServiceVersion(String newValue) {
        this.serviceVersion = newValue;
    }

    /**
     * <p>Original spec-file function name: get_taxon</p>
     * <pre>
     * </pre>
     * @param   arg1   instance of type {@link us.kbase.genomeannotationapi.InputsGetTaxon InputsGetTaxon} (original type "inputs_get_taxon")
     * @return   instance of original type "ObjectReference"
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public String getTaxon(InputsGetTaxon arg1, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(arg1);
        TypeReference<List<String>> retType = new TypeReference<List<String>>() {};
        List<String> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_taxon", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_assembly</p>
     * <pre>
     * </pre>
     * @param   arg1   instance of type {@link us.kbase.genomeannotationapi.InputsGetAssembly InputsGetAssembly} (original type "inputs_get_assembly")
     * @return   instance of original type "ObjectReference"
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public String getAssembly(InputsGetAssembly arg1, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(arg1);
        TypeReference<List<String>> retType = new TypeReference<List<String>>() {};
        List<String> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_assembly", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_feature_types</p>
     * <pre>
     * </pre>
     * @param   arg1   instance of type {@link us.kbase.genomeannotationapi.InputsGetFeatureTypes InputsGetFeatureTypes} (original type "inputs_get_feature_types")
     * @return   instance of list of String
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public List<String> getFeatureTypes(InputsGetFeatureTypes arg1, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(arg1);
        TypeReference<List<List<String>>> retType = new TypeReference<List<List<String>>>() {};
        List<List<String>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_feature_types", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_feature_type_descriptions</p>
     * <pre>
     * </pre>
     * @param   arg1   instance of type {@link us.kbase.genomeannotationapi.InputsGetFeatureTypeDescriptions InputsGetFeatureTypeDescriptions} (original type "inputs_get_feature_type_descriptions")
     * @return   instance of mapping from String to String
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,String> getFeatureTypeDescriptions(InputsGetFeatureTypeDescriptions arg1, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(arg1);
        TypeReference<List<Map<String,String>>> retType = new TypeReference<List<Map<String,String>>>() {};
        List<Map<String,String>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_feature_type_descriptions", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_feature_type_counts</p>
     * <pre>
     * </pre>
     * @param   arg1   instance of type {@link us.kbase.genomeannotationapi.InputsGetFeatureTypeCounts InputsGetFeatureTypeCounts} (original type "inputs_get_feature_type_counts")
     * @return   instance of mapping from String to Long
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,Long> getFeatureTypeCounts(InputsGetFeatureTypeCounts arg1, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(arg1);
        TypeReference<List<Map<String,Long>>> retType = new TypeReference<List<Map<String,Long>>>() {};
        List<Map<String,Long>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_feature_type_counts", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_proteins</p>
     * <pre>
     * </pre>
     * @param   arg1   instance of type {@link us.kbase.genomeannotationapi.InputsGetProteins InputsGetProteins} (original type "inputs_get_proteins")
     * @return   instance of mapping from String to type {@link us.kbase.genomeannotationapi.ProteinData ProteinData} (original type "Protein_data")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,ProteinData> getProteins(InputsGetProteins arg1, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(arg1);
        TypeReference<List<Map<String,ProteinData>>> retType = new TypeReference<List<Map<String,ProteinData>>>() {};
        List<Map<String,ProteinData>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_proteins", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_feature_locations</p>
     * <pre>
     * </pre>
     * @param   arg1   instance of type {@link us.kbase.genomeannotationapi.InputsGetFeatureLocations InputsGetFeatureLocations} (original type "inputs_get_feature_locations")
     * @return   instance of mapping from String to list of type {@link us.kbase.genomeannotationapi.Region Region}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,List<Region>> getFeatureLocations(InputsGetFeatureLocations arg1, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(arg1);
        TypeReference<List<Map<String,List<Region>>>> retType = new TypeReference<List<Map<String,List<Region>>>>() {};
        List<Map<String,List<Region>>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_feature_locations", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_feature_dna</p>
     * <pre>
     * </pre>
     * @param   arg1   instance of type {@link us.kbase.genomeannotationapi.InputsGetFeatureDna InputsGetFeatureDna} (original type "inputs_get_feature_dna")
     * @return   instance of mapping from String to String
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,String> getFeatureDna(InputsGetFeatureDna arg1, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(arg1);
        TypeReference<List<Map<String,String>>> retType = new TypeReference<List<Map<String,String>>>() {};
        List<Map<String,String>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_feature_dna", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_feature_functions</p>
     * <pre>
     * </pre>
     * @param   arg1   instance of type {@link us.kbase.genomeannotationapi.InputsGetFeatureFunctions InputsGetFeatureFunctions} (original type "inputs_get_feature_functions")
     * @return   instance of mapping from String to String
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,String> getFeatureFunctions(InputsGetFeatureFunctions arg1, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(arg1);
        TypeReference<List<Map<String,String>>> retType = new TypeReference<List<Map<String,String>>>() {};
        List<Map<String,String>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_feature_functions", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_feature_aliases</p>
     * <pre>
     * </pre>
     * @param   arg1   instance of type {@link us.kbase.genomeannotationapi.InputsGetFeatureAliases InputsGetFeatureAliases} (original type "inputs_get_feature_aliases")
     * @return   instance of mapping from String to list of String
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,List<String>> getFeatureAliases(InputsGetFeatureAliases arg1, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(arg1);
        TypeReference<List<Map<String,List<String>>>> retType = new TypeReference<List<Map<String,List<String>>>>() {};
        List<Map<String,List<String>>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_feature_aliases", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_genome_v1</p>
     * <pre>
     * A reasonably simple wrapper on get_objects2, but with Genome specific
     * filters instead of arbitrary get subdata included paths.
     * </pre>
     * @param   params   instance of type {@link us.kbase.genomeannotationapi.GetGenomeParamsV1 GetGenomeParamsV1}
     * @return   parameter "data" of type {@link us.kbase.genomeannotationapi.GenomeDataSetV1 GenomeDataSetV1}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public GenomeDataSetV1 getGenomeV1(GetGenomeParamsV1 params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<GenomeDataSetV1>> retType = new TypeReference<List<GenomeDataSetV1>>() {};
        List<GenomeDataSetV1> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_genome_v1", args, retType, true, false, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: save_one_genome_v1</p>
     * <pre>
     * @deprecated: GenomeFileUtil.save_one_genome
     * </pre>
     * @param   params   instance of type {@link us.kbase.genomeannotationapi.SaveOneGenomeParamsV1 SaveOneGenomeParamsV1}
     * @return   parameter "result" of type {@link us.kbase.genomeannotationapi.SaveGenomeResultV1 SaveGenomeResultV1}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public SaveGenomeResultV1 saveOneGenomeV1(SaveOneGenomeParamsV1 params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<SaveGenomeResultV1>> retType = new TypeReference<List<SaveGenomeResultV1>>() {};
        List<SaveGenomeResultV1> res = caller.jsonrpcCall("GenomeAnnotationAPI.save_one_genome_v1", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    public Map<String, Object> status(RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        TypeReference<List<Map<String, Object>>> retType = new TypeReference<List<Map<String, Object>>>() {};
        List<Map<String, Object>> res = caller.jsonrpcCall("GenomeAnnotationAPI.status", args, retType, true, false, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }
}

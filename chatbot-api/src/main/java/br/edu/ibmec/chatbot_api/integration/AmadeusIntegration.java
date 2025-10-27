package br.edu.ibmec.chatbot_api.integration;

import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

public class AmadeusIntegration {
    private static final String BASE_URL = "https://test.api.amadeus.com/";
    private static final String TOKEN_URL = BASE_URL + "v1/security/oauth2/token";

    //Obtido no site do Amadeus for Developers
    private String clientId = "ah7RWCEoRe1Aoa7fWiMhAUxRVunicqco";
    private String clientSecret = "e6NVm3boYPtUC0lv";

    //Variavel que armazenará o token de acesso obtido após a autenticação
    private String accessToken;

    //Variaveis para requisições HTTP e manipulação de JSON
    private final HttpClient httpClient;
    private final ObjectMapper objectMapper;

    public AmadeusIntegration() {
        this.httpClient = HttpClient.newHttpClient();
        this.objectMapper = new ObjectMapper();
    }

    // Obter o token de acesso
    public void authenticate() throws Exception {
        String body = "grant_type=client_credentials&client_id=" + clientId 
                      + "&client_secret=" + clientSecret;

        HttpRequest request = HttpRequest.newBuilder()
                .uri(new java.net.URI(TOKEN_URL))
                .header("Content-Type", "application/x-www-form-urlencoded")
                .POST(HttpRequest.BodyPublishers.ofString(body))
                .build();

        var response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        JsonNode jsonResponse = objectMapper.readTree(response.body());

        if (response.statusCode() != 200) {
            throw new Exception("Failed to authenticate with Amadeus API: " + jsonResponse.toString());
        }

        this.accessToken = jsonResponse.get("access_token").asText();
        System.out.println("Access Token: " + this.accessToken);

    }

    public String searchHotelByCity(String cityCode) throws Exception {
        if (accessToken == null) 
            this.authenticate();
        
        String url = BASE_URL + "v1/reference-data/locations/hotels/by-city?cityCode=" + cityCode;

        HttpRequest request = HttpRequest.newBuilder()
                .uri(new java.net.URI(url))
                .header("Authorization", "Bearer " + accessToken)
                .GET()
                .build();
        var response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        
        return response.body();
    }

    public String searchCityByName(String cityName, int limit) throws Exception {
        if (accessToken == null) 
            this.authenticate();
        
        String url = BASE_URL + "v1/reference-data/locations?subType=CITY&keyword=" + cityName
                              + "&view=LIGHT"
                              + "&page[limit]=" + limit;

        HttpRequest request = HttpRequest.newBuilder()
                .uri(new java.net.URI(url))
                .header("Authorization", "Bearer " + accessToken)
                .GET()
                .build();
        var response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        
        return response.body();
    }

    public String searchHotelOffers(String cityCode) throws Exception {
        if (accessToken == null) 
            this.authenticate();
        
        String url = BASE_URL + "v2/shopping/hotel-offers?cityCode=" + cityCode;

        HttpRequest request = HttpRequest.newBuilder()
                .uri(new java.net.URI(url))
                .header("Authorization", "Bearer " + accessToken)
                .GET()
                .build();
                
        var response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        
        return response.body();
    }


}

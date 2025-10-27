package br.edu.ibmec.chatbot_api.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.azure.core.annotation.PathParam;

import br.edu.ibmec.chatbot_api.integration.AmadeusIntegration;

@RestController
@RequestMapping("/hotels")
public class HotelController {

    @GetMapping("searchByCity")
    public ResponseEntity<String> searchHotelsByCity(@RequestParam String destinationCity) throws Exception {
        AmadeusIntegration amadeusIntegration = new AmadeusIntegration();
        return ResponseEntity.ok(amadeusIntegration.searchCityByName(destinationCity, 10));
    }

    @GetMapping("searchHotelsByCityCode")
    public ResponseEntity<String> searchHotelsByCityCode(@RequestParam String cityCode) throws Exception {
        AmadeusIntegration amadeusIntegration = new AmadeusIntegration();
        return ResponseEntity.ok(amadeusIntegration.searchHotelByCity(cityCode));
    }

}

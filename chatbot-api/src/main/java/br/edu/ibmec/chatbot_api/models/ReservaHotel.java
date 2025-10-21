package br.edu.ibmec.chatbot_api.models;

import lombok.Data;

import java.time.LocalDate;

@Data
public class ReservaHotel {
    private String id;
    private String cidade;
    private String hotel;
    private LocalDate dataEntrada;
    private LocalDate dataSaida;
}
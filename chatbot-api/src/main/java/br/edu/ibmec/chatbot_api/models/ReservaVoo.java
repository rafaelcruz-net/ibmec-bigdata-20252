package br.edu.ibmec.chatbot_api.models;

import lombok.Data;

import java.time.LocalDate;

@Data
public class ReservaVoo {
    private String id;
    private String cidadeOrigem;
    private String cidadeDestino;
    private LocalDate data;
    private String horario;
    private String codigoVoo;
}
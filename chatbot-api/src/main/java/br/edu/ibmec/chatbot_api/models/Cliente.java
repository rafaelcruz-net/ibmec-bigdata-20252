package br.edu.ibmec.chatbot_api.models;

import java.util.List;

import lombok.Data;

@Data
public class Cliente {
    private Long id;

    private String nome;

    private String email;

    private String celular;

    private String cpf;

    private List<ReservaVoo> reservasVoo;

    private List<ReservaHotel> reservasHotel;
}
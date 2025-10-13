package br.edu.ibmec.chatbot_api.models;

import jakarta.persistence.*;
import lombok.Data;

@Data
@Entity
@Table(name = "opcoes_hoteis")
public class OpcoesHoteis {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String cidade;

    @Column(nullable = false)
    private String nome;
}
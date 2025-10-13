package br.edu.ibmec.chatbot_api.models;

import jakarta.persistence.*;
import lombok.Data;

@Data
@Entity
@Table(name = "opcoes_voos")
public class OpcoesVoos {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String codigo;

    @Column(nullable = false)
    private String origem;

    @Column(nullable = false)
    private String destino;

    @Column(nullable = false, columnDefinition = "TEXT")
    private String horarios;
}
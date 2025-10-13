package br.edu.ibmec.chatbot_api.models;

import jakarta.persistence.*;
import lombok.Data;

@Data
@Entity
@Table(name = "opcoes_cidades")
public class OpcoesCidades {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String nome;
}
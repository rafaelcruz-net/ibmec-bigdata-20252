package br.edu.ibmec.chatbot_api.models;

import jakarta.persistence.*;
import lombok.Data;

import java.time.LocalDate;

@Data
@Entity
@Table(name = "reservas_voo")
public class ReservaVoo {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(cascade = CascadeType.MERGE)
    @JoinColumn(name = "cliente_id", nullable = false)
    private Cliente cliente;

    @Column(name = "cidade_origem", nullable = false)
    private String cidadeOrigem;

    @Column(name = "cidade_destino", nullable = false)
    private String cidadeDestino;

    @Column(nullable = false)
    private LocalDate data;

    @Column(nullable = false)
    private String horario;

    @Column(name = "codigo_voo", nullable = false)
    private String codigoVoo;
}
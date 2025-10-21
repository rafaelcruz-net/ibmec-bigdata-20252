package br.edu.ibmec.chatbot_api.models;

import java.util.List;

import org.springframework.data.annotation.Id;

import com.azure.spring.data.cosmos.core.mapping.Container;
import com.azure.spring.data.cosmos.core.mapping.PartitionKey;

import lombok.Data;

@Data
@Container(containerName = "clientes")
public class Cliente {
    @Id
    private String id;

    @PartitionKey
    private String cpf;
    
    private String nome;
    private String email;
    private String celular;
    private List<ReservaVoo> reservasVoo;
    private List<ReservaHotel> reservasHotel;
}
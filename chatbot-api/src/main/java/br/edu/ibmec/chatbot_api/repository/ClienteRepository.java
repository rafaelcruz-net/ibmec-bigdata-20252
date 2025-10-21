package br.edu.ibmec.chatbot_api.repository;

import br.edu.ibmec.chatbot_api.models.Cliente;
import org.springframework.stereotype.Repository;

import com.azure.spring.data.cosmos.repository.CosmosRepository;

import java.util.Optional;

@Repository
public interface ClienteRepository extends CosmosRepository<Cliente, String> {
    Optional<Cliente> findByCpf(String cpf);
}
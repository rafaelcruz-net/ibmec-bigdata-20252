package br.edu.ibmec.chatbot_api.repository;

import br.edu.ibmec.chatbot_api.models.Cliente;
import br.edu.ibmec.chatbot_api.models.ReservaVoo;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ReservaVooRepository extends JpaRepository<ReservaVoo, Long> {
    List<ReservaVoo> findByClienteCpf(String cpf);

    List<ReservaVoo> findByCliente(Cliente cliente);
}
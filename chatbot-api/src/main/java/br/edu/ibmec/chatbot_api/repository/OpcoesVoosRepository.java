package br.edu.ibmec.chatbot_api.repository;

import br.edu.ibmec.chatbot_api.models.OpcoesVoos;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface OpcoesVoosRepository extends JpaRepository<OpcoesVoos, Long> {
    List<OpcoesVoos> findByOrigemAndDestino(String origem, String destino);
}
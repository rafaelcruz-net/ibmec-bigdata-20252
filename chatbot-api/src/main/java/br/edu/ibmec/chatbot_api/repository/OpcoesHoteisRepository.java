package br.edu.ibmec.chatbot_api.repository;

import br.edu.ibmec.chatbot_api.models.OpcoesHoteis;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface OpcoesHoteisRepository extends JpaRepository<OpcoesHoteis, Long> {
    @Query("SELECT o.nome FROM OpcoesHoteis o WHERE o.cidade = :cidade")
    List<String> findNomeByCidade(@Param("cidade") String cidade);

    List<OpcoesHoteis> findByCidade(String cidade);
}
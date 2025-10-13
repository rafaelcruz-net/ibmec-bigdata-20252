package br.edu.ibmec.chatbot_api.repository;

import br.edu.ibmec.chatbot_api.models.OpcoesCidades;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface OpcoesCidadesRepository extends JpaRepository<OpcoesCidades, Long> {
    @Query("SELECT o.nome FROM OpcoesCidades o")
    List<String> findAllNomeBy();
}
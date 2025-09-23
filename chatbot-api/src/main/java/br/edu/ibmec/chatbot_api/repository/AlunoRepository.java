package br.edu.ibmec.chatbot_api.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import br.edu.ibmec.chatbot_api.models.Aluno;

@Repository
public interface AlunoRepository extends JpaRepository<Aluno, Integer> {

}

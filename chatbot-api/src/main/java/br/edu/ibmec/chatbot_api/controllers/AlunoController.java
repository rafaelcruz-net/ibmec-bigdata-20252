package br.edu.ibmec.chatbot_api.controllers;

import java.util.List;

import org.apache.catalina.connector.Response;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

import br.edu.ibmec.chatbot_api.models.Aluno;
import br.edu.ibmec.chatbot_api.repository.AlunoRepository;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;



@Controller
@RequestMapping("/alunos")
public class AlunoController {

    @Autowired
    private AlunoRepository alunoRepository;

    @GetMapping
    public ResponseEntity<List<Aluno>> getAlunos()
    {
        return ResponseEntity.ok(alunoRepository.findAll());
    }

    @PostMapping()
    public ResponseEntity saveAluno(@RequestBody Aluno aluno) 
    {
        alunoRepository.save(aluno);
        return ResponseEntity.ok("Aluno Cadastrado com sucesso");
        
    }
    
    

}

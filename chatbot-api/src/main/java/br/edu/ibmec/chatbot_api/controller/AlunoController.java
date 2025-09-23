package br.edu.ibmec.chatbot_api.controller;


import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.GetMapping;

import br.edu.ibmec.chatbot_api.models.Aluno;
import br.edu.ibmec.chatbot_api.repository.AlunoRepository;


@Controller
@RequestMapping("/alunos")
public class AlunoController {

    @Autowired
    private AlunoRepository repository;

    @GetMapping()
    public ResponseEntity<List<Aluno>> getAlunos() {
        List<Aluno> response = repository.findAll();
        return new ResponseEntity<>(response, HttpStatus.OK);
    }
    

}

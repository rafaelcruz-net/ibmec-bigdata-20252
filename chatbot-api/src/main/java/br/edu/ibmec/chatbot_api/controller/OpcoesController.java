package br.edu.ibmec.chatbot_api.controller;

import br.edu.ibmec.chatbot_api.models.OpcoesVoos;
import br.edu.ibmec.chatbot_api.repository.OpcoesCidadesRepository;
import br.edu.ibmec.chatbot_api.repository.OpcoesHoteisRepository;
import br.edu.ibmec.chatbot_api.repository.OpcoesVoosRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/opcoes") 
public class OpcoesController {

        @Autowired
        private OpcoesCidadesRepository cidadesRepository;

        @Autowired
        private OpcoesHoteisRepository hoteisRepository;

        @Autowired
        private OpcoesVoosRepository voosRepository;

        @GetMapping("/cidades")
        public ResponseEntity<List<String>> getCidades() {
                return ResponseEntity.ok(cidadesRepository.findAllNomeBy());
        }

        @GetMapping("/hoteis")
        public ResponseEntity<Map<String, List<String>>> getHoteis() {
                List<String> cidades = cidadesRepository.findAllNomeBy();
                Map<String, List<String>> hoteisPorCidade = new HashMap<>();

                for (String cidade : cidades) {
                        List<String> hoteis = hoteisRepository.findNomeByCidade(cidade);
                        hoteisPorCidade.put(cidade, hoteis);
                }

                return ResponseEntity.ok(hoteisPorCidade);
        }

        @GetMapping("/voos")
        public ResponseEntity<List<OpcoesVoos>> getVoos() {
                return ResponseEntity.ok(voosRepository.findAll());
        }
}
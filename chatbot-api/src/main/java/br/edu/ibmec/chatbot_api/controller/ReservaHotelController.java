package br.edu.ibmec.chatbot_api.controller;

import br.edu.ibmec.chatbot_api.models.Cliente;
import br.edu.ibmec.chatbot_api.models.ReservaHotel;
import br.edu.ibmec.chatbot_api.repository.ClienteRepository;
import br.edu.ibmec.chatbot_api.repository.ReservaHotelRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/reservas-hotel")
public class ReservaHotelController {

    @Autowired
    private ReservaHotelRepository reservaHotelRepository;

    @Autowired
    private ClienteRepository clienteRepository;

    @GetMapping
    public List<ReservaHotel> getAllReservas() {
        return reservaHotelRepository.findAll();
    }

    @GetMapping("/cliente/cpf/{cpf}")
    public ResponseEntity<List<ReservaHotel>> getReservasByCpf(@PathVariable String cpf) {
        Optional<Cliente> cliente = clienteRepository.findByCpf(cpf);
        if (cliente.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        List<ReservaHotel> reservas = reservaHotelRepository.findByCliente(cliente.get());
        return ResponseEntity.ok(reservas);
    }

    @PostMapping
    public ResponseEntity<?> createReserva(@RequestBody ReservaHotel reserva) {
        if (reserva.getCliente() == null || reserva.getCliente().getCpf() == null) {
            return ResponseEntity.badRequest().body("Cliente é obrigatório");
        }

        // Busca o cliente pelo CPF
        Optional<Cliente> cliente = clienteRepository.findByCpf(reserva.getCliente().getCpf());
        if (cliente.isEmpty()) {
            // Se não encontrou, cria um novo cliente
            Cliente novoCliente = new Cliente();
            novoCliente.setNome(reserva.getCliente().getNome());
            novoCliente.setCpf(reserva.getCliente().getCpf());
            novoCliente.setEmail(reserva.getCliente().getEmail());
            novoCliente.setCelular(reserva.getCliente().getCelular());
            clienteRepository.save(novoCliente);

            reserva.setCliente(novoCliente);
        } else {
            // Se encontrou, usa o cliente existente
            reserva.setCliente(cliente.get());
        }

        ReservaHotel savedReserva = reservaHotelRepository.save(reserva);
        return ResponseEntity.status(HttpStatus.CREATED).body(savedReserva);
    }
}
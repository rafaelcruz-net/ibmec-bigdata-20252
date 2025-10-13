package br.edu.ibmec.chatbot_api.repository;

import br.edu.ibmec.chatbot_api.models.Cliente;
import br.edu.ibmec.chatbot_api.models.ReservaHotel;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ReservaHotelRepository extends JpaRepository<ReservaHotel, Long> {
    List<ReservaHotel> findByClienteCpf(String cpf);

    List<ReservaHotel> findByCliente(Cliente cliente);
}
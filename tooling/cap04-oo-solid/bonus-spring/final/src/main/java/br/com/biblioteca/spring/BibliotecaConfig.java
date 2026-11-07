package br.com.biblioteca.spring;

import br.com.biblioteca.Biblioteca;
import br.com.biblioteca.Notificador;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Quem monta o programa: o papel que o App fazia no projeto puro.
 * O Spring chama este método uma vez e entrega a Biblioteca pronta a quem pedir.
 */
@Configuration
public class BibliotecaConfig {

    @Bean
    public Biblioteca biblioteca(Notificador notificador) {
        return new Biblioteca(notificador);
    }
}

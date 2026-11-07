package br.com.biblioteca.spring;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Liga o Spring. Ele procura as peças deste pacote (br.com.biblioteca.spring).
 * O pacote br.com.biblioteca, com as regras, fica de fora: lá não há nada do Spring.
 */
@SpringBootApplication
public class BibliotecaApplication {

    public static void main(String[] args) {
        SpringApplication.run(BibliotecaApplication.class, args);
    }
}

package br.com.biblioteca;

import java.util.List;

/** O contrato de quem guarda livros. As funções dependem dele, não do DynamoDB. */
public interface LivroRepositorio {

    void salvar(Livro livro);

    List<Livro> listar();
}

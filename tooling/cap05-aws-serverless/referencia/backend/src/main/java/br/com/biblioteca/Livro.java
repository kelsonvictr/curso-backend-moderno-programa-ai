package br.com.biblioteca;

/** Um livro do acervo. O id é gerado no cadastro. */
public record Livro(String id, String titulo, String autor) {
}

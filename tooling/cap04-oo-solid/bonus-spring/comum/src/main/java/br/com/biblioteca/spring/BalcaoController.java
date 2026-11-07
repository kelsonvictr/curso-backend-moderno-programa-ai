package br.com.biblioteca.spring;

import br.com.biblioteca.Aluno;
import br.com.biblioteca.Biblioteca;
import br.com.biblioteca.Leitor;
import br.com.biblioteca.Livro;
import br.com.biblioteca.Professor;
import br.com.biblioteca.TipoDeLeitor;
import br.com.biblioteca.Visitante;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

/**
 * O balcão na web. Só traduz: texto do HTTP vira objeto, e a Biblioteca faz o resto.
 * Não calcula multa nem manda aviso.
 * Sem banco: cada devolução cria o livro já emprestado e devolve na hora.
 */
@RestController
public class BalcaoController {

    private final Biblioteca biblioteca;
    private final Map<String, TipoDeLeitor> tipos = Map.of(
            "aluno", new Aluno(),
            "professor", new Professor(),
            "visitante", new Visitante());

    public BalcaoController(Biblioteca biblioteca) {
        this.biblioteca = biblioteca;
    }

    @PostMapping("/devolucoes")
    public String devolver(@RequestParam String leitor, @RequestParam String tipo,
                           @RequestParam String livro, @RequestParam int dias) {
        TipoDeLeitor tipoDoLeitor = tipos.get(tipo);
        if (tipoDoLeitor == null) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Tipo de leitor desconhecido: " + tipo);
        }
        Leitor quem = new Leitor(leitor, leitor.toLowerCase() + "@email.com", tipoDoLeitor);
        Livro exemplar = new Livro("BALCAO", livro);
        biblioteca.emprestar(exemplar);

        int multa = biblioteca.devolver(exemplar, quem, dias);
        return leitor + " devolveu " + livro + " com " + dias + " dia(s) de atraso. Multa: " + multa + " centavos";
    }
}

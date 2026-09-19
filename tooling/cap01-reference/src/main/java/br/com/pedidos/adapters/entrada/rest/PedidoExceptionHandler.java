package br.com.pedidos.adapters.entrada.rest;
import br.com.pedidos.dominio.*;
import org.springframework.http.HttpStatus;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.*;
@RestControllerAdvice
public class PedidoExceptionHandler {
    record Erro(String mensagem) { }
    @ExceptionHandler({ItemInvalidoException.class, PedidoSemItensException.class})
    @ResponseStatus(HttpStatus.UNPROCESSABLE_ENTITY)
    Erro regra(RuntimeException e) { return new Erro(e.getMessage()); }
    @ExceptionHandler({MethodArgumentNotValidException.class, HttpMessageNotReadableException.class})
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    Erro formato(Exception e) { return new Erro("Confira o JSON e os campos obrigatórios."); }
}

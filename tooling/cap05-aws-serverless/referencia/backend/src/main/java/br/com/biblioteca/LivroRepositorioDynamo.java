package br.com.biblioteca;

import java.util.Comparator;
import java.util.List;
import java.util.Map;

import software.amazon.awssdk.http.urlconnection.UrlConnectionHttpClient;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.AttributeValue;
import software.amazon.awssdk.services.dynamodb.model.PutItemRequest;
import software.amazon.awssdk.services.dynamodb.model.ScanRequest;

/** Guarda os livros na tabela do DynamoDB. O nome da tabela chega por variável de ambiente. */
public class LivroRepositorioDynamo implements LivroRepositorio {

    private final DynamoDbClient dynamo;
    private final String tabela;

    public LivroRepositorioDynamo() {
        this(DynamoDbClient.builder().httpClient(UrlConnectionHttpClient.create()).build(),
                System.getenv("TABELA_LIVROS"));
    }

    public LivroRepositorioDynamo(DynamoDbClient dynamo, String tabela) {
        this.dynamo = dynamo;
        this.tabela = tabela;
    }

    @Override
    public void salvar(Livro livro) {
        dynamo.putItem(PutItemRequest.builder()
                .tableName(tabela)
                .item(Map.of(
                        "id", AttributeValue.fromS(livro.id()),
                        "titulo", AttributeValue.fromS(livro.titulo()),
                        "autor", AttributeValue.fromS(livro.autor())))
                .build());
    }

    @Override
    public List<Livro> listar() {
        // Scan lê a tabela inteira: serve para um acervo pequeno, não para milhões de itens.
        return dynamo.scan(ScanRequest.builder().tableName(tabela).build())
                .items().stream()
                .map(item -> new Livro(item.get("id").s(), item.get("titulo").s(), item.get("autor").s()))
                .sorted(Comparator.comparing(Livro::titulo))
                .toList();
    }
}

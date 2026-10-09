package br.com.analytics;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
@RestController
public class AnalyticsController {
    private final PainelVendas painel;
    public AnalyticsController(PainelVendas painel) { this.painel = painel; }
    @GetMapping("/analytics/resumo")
    public PainelVendas.Resumo resumo() { return painel.resumo(); }
}

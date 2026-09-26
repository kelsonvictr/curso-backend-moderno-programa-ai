---
workflow: general-video
flow: automation
storyboard: no
message: "Solicitar pagamento não é concluir pagamento."
destination: "Capítulo HTML em sala de aula"
aspect: "16:9"
language: "pt-BR"
length: "32s, oito pontos de pausa"
---
## Intent
Pedido aprovado: desenhos didáticos prontos e fluxos animados HyperFrames,
substituindo pranchetas. Usuário aprovou o percurso de RabbitMQ/Pagamentos.
## Decisões de execução
Composição única, silenciosa e local, navegador com passos manuais. Formato
horizontal acompanha o capítulo existente. Não há exportação de vídeo neste pedido.
## Design
Fundo #11111d, tinta #f4f1e9, laranja #ffb466, verde #a1e5b3.
Tipografia system-ui, sem recursos de fonte externos. Mensagem laranja em movimento,
resultado verde voltando, contador e estado trocam juntos. Sem movimento decorativo.
## Validação
Seek em ambos os sentidos, pausa e controle de movimento reduzido no player do capítulo.
Recebido, confirmado pelo broker, processado e pago são estados distintos.

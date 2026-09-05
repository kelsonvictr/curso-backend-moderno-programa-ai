/* Caderno livre do Cap 1, com armazenamento separado dos demais capítulos. */
const CADERNO_CONFIG = {
  id: 'backend-moderno-cap01',
  curso: 'Backend Moderno · Programa AI',
  capitulo: 'Capítulo 1',
  titulo: 'Meu caderno de SDD',
  subtitulo: 'decisões do Pedido 4711',
  emoji: '📝',
  stack: 'Java 21 · Spring · Agentes',
  voltar: 'index.html',
  frase: 'O agente acelera. Você registra as decisões que dão direção.<br><b>Programa AI · Prof. Kelson</b>',
  missoes: [
    {
      id: 'anotacoes', titulo: 'Minhas anotações',
      widgets: [{ tipo: 'texto', id: 'livre', linhas: 22, placeholder: '' }]
    },
    {
      id: 'rascunho', titulo: 'Meu espaço de rascunho',
      widgets: [{ tipo: 'desenho', id: 'livre', altura: 360, rotulo: 'Desenho livre', cores: [
        { cor: '#1d4ed8', rot: 'Caneta azul' },
        { cor: '#1f2937', rot: 'Caneta preta' },
        { cor: '#b45309', rot: 'Caneta laranja' }
      ] }]
    }
  ]
};
CadernoEngine.mount(document.getElementById('app'), CADERNO_CONFIG);
document.querySelector('.cad-texto').setAttribute('aria-label', 'Minhas anotações sobre SDD, Java e arquitetura');
document.querySelector('[data-aluno]').setAttribute('aria-label', 'Seu nome');
document.querySelector('.cad-des-canvas').setAttribute('aria-label', 'Área de desenho livre; use as anotações em texto se preferir o teclado');
document.querySelectorAll('.cad-cor').forEach(button => button.setAttribute('aria-label', button.title));

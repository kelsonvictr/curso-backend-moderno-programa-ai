/* Caderno livre do Cap 0, com armazenamento separado dos demais capítulos. */
const CADERNO_CONFIG = {
  id: 'backend-moderno-cap00',
  curso: 'Backend Moderno · Programa AI',
  capitulo: 'Capítulo 0',
  titulo: 'Meu caderno de IA',
  subtitulo: 'ideias, dúvidas e descobertas',
  emoji: '🤖',
  stack: 'IA · Agentes · SDD',
  voltar: 'index.html',
  frase: 'O professor apresenta. Você conecta as ideias do seu jeito.<br><b>Programa AI · Prof. Kelson</b>',
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
        { cor: '#7c3aed', rot: 'Caneta roxa' }
      ] }]
    }
  ]
};
CadernoEngine.mount(document.getElementById('app'), CADERNO_CONFIG);
document.querySelector('.cad-texto').setAttribute('aria-label', 'Minhas anotações sobre IA e agentes');
document.querySelector('[data-aluno]').setAttribute('aria-label', 'Seu nome');
document.querySelector('.cad-des-canvas').setAttribute('aria-label', 'Área de desenho livre; use as anotações em texto se preferir o teclado');
document.querySelectorAll('.cad-cor').forEach(button => button.setAttribute('aria-label', button.title));

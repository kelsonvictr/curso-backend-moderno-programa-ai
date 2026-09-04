/* Atividades de classificação e revisão com estados locais independentes. */
(() => {
  'use strict';
  const make=(tag,text)=>{const e=document.createElement(tag);e.textContent=text;return e;};
  const cards=document.getElementById('regras-cards');
  const categories=['Escolha um destino','Instruções gerais','Spec desta tarefa','Documentação de referência','Configuração segura de credenciais'];
  const rules=[
    ['Como executar os testes em todas as tarefas',1,'O comando recorrente orienta o trabalho no projeto.'],
    ['Nesta tarefa, aceitar zero e recusar preço negativo',2,'É o comportamento que esta mudança precisa implementar.'],
    ['Tutorial detalhado da biblioteca usada',3,'É material de consulta; carregue o trecho relevante quando necessário.'],
    ['Chave de acesso a uma API',4,'Configure como credencial no ambiente apropriado; não coloque o valor no arquivo de instruções.'],
    ['Convenção do projeto: preços em centavos',1,'Essa representação precisa continuar consistente entre tarefas.']
  ];
  if(cards){
    rules.forEach(([text],i)=>{const wrap=make('div','');wrap.className='jg-file';const label=make('label',text);label.htmlFor='regra-'+i;const sel=make('select','');sel.id=label.htmlFor;sel.style.cssText='display:block;width:100%;margin-top:10px;padding:12px;background:#202030;color:#eee;border:1px solid #9983ba;border-radius:8px;font:inherit';categories.forEach((c,j)=>{const o=make('option',c);o.value=j;sel.append(o);});wrap.append(label,sel);cards.append(wrap);});
    document.getElementById('regras-check').addEventListener('click',()=>{
      const result=document.getElementById('regras-result'),selects=[...cards.querySelectorAll('select')];
      if(selects.some(s=>s.value==='0')){result.textContent='Escolha um destino para todos os cartões antes de conferir.';return;}
      const hits=rules.filter((r,i)=>Number(selects[i].value)===r[1]).length;
      result.replaceChildren(make('strong',`${hits} / ${rules.length} destinos corretos.`));rules.forEach(([text,answer,why],i)=>result.append(make('p',`${Number(selects[i].value)===answer?'✓':'↳'} ${text}: ${categories[answer]}. ${why}`)));
    });
  }
  const container=document.getElementById('review-lines');if(!container)return;
  const rows=[
    ['ProdutoService.java — trecho do método de cadastro',null],
    ['if (precoEmCentavos <= 0) {','A condição também rejeita zero, que é permitido. Use < 0.'],
    ['    return "Preço inválido";',false],
    ['}',false],
    ['produtos.add(produto);',false],
    ['return "Produto cadastrado";',false],
    ['ProdutoServiceTest.java — resumo dos casos executados',null],
    ['Apenas preço 1000: aceito. Nenhum teste de -500 ou 0.','A spec exige os três casos e verificar que o recusado não entrou na lista.'],
    ['ProdutoController.java — alteração adicional',null],
    ['Removida a função de listar produtos.','A listagem está fora do escopo e deveria continuar funcionando.']
  ];
  let found=new Set();
  function render(){
    found=new Set();container.replaceChildren();document.getElementById('review-feedback').textContent='0 / 3 problemas encontrados.';
    rows.forEach(([text,reason],i)=>{if(reason===null){container.append(make('h4',text));return;}
      const b=make('button',text);b.type='button';b.className='jg-token';b.style.cssText='display:block;width:100%;margin:6px 0;white-space:pre-wrap;overflow-wrap:anywhere;font-size:.8rem';b.setAttribute('aria-pressed','false');
      b.addEventListener('click',()=>{const note=document.getElementById('review-feedback');if(reason){found.add(i);b.setAttribute('aria-pressed','true');note.textContent=`${found.size} / 3 problemas encontrados. ${reason}`+(found.size===3?' Entrega devolvida para correção: ajustar a condição, completar os testes e preservar a listagem.':'');}else{note.textContent=`${found.size} / 3 problemas encontrados. Este trecho é compatível com o fluxo: recusar antes de salvar; salvar e informar sucesso para entradas aceitas. Procure a condição errada e as violações da spec.`;}});container.append(b);
    });
  }
  document.getElementById('review-reset').addEventListener('click',render);render();
})();

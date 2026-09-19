/* Página de consulta: sem reprodução, rede ou estado compartilhado com os alunos. */
(() => {
  'use strict';
  const status=document.getElementById('copy-status');
  let timer;
  document.querySelectorAll('[data-copy]').forEach(button=>{
    button.addEventListener('click',async()=>{
      const prompt=button.closest('.prompt');
      const source=prompt.querySelector('pre');
      let copied=false;
      try{await navigator.clipboard.writeText(source.textContent);copied=true;}catch{}
      if(!copied){
        const field=document.createElement('textarea');
        field.value=source.textContent;field.style.cssText='position:fixed;left:-9999px';document.body.append(field);field.select();
        try{copied=document.execCommand('copy');}catch{}
        field.remove();button.focus();
      }
      clearTimeout(timer);
      if(copied){status.textContent='Copiado. Cole na conversa com o agente.';}
      else{const details=prompt.querySelector('details');if(details)details.open=true;status.textContent='Não foi possível copiar. Selecione o texto do prompt e copie manualmente.';}
      timer=setTimeout(()=>{status.textContent='';},4000);
    });
  });
})();

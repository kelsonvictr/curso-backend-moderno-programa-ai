// Kit das composições do Cap 02: monta o SVG de forma determinística e registra
// cada mudança no timeline pausado. Nada depende de relógio, rede ou interação.
(function(){
  const NS='http://www.w3.org/2000/svg';
  function Kit(svg,tl){this.svg=svg;this.tl=tl;}
  Kit.prototype.el=function(tag,attrs,parent,text){
    const e=document.createElementNS(NS,tag);
    for(const k in attrs)e.setAttribute(k,attrs[k]);
    if(text!=null)e.textContent=text;
    (parent||this.svg).appendChild(e);return e;
  };
  Kit.prototype.g=function(attrs,parent){return this.el('g',attrs||{},parent);};
  Kit.prototype.text=function(x,y,t,cls,parent,extra){return this.el('text',Object.assign({x:x,y:y,class:cls||''},extra||{}),parent,t);};
  // Caixa com nome e subtítulo. Retorna o grupo para uso posterior.
  Kit.prototype.node=function(x,y,w,h,nome,sub,cls,parent){
    const g=this.g({},parent);
    this.el('rect',{x:x,y:y,width:w,height:h,rx:16,class:cls||'node'},g);
    this.text(x+20,y+36,nome,'label',g);
    if(sub)this.text(x+20,y+h-22,sub,'small',g);
    return g;
  };
  // Um texto por valor; cada valor aparece no seu instante e some no próximo.
  Kit.prototype.variants=function(x,y,cls,lista,parent,extra){
    const tl=this.tl,self=this;
    lista.forEach(function(item,i){
      const e=self.text(x,y,item[1],item[2]||cls,parent,Object.assign({opacity:i===0?1:0},extra||{}));
      if(i>0)tl.set(e,{opacity:1},item[0]);
      if(lista[i+1])tl.set(e,{opacity:0},lista[i+1][0]);
    });
  };
  // Agrupa tudo o que foi criado a partir do filho n (para esmaecer um cenário inteiro).
  Kit.prototype.wrapFrom=function(n){const g=document.createElementNS(NS,'g');const filhos=Array.prototype.slice.call(this.svg.children,n);filhos.forEach(function(f){g.appendChild(f);});this.svg.appendChild(g);return g;};
  Kit.prototype.mark=function(){return this.svg.children.length;};
  Kit.prototype.show=function(alvo,t){this.tl.set(alvo,{opacity:1},t);};
  Kit.prototype.hide=function(alvo,t){this.tl.set(alvo,{opacity:0},t);};
  Kit.prototype.fadeIn=function(alvo,t,d){this.tl.fromTo(alvo,{opacity:0},{opacity:1,duration:d||.35,immediateRender:false},t);};
  Kit.prototype.fadeOut=function(alvo,t,d){this.tl.to(alvo,{opacity:0,duration:d||.3},t);};
  // Ficha que viaja. O centro da ficha é a coordenada informada.
  Kit.prototype.token=function(rotulo,fill,ink,w){
    const g=this.g({opacity:0,transform:'translate(640 300)','data-layout-allow-overlap':'true'});w=w||Math.max(60,rotulo.length*13+26);
    this.el('rect',{x:-w/2,y:-18,width:w,height:36,rx:9,fill:fill,stroke:'#11111d','stroke-width':2},g);
    this.el('text',{x:0,y:7,'text-anchor':'middle','data-layout-allow-overlap':'true',style:'fill:'+ink+';font-size:19px;font-weight:800'},g,rotulo);
    return g;
  };
  // Aparece no primeiro ponto e percorre os demais em velocidade constante.
  Kit.prototype.travel=function(tok,pts,t0,vel){
    vel=vel||420;const tl=this.tl;
    tl.fromTo(tok,{x:pts[0][0],y:pts[0][1],opacity:0},{x:pts[0][0],y:pts[0][1],opacity:1,duration:.2,immediateRender:false},t0);
    let t=t0+.2;
    for(let i=1;i<pts.length;i++){
      const dx=pts[i][0]-pts[i-1][0],dy=pts[i][1]-pts[i-1][1];
      const d=Math.max(.25,Math.sqrt(dx*dx+dy*dy)/vel);
      tl.to(tok,{x:pts[i][0],y:pts[i][1],duration:d,ease:'none'},t);t+=d;
    }
    return t;
  };
  // Linha que se desenha (seta de diagrama de sequência).
  Kit.prototype.draw=function(el,t,d){
    const L=el.getTotalLength?el.getTotalLength():400;
    el.setAttribute('stroke-dasharray',L);el.setAttribute('stroke-dashoffset',L);
    this.tl.to(el,{strokeDashoffset:0,duration:d||.7,ease:'none'},t);
  };
  // Legenda inferior: [instante, título, linha 1, linha 2?]
  Kit.prototype.captions=function(lista,y){
    y=y||588;const self=this;
    this.el('line',{x1:60,y1:y-42,x2:1220,y2:y-42,stroke:'#3a3850','stroke-width':2});
    const itens=lista.map(function(c){return [c[0],c[1]];});
    this.variants(72,y,'caption-title',itens);
    this.variants(72,y+44,'caption',lista.map(function(c){return [c[0],c[2]||''];}));
    this.variants(72,y+80,'caption',lista.map(function(c){return [c[0],c[3]||''];}));
  };
  window.HFKit=Kit;
})();

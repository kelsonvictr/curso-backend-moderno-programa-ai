const form = document.getElementById("form-livro");
const botao = document.getElementById("botao");
const aviso = document.getElementById("aviso");
const acervo = document.getElementById("acervo");

function avisar(texto, erro = false) {
  aviso.textContent = texto;
  aviso.classList.toggle("erro", erro);
}

async function carregarAcervo() {
  try {
    const resposta = await fetch(`${API_URL}/livros`);
    if (!resposta.ok) throw new Error(`A API respondeu ${resposta.status}`);
    const livros = await resposta.json();

    acervo.replaceChildren();
    for (const livro of livros) {
      const item = document.createElement("li");
      const titulo = document.createElement("strong");
      const autor = document.createElement("span");
      titulo.textContent = livro.titulo;
      autor.textContent = livro.autor;
      item.append(titulo, autor);
      acervo.append(item);
    }
    if (livros.length === 0) avisar("Nenhum livro ainda. Cadastre o primeiro.");
  } catch (erro) {
    // Erro de CORS cai aqui: o navegador bloqueia e o fetch falha sem dizer o motivo.
    // O motivo aparece no Console do navegador (F12).
    avisar("Não consegui falar com a API. Abra o Console (F12) e leia o erro.", true);
    console.error(erro);
  }
}

form.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  botao.disabled = true;
  avisar("Enviando...");
  try {
    const resposta = await fetch(`${API_URL}/livros`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ titulo: form.titulo.value, autor: form.autor.value }),
    });
    const corpo = await resposta.json();
    if (!resposta.ok) throw new Error(corpo.erro || `A API respondeu ${resposta.status}`);
    form.reset();
    avisar(`"${corpo.titulo}" entrou no acervo.`);
    await carregarAcervo();
  } catch (erro) {
    avisar(erro.message === "Failed to fetch"
      ? "Não consegui falar com a API. Abra o Console (F12) e leia o erro."
      : erro.message, true);
    console.error(erro);
  } finally {
    botao.disabled = false;
  }
});

carregarAcervo();

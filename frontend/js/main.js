

import { encurtarUrl } from "./api.js";
import { copiarTexto } from "./clipboard.js";


// ------------------------------------------------------------
// 1) PEGAR OS ELEMENTOS uma vez só, no topo.
//    Buscar no DOM é caro; a gente guarda a referência e reusa.
// ------------------------------------------------------------
const form      = document.getElementById("shortenForm");
const input     = document.getElementById("urlInput");
const submitBtn = document.getElementById("submitBtn");
const feedback  = document.getElementById("formFeedback");
const result    = document.getElementById("result");
const resultLink = document.getElementById("resultLink");
const copyBtn   = document.getElementById("copyBtn");


// ------------------------------------------------------------
// 2) FUNÇÕES AUXILIARES pequenas, cada uma com um trabalho.
// ------------------------------------------------------------

// Mostra uma mensagem de erro embaixo do formulário.
function mostrarErro(mensagem) {
  feedback.textContent = mensagem;
  feedback.hidden = false;   // hidden=false = aparece
  result.hidden = true;      // some com o resultado antigo, se houver
}

// Esconde a mensagem de erro.
function limparErro() {
  feedback.hidden = true;
}

// Mostra o card de resultado com a URL curta.
function mostrarResultado(urlCurta) {
  resultLink.href = urlCurta;        // pra onde o link leva
  resultLink.textContent = urlCurta; // o texto que aparece
  result.hidden = false;
  limparErro();
}

// Liga/desliga o estado "carregando".
// A classe .is-loading (no CSS) troca a seta pelo spinner girando.
function definirCarregando(estaCarregando) {
  form.classList.toggle("is-loading", estaCarregando);
  submitBtn.disabled = estaCarregando;  // evita clique duplo
  input.disabled = estaCarregando;
}


// ------------------------------------------------------------
// 3) O EVENTO PRINCIPAL: enviar o formulário.
//    Dispara no clique em "Encurtar" E no Enter dentro do input.
// ------------------------------------------------------------
form.addEventListener("submit", async (evento) => {

  // Sem isto, o navegador RECARREGA a página ao enviar o form —
  // e a gente perderia tudo. preventDefault segura esse comportamento
  // padrão pra fazermos a chamada por JavaScript no lugar.
  evento.preventDefault();

  const urlLonga = input.value.trim();

  // Validação de borda: campo vazio.
  if (urlLonga === "") {
    mostrarErro("Cole uma URL antes de encurtar.");
    return;
  }

  // Validação de formato usando o próprio navegador.
  // input type="url" já sabe dizer se "abc" é uma URL válida.
  if (!input.checkValidity()) {
    mostrarErro("Isso não parece uma URL. Ex.: https://exemplo.com");
    return;
  }

  // Tudo certo até aqui: chama o backend.
  definirCarregando(true);
  try {
    const urlCurta = await encurtarUrl(urlLonga);
    mostrarResultado(urlCurta);
  } catch (erro) {
    // Qualquer erro que api.js lançou (rede, 422, 500...) cai aqui
    // com a mensagem amigável já pronta.
    mostrarErro(erro.message);
  } finally {
    // finally roda SEMPRE — deu certo ou deu erro. É o lugar certo
    // pra desligar o "carregando"; senão o spinner poderia girar
    // pra sempre num caminho de erro que a gente esquecesse.
    definirCarregando(false);
  }
});


// ------------------------------------------------------------
// 4) BOTÃO DE COPIAR o resultado.
// ------------------------------------------------------------
copyBtn.addEventListener("click", async () => {
  const copiou = await copiarTexto(resultLink.textContent);

  if (!copiou) {
    mostrarErro("Não consegui copiar automático. Copie manualmente, por favor.");
    return;
  }

  // Feedback visual: fica verde por 1,5s. A classe .is-copied está no CSS.
  copyBtn.classList.add("is-copied");
  copyBtn.setAttribute("aria-label", "Link copiado!");
  setTimeout(() => {
    copyBtn.classList.remove("is-copied");
    copyBtn.setAttribute("aria-label", "Copiar link encurtado");
  }, 1500);
});

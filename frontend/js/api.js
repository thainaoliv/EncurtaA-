const BACKEND_LOCAL = "http://127.0.0.1:8000";
const BACKEND_PRODUCAO = "https://encurtaa.onrender.com";

function descobrirEnderecoDoBackend() {
  const hostsLocais = ["localhost", "127.0.0.1"];

  if (hostsLocais.includes(location.hostname)) {
    return BACKEND_LOCAL;
  }
  return BACKEND_PRODUCAO;
}

// A raiz do backend, já decidida.
export const API_BASE = descobrirEnderecoDoBackend();

export async function encurtarUrl(urlLonga) {

  let resposta;

  try {
    resposta = await fetch(`${API_BASE}/encurtar`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      // O nome "url_original" NÃO é escolha nossa: é exatamente o nome
      // que o backend espera receber (backend/api.py, classe LinkRequest).
      // Qualquer outro nome faz o backend responder 422.
      body: JSON.stringify({ url_original: urlLonga }),
    });
  } catch {
    throw new Error("Não foi possível falar com o servidor. Verifique sua conexão e tente de novo.");
  }

  // 2) O SERVIDOR RESPONDEU, MAS FOI ERRO? (status fora de 200–299)
  //    ok = true só quando o status é de sucesso.
  if (!resposta.ok) {
    // 422 = "os dados que você mandou não estão no formato que eu peço".
    // Na prática é quase sempre URL inválida, MAS também aparece quando
    // o frontend manda um nome de campo diferente do que o backend
    // espera. Por isso a mensagem não afirma de quem é a culpa: manda
    // conferir a URL e sugere o console, onde o erro real aparece.
    if (resposta.status === 422 || resposta.status === 400) {
      throw new Error("O servidor não aceitou esse endereço. Confira a URL (ex.: https://exemplo.com).");
    }
    throw new Error("O servidor teve um problema ao encurtar. Tente de novo em instantes.");
  }

  // 3) DEU CERTO. O backend já manda o link curto pronto, no campo
  //    "url_curta" — ele é quem sabe o endereço público do servidor.
  //    Aqui a gente só confere que veio e devolve. Nada de montar
  //    URL à mão: um lugar só decide isso, e é o backend.
  const dados = await resposta.json();

  if (!dados.url_curta) {
    throw new Error("O servidor respondeu, mas não veio o link encurtado.");
  }

  return dados.url_curta;
}

// ============================================================
// clipboard.js — copiar texto para a área de transferência.
//
// Isolado porque "copiar" não tem nada a ver com "encurtar".
// Cada arquivo faz uma coisa só.
// ============================================================

// Devolve true se copiou, false se não deu.
// async porque a API do navegador (navigator.clipboard) também é
// assíncrona — ela pede permissão e isso pode demorar um instante.
export async function copiarTexto(texto) {
  try {
    await navigator.clipboard.writeText(texto);
    return true;
  } catch {
    // navigator.clipboard só funciona em https ou localhost.
    // Se falhar (ex.: abriram por file://), a gente devolve false
    // em vez de quebrar a página inteira.
    return false;
  }
}

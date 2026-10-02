# EncurtaAí — Frontend

HTML, CSS e JavaScript puro. Sem framework, sem build step.

## Estrutura

    frontend/
    ├── index.html            # única página (HTML puro não tem "include")
    ├── assets/favicon.svg
    ├── css/
    │   ├── 01-reset.css      # zera padrões do navegador + utilitários
    │   ├── 02-tokens.css     # variáveis (cores, espaços, fontes)
    │   ├── 03-base.css       # elementos nus: body, h1, p, input
    │   ├── 04-layout.css     # container, header, grids, footer
    │   └── 05-components.css # btn, badge, feature, url-card, result
    └── js/
        ├── api.js            # chamadas ao backend
        ├── clipboard.js      # copiar link
        └── main.js           # ponto de entrada (type="module")

Os arquivos CSS são numerados porque **a ordem da cascata importa**:
o que vem depois pode sobrescrever o que veio antes.

## Como rodar

Por causa do `type="module"`, abrir o `index.html` com duplo clique
(`file://`) quebra os imports. Use um servidor local:

    # VS Code: extensão "Live Server" → botão "Go Live"
    # ou, com Python instalado:
    python -m http.server 5500

Depois acesse http://localhost:5500

## Backend

https://encurtaa.onrender.com

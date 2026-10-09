import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl
from shortener import criar_link, buscar_url_original, contar_clique
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Lê o arquivo .env e joga o conteúdo nas variáveis de ambiente.
# Precisa vir ANTES dos os.environ.get() abaixo.
load_dotenv()


# Endereço público deste servidor, usado para montar o link curto.
# O 2º argumento é o padrão, usado quando a variável não existe — e o
# padrão é sempre o local, para rodar na sua máquina sem configurar nada.
BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000").rstrip("/")

# Caminho da pasta frontend/ no disco.
# __file__ é o caminho deste próprio arquivo (backend/api.py).
# .resolve() transforma em caminho absoluto, sem "..." pelo meio.
# O 1º .parent é a pasta backend/; o 2º é a raiz do projeto.
# Daí descemos para frontend/, que é irmã da backend/.
PASTA_FRONTEND = Path(__file__).resolve().parent.parent / "frontend"

ORIGENS_PERMITIDAS = os.environ.get(
    "ALLOWED_ORIGINS",
    "http://localhost:5500,http://127.0.0.1:5500",
).split(",")


app = FastAPI(title="EncurtaAÍ")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGENS_PERMITIDAS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Publica as pastas de arquivos prontos (CSS, JS, imagens).
# O caminho da esquerda ("/css") é o que o navegador pede; ele precisa bater
# com o que está escrito no index.html (<link href="css/01-reset.css">).
# Montamos pasta por pasta, e não uma só em "/", porque um mount em "/"
# brigaria com a rota GET /{codigo} lá embaixo.
app.mount("/css", StaticFiles(directory=PASTA_FRONTEND / "css"), name="css")
app.mount("/js", StaticFiles(directory=PASTA_FRONTEND / "js"), name="js")
app.mount("/assets", StaticFiles(directory=PASTA_FRONTEND / "assets"), name="assets")


class LinkRequest(BaseModel):
    url_original: HttpUrl


# A página inicial. Sem esta rota, abrir o endereço "pelado" do servidor
# pelo menos um caractere e não cobre a raiz.
# FileResponse manda um arquivo do disco como resposta HTTP.
@app.get("/")
def pagina_inicial():
    return FileResponse(PASTA_FRONTEND / "index.html")

@app.post("/encurtar")
def encurtar(link: LinkRequest):
    # criar_link grava no banco e devolve só o código (ex.: "aB3xY9k").
    codigo = criar_link(str(link.url_original))

    # Aqui, sim, é o lugar de montar o link completo: este arquivo sabe
    # em que endereço o servidor está rodando, porque leu o BASE_URL.
    return {"url_curta": f"{BASE_URL}/{codigo}"}

@app.get("/{codigo}")
def redirecionar(codigo: str):
    url_original = buscar_url_original(codigo)
    if url_original is None:
        raise HTTPException(status_code=404, detail="Link não encontrado")
    contar_clique(codigo)
    return RedirectResponse(url=url_original)
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
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

class LinkRequest(BaseModel):
    url_original: HttpUrl

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
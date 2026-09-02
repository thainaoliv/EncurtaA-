from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from shortener import criar_link, buscar_url_original, contar_clique

app = FastAPI(title="EncurtaAÍ")

class LinkRequest(BaseModel):
    url_original: HttpUrl

@app.get("/")
def resultado():
    return "Galera, To viva"

@app.post("/encurtar")
def encurtar(link: LinkRequest):
    url_curta = criar_link(str(link.url_original))
    return {"url_curta": url_curta}

@app.get("/{codigo}")
def redirecionar(codigo: str):
    url_original = buscar_url_original(codigo)
    if url_original is None:
        raise HTTPException(status_code=404, detail="Link não encontrado")
    contar_clique(codigo)
    return RedirectResponse(url=url_original)
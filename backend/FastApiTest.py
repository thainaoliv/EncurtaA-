from fastapi import FastAPI

app = FastAPI(title = "EncurtaAÍ")


@app.get("/") # Aqui acredito que seja o endereço?
def resultado (): # Função que vai disparar na hora que o usuario entrar na tela?
    resposta = "Galera, To viva" # O que eu vou mostrar na tela
    return resposta
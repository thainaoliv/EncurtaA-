import secrets
import string
from database import supabase

def gerar_codigo():
    caracteres_permitidos = string.ascii_letters + string.digits
    codigo = ''.join(secrets.choice(caracteres_permitidos) for _ in range(7))
    return codigo

def criar_link(url_original):
    while True:
        codigo = gerar_codigo()
        try:
            supabase.table("links").insert({
                "codigo": codigo,
                "url_original": url_original
            }).execute()
            break
        except Exception as erro:
            if "duplicate key" in str(erro):
                continue
            else:
                raise

    url_curta = "https://encurtaa.onrender.com/" + codigo
    return url_curta

def buscar_url_original(codigo):
    resposta = supabase.table("links").select("url_original").eq("codigo", codigo).execute()
    if len(resposta.data) == 0:
        return None
    return resposta.data[0]["url_original"]

def contar_clique(codigo):
    qtd = supabase.table("links").select("qtd_cliques").eq("codigo", codigo).execute()
    valor = qtd.data[0]["qtd_cliques"]
    novo_valor = valor + 1
    supabase.table("links").update({"qtd_cliques": novo_valor}).eq("codigo", codigo).execute()

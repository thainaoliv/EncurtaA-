import string
from shortener import gerar_codigo, buscar_url_original
import shortener

def test_gerar_codigo_():
    caracteres_permitidos = string.ascii_letters + string.digits

    for _ in range(1000):
        codigo = gerar_codigo()

        # Regra 1: tamanho exato 7
        assert len(codigo) == 7

        # Regra 2: todo caractere pertence ao conjunto permitido
        for caractere in codigo:
            assert caractere in caracteres_permitidos

def test_buscar_url_original_existe(monkeypatch):
    # 1. Criar a resposta falsa que o banco "devolveria"

    class RespostaFake:
        data = [{"url_original": "https://google.com"}]

     # 2. Criar um dublê da cadeia supabase.table(...).select(...).eq(...).execute()
    class QueryFake:
        def select(self, *args): return self
        def eq(self, *args): return self
        def execute(self, *args): return self

    class SupabaseFake:
        def table(self, *args): return QueryFake()

    # 3. Substituir o supabase real pelo falso, só durante este teste
    monkeypatch.setattr(shortener, "supabase", SupabaseFake())

    # 4. Rodar a função e verificar
    resultado = buscar_url_original("qualquercodigo")
    assert resultado == "https://google.com"

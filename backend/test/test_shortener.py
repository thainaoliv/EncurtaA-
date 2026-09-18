import string
from shortener import gerar_codigo, buscar_url_original, contar_clique, criar_link
import shortener
import pytest

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
        def execute(self, *args): return RespostaFake

    class SupabaseFake:
        def table(self, *args): return QueryFake()

    # 3. Substituir o supabase real pelo falso, só durante este teste
    monkeypatch.setattr(shortener, "supabase", SupabaseFake())

    # 4. Rodar a função e verificar
    resultado = buscar_url_original("qualquercodigo")
    assert resultado == "https://google.com"

def test_buscar_url_original_nao_existe(monkeypatch):
    class RespostaFake:
        data = []          # lista vazia = banco não achou nada

    class QueryFake:
        def select(self, *args): return self
        def eq(self, *args): return self
        def execute(self): return RespostaFake()

    class SupabaseFake:
        def table(self, *args): return QueryFake()

    monkeypatch.setattr(shortener, "supabase", SupabaseFake())

    resultado = buscar_url_original("codigoinexistente")
    assert resultado is None

def test_contar_cliques(monkeypatch):
    class RespostaFake:
        data = [{"qtd_cliques": 5}]        # banco tinha 5 cliques

    class QueryFake:
        def select(self, *args): return self
        def eq(self, *args): return self
        def update(self, dados):
            self.dados_recebidos = dados    # anota o que recebeu
            return self
        def execute(self): return RespostaFake()

    query_fake = QueryFake()               # ← cria UMA vez, guarda na variável

    class SupabaseFake:
        def table(self, *args): return query_fake   # ← devolve SEMPRE essa mesma

    monkeypatch.setattr(shortener, "supabase", SupabaseFake())

    contar_clique("qualquercodigo")        # roda a função

    # agora o teste pega a variável e espia o que foi guardado
    assert query_fake.dados_recebidos == {"qtd_cliques": 6}

def test_criar_link_feliz(monkeypatch):
    class RespostaFake:
        data = [{"codigo": "abc"}]

    class QueryFake:
        def insert(self, *args): return self
        def execute(self): return RespostaFake()

    class SupabaseFake:
        def table(self, *args): return QueryFake()

    monkeypatch.setattr(shortener, "supabase", SupabaseFake())

    url = criar_link("https://google.com")

    assert url.startswith("https://encurtaa.onrender.com/")
    assert len(url) == len("https://encurtaa.onrender.com/") + 8

def test_criar_link_colisao(monkeypatch):
    class RespostaFake:
        data = [{"codigo": "abc"}]

    class QueryFake:
        tentativas = 0    # contador de quantas vezes o execute foi chamado

        def insert(self, *args): return self

        def execute(self):
            QueryFake.tentativas += 1        # a cada chamada, soma 1
            if QueryFake.tentativas == 1:    # na 1ª chamada...
                raise Exception("duplicate key value violates unique constraint")
            return RespostaFake()            # da 2ª em diante, funciona

    class SupabaseFake:
        def table(self, *args): return QueryFake()

    monkeypatch.setattr(shortener, "supabase", SupabaseFake())

    url = criar_link("https://google.com")

    assert url.startswith("https://encurtaa.onrender.com/")
    assert QueryFake.tentativas == 2

def test_criar_link_erro_real(monkeypatch):
    class QueryFake:
        def insert(self, *args): return self
        def execute(self):
            raise Exception("conncetion timeout")

    class SupaBaseFake:
        def table(self, *args): return QueryFake()

    monkeypatch.setattr(shortener, "supabase", SupaBaseFake())

    with pytest.raises(Exception):
        criar_link("https://google.com")


import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base
from main import app, get_db

# Configuração do banco de teste em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override da dependência de DB
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Cria as tabelas no banco de teste
Base.metadata.create_all(bind=engine)

client = TestClient(app)

# Dados de exemplo
SAMPLE_CATEGORIA = {
    "nome": "Ficção Científica",
    "descricao": "Livros de ficção científica e fantasia"
}

SAMPLE_LIVRO = {
    "titulo": "Duna",
    "autor": "Frank Herbert",
    "ano_publicacao": 1965,
}

SAMPLE_LIVRO_WITH_CATEGORIA = {
    "titulo": "Fundação",
    "autor": "Isaac Asimov",
    "ano_publicacao": 1951,
    "categoria_id": 1
}

def test_list_livros_empty():
    response = client.get("/livros/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_and_get_livro():
    # cria livro sem categoria
    resp = client.post("/livros/", json=SAMPLE_LIVRO)
    assert resp.status_code == 201
    data = resp.json()
    assert data["titulo"] == SAMPLE_LIVRO["titulo"]
    assert data["autor"] == SAMPLE_LIVRO["autor"]
    assert "id" in data
    livro_id = data["id"]

    # busca o mesmo livro
    resp2 = client.get(f"/livros/{livro_id}")
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["id"] == livro_id
    assert data2["titulo"] == SAMPLE_LIVRO["titulo"]

def test_create_livro_validation_error():
    invalid = {"titulo": "", "autor": "X", "ano_publicacao": 3000}
    resp = client.post("/livros/", json=invalid)
    assert resp.status_code == 422

def test_update_livro():
    # cria
    resp = client.post("/livros/", json=SAMPLE_LIVRO)
    livro_id = resp.json()["id"]

    # atualiza título apenas
    resp2 = client.put(f"/livros/{livro_id}", json={"titulo": "Duna Atualizada"})
    assert resp2.status_code == 200
    assert resp2.json()["titulo"] == "Duna Atualizada"

def test_patch_livro():
    # cria
    resp = client.post("/livros/", json=SAMPLE_LIVRO)
    livro_id = resp.json()["id"]

    # patch
    resp2 = client.patch(f"/livros/{livro_id}", json={"autor": "F. Herbert"})
    assert resp2.status_code == 200
    assert resp2.json()["autor"] == "F. Herbert"

def test_delete_livro():
    # cria
    resp = client.post("/livros/", json=SAMPLE_LIVRO)
    livro_id = resp.json()["id"]

    # deleta
    resp2 = client.delete(f"/livros/{livro_id}")
    assert resp2.status_code == 204

    # confirma remoção
    resp3 = client.get(f"/livros/{livro_id}")
    assert resp3.status_code == 404

def test_list_categorias_empty():
    response = client.get("/categorias/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_and_get_categoria():
    resp = client.post("/categorias/", json=SAMPLE_CATEGORIA)
    assert resp.status_code == 201
    data = resp.json()
    assert data["nome"] == SAMPLE_CATEGORIA["nome"]
    assert "id" in data
    categoria_id = data["id"]

    resp2 = client.get(f"/categorias/{categoria_id}")
    assert resp2.status_code == 200
    assert resp2.json()["id"] == categoria_id

def test_update_categoria():
    resp = client.post("/categorias/", json=SAMPLE_CATEGORIA)
    categoria_id = resp.json()["id"]

    resp2 = client.put(
        f"/categorias/{categoria_id}",
        json={"nome": "Ficção Atualizada", "descricao": "Atualizada"}
    )
    assert resp2.status_code == 200
    assert resp2.json()["nome"] == "Ficção Atualizada"

def test_patch_categoria():
    resp = client.post("/categorias/", json=SAMPLE_CATEGORIA)
    categoria_id = resp.json()["id"]

    resp2 = client.patch(f"/categorias/{categoria_id}", json={"descricao": "Parcial"})
    assert resp2.status_code == 200
    assert resp2.json()["descricao"] == "Parcial"

def test_delete_categoria():
    resp = client.post("/categorias/", json=SAMPLE_CATEGORIA)
    categoria_id = resp.json()["id"]

    resp2 = client.delete(f"/categorias/{categoria_id}")
    assert resp2.status_code == 204

    resp3 = client.get(f"/categorias/{categoria_id}")
    assert resp3.status_code == 404
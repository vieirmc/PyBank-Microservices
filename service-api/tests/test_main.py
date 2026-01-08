import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app, get_db
from app.database import Base

# Configurar banco de dados de teste em memória
TEST_DATABASE_URL = "sqlite:///./test_clientes.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Criar tabelas
    Base.metadata.create_all(bind=engine)
    yield
    # Limpar após testes
    Base.metadata.drop_all(bind=engine)

def test_criar_cliente():
    response = client.post("/clientes", json={
        "nome": "João Silva",
        "telefone": 11999999999,
        "correntista": True,
        "score_credito": 5.0,
        "saldo_cc": 1000.0
    })
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "João Silva"
    assert data["telefone"] == 11999999999
    assert "id" in data

def test_criar_cliente_duplicado():
    # Primeiro, criar um cliente
    client.post("/clientes", json={
        "nome": "Maria Clara",
        "telefone": 11888888888,
        "correntista": True,
        "score_credito": 0,
        "saldo_cc": 1500
    })
    # Tentar criar outro com mesmo telefone
    response = client.post("/clientes", json={
        "nome": "Outro Nome",
        "telefone": 11888888888,
        "correntista": False,
        "score_credito": 1.0,
        "saldo_cc": 500
    })
    assert response.status_code == 409
    assert "já existe" in response.json()["detail"]

def test_listar_clientes():
    response = client.get("/clientes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1  # Pelo menos o criado acima

def test_buscar_cliente():
    # Assumindo que há um cliente com id 1
    response = client.get("/clientes/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_buscar_cliente_nao_encontrado():
    response = client.get("/clientes/999")
    assert response.status_code == 404

def test_atualizar_cliente():
    response = client.put("/clientes/1", json={
        "nome": "João Atualizado",
        "telefone": 11999999999,
        "correntista": True,
        "score_credito": 6.0,
        "saldo_cc": 1200.0
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "João Atualizado"

def test_deletar_cliente():
    response = client.delete("/clientes/1")
    assert response.status_code == 200
    assert response.json()["mensagem"] == "Cliente removido"

    # Verificar se foi deletado
    response = client.get("/clientes/1")
    assert response.status_code == 404
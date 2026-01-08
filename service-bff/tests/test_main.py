import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app import client

from app.schemas import ClienteResponse
client_test = TestClient(app)


# Dados mockados como ClienteResponse convertido para dict (garantindo tipos)
def make_cliente_dict(**kwargs):
    return ClienteResponse(
        id=kwargs.get("id", 1),
        nome=kwargs.get("nome", "João Silva"),
        telefone=kwargs.get("telefone", 11999999999),
        correntista=kwargs.get("correntista", True),
        score_credito=kwargs.get("score_credito", 5.0),
        saldo_cc=kwargs.get("saldo_cc", 1000.0)
    ).model_dump()
@patch("app.main.criar_cliente")
def test_criar_cliente_bff(mock_criar):
    mock_cliente = make_cliente_dict()
    mock_criar.return_value = mock_cliente
    response = client_test.post("/clientes", json={
        "nome": "João Silva",
        "telefone": 11999999999,
        "correntista": True,
        "score_credito": 5.0,
        "saldo_cc": 1000.0
    })
    print("criar_cliente_bff", response.json())
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "João Silva"

@patch("app.main.listar_clientes")
def test_listar_clientes_bff(mock_listar):
    mock_cliente = make_cliente_dict()
    mock_clientes_list = [mock_cliente]
    mock_listar.return_value = mock_clientes_list
    response = client_test.get("/clientes")
    print("listar_clientes_bff", response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1

@patch("app.main.buscar_cliente")
def test_buscar_cliente_bff(mock_buscar):
    mock_cliente = make_cliente_dict()
    mock_buscar.return_value = mock_cliente
    response = client_test.get("/clientes/1")
    print("buscar_cliente_bff", response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

@patch("app.main.buscar_cliente")
def test_buscar_cliente_nao_encontrado_bff(mock_buscar):
    mock_buscar.side_effect = Exception("Cliente não encontrado")
    response = client_test.get("/clientes/999")
    assert response.status_code == 400

@patch("app.main.atualizar_cliente")
def test_atualizar_cliente_bff(mock_atualizar):
    mock_atualizar.return_value = make_cliente_dict(nome="João Atualizado")
    response = client_test.put("/clientes/1", json={
        "nome": "João Atualizado",
        "telefone": 11999999999,
        "correntista": True,
        "score_credito": 5.0,
        "saldo_cc": 1000.0
    })
    print("atualizar_cliente_bff", response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "João Atualizado"

@patch("app.main.deletar_cliente")
def test_deletar_cliente_bff(mock_deletar):
    mock_deletar.return_value = {"mensagem": "Cliente removido"}
    response = client_test.delete("/clientes/1")
    print("deletar_cliente_bff", response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["mensagem"] == "Cliente removido"

@patch("app.main.buscar_cliente")
def test_calcular_score(mock_buscar):
    mock_cliente = make_cliente_dict()
    mock_buscar.return_value = mock_cliente
    response = client_test.get("/clientes/1/score")
    print("calcular_score", response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["cliente_id"] == 1
    assert data["score_calculado"] == mock_cliente["saldo_cc"] * 0.1
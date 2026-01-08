from fastapi import FastAPI, HTTPException
from typing import List
from app.client import (
    criar_cliente,
    buscar_cliente,
    listar_clientes,
    atualizar_cliente,
    deletar_cliente,
)
from app.schemas import ClienteCreate, ClienteResponse

app = FastAPI(title="Service BFF")


@app.post("/clientes", response_model=ClienteResponse, status_code=201, summary="Criar Cliente BFF")
def criar_cliente_bff(cliente: ClienteCreate):
    try:
        data = criar_cliente(cliente.model_dump())
        if isinstance(data, dict):
            return ClienteResponse(**data)
        return data
    except Exception as e:
        raise HTTPException(400, str(e))


@app.get("/clientes/{cliente_id}", response_model=ClienteResponse, summary="Buscar Cliente BFF")
def buscar_cliente_bff(cliente_id: int):
    try:
        data = buscar_cliente(cliente_id)
        if isinstance(data, dict):
            return ClienteResponse(**data)
        return data
    except Exception as e:
        raise HTTPException(400, str(e))


@app.get("/clientes", response_model=list[ClienteResponse], summary="Listar Clientes BFF")
def listar_clientes_bff():
    try:
        data = listar_clientes()
        if isinstance(data, list):
            return [ClienteResponse(**item) if isinstance(item, dict) else item for item in data]
        return data
    except Exception as e:
        raise HTTPException(400, str(e))


@app.put("/clientes/{cliente_id}", response_model=ClienteResponse, summary="Atualizar Cliente BFF")
def atualizar_cliente_bff(cliente_id: int, dados: ClienteCreate):
    try:
        data = atualizar_cliente(cliente_id, dados.model_dump())
        if isinstance(data, dict):
            return ClienteResponse(**data)
        return data
    except Exception as e:
        raise HTTPException(400, str(e))


@app.delete("/clientes/{cliente_id}", summary="Deletar Cliente BFF")
def deletar_cliente_bff(cliente_id: int):
    try:
        return deletar_cliente(cliente_id)
    except Exception as e:
        raise HTTPException(400, str(e))


@app.get("/clientes/{cliente_id}/score", summary="Calcular Score Cliente BFF")
def calcular_score(cliente_id: int):
    try:
        cliente = buscar_cliente(cliente_id)
        score = cliente["saldo_cc"] * 0.1
        return {
            "cliente_id": cliente_id,
            "score_calculado": score,
        }
    except Exception as e:
        raise HTTPException(400, str(e))

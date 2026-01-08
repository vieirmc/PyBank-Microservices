import requests

BASE_URL = "http://localhost:8001"


def criar_cliente(data):
    r = requests.post(f"{BASE_URL}/clientes", json=data)
    r.raise_for_status()
    return r.json()


def buscar_cliente(cliente_id):
    r = requests.get(f"{BASE_URL}/clientes/{cliente_id}")
    r.raise_for_status()
    return r.json()


def listar_clientes():
    r = requests.get(f"{BASE_URL}/clientes")
    r.raise_for_status()
    return r.json()


def atualizar_cliente(cliente_id, data):
    r = requests.put(f"{BASE_URL}/clientes/{cliente_id}", json=data)
    r.raise_for_status()
    return r.json()


def deletar_cliente(cliente_id):
    r = requests.delete(f"{BASE_URL}/clientes/{cliente_id}")
    r.raise_for_status()
    try:
        return r.json()
    except ValueError:
        return {"status_code": r.status_code}

# PyBank Microservices

Monorepo simples com duas aplicações FastAPI:

- `service-api` — serviço de domínio que provê CRUD de clientes usando SQLite.
- `service-bff` — BFF (backend-for-frontend) que expõe os mesmos endpoints do `service-api` e adiciona lógica de negócio (cálculo de score).

Visão geral

- O `service-api` mantém o banco SQLite `clientes.db` e oferece endpoints para criar, ler, atualizar e deletar clientes.
- O `service-bff` age como um cliente HTTP do `service-api`, expondo os mesmos endpoints e um endpoint adicional `/clientes/{id}/score` que calcula o score a partir do `saldo_cc`.

Requisitos

- Python 3.10+
- Instalar dependências em cada serviço (veja os `requirements.txt`).

Como executar

1. Inicie a API de domínio:

```bash
cd service-api
pip install -r requirements.txt
uvicorn app.main:app --port 8001 --reload
```

2. Inicie o BFF:

```bash
cd service-bff
pip install -r requirements.txt
uvicorn app.main:app --port 8000 --reload
```

Testes rápidos

- `service-api` padrão: http://localhost:8001
- `service-bff` padrão: http://localhost:8000

Veja os README específicos de cada serviço para exemplos de endpoints e comandos.

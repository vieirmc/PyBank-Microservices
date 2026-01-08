# Service BFF (service-bff)

Descrição

BFF que expõe os mesmos endpoints do `service-api` e aplica regras de negócio adicionais. Faz requests HTTP para a API de domínio em `http://localhost:8001`.

Tecnologias

- FastAPI
- requests

Como executar

```bash
cd service-bff
pip install -r requirements.txt
uvicorn app.main:app --port 8002 --reload
```

Endpoints expostos (proxy para `service-api`)

- `POST /clientes` — encaminha para `service-api` e retorna `201` em caso de sucesso.
- `GET /clientes` — lista todos os clientes (via `service-api`).
- `GET /clientes/{id}` — busca cliente por id (via `service-api`).
- `PUT /clientes/{id}` — atualiza cliente (via `service-api`).
- `DELETE /clientes/{id}` — deleta cliente (via `service-api`).

Endpoint de negócio

- `GET /clientes/{id}/score` — calcula um score simples a partir de `saldo_cc` recebido do `service-api` (regra: `score = saldo_cc * 0.1`).

Exemplos (curl)

Criar cliente via BFF:

```bash
curl -X POST http://localhost:8002/clientes \
  -H "Content-Type: application/json" \
  -d '{"nome":"João","telefone":11988888888,"correntista":false,"score_credito":0,"saldo_cc":500}'
```

Calcular score:

```bash
curl http://localhost:8002/clientes/1/score
```

Observações

- O BFF assume que a `service-api` está disponível em `http://localhost:8001`.
- Se desejar alterar o endereço, edite `service-bff/app/client.py` (variável `BASE_URL`).

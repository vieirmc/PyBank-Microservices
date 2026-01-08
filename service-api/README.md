# Service Domain — API (service-api)

Descrição

Serviço FastAPI responsável pelo CRUD de clientes, persistindo em `clientes.db` (SQLite).

Tecnologias

- FastAPI
- SQLAlchemy
- SQLite

Como executar

```bash
cd service-api
pip install -r requirements.txt
uvicorn app.main:app --port 8001 --reload
```

Endpoints

- `POST /clientes` — cria um cliente. Retorna `201` em criação bem-sucedida. Retorna `409` se já existir um cliente com o mesmo `telefone`.
- `GET /clientes` — lista todos os clientes.
- `GET /clientes/{id}` — busca cliente por id.
- `PUT /clientes/{id}` — atualiza cliente.
- `DELETE /clientes/{id}` — remove cliente.

Observações

- O campo `telefone` é usado para prevenir duplicatas (validação feita na camada da API; o arquivo SQLite continuará a aceitar valores distintos de id).
- Banco de dados: `clientes.db` criado no diretório do serviço.

Exemplos (curl)

Criar cliente:

```bash
curl -X POST http://localhost:8001/clientes \
  -H "Content-Type: application/json" \
  -d '{"nome":"Maria Clara","telefone":11999999999,"correntista":true,"score_credito":0,"saldo_cc":1500}'
```

Listar:

```bash
curl http://localhost:8001/clientes
```

Buscar por id:

```bash
curl http://localhost:8001/clientes/1
```

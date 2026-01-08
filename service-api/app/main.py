from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import Cliente
from .schemas import ClienteCreate, ClienteResponse

app = FastAPI(title="Service Domain API")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/clientes", response_model=ClienteResponse, status_code=201, summary="Criar Cliente API")
def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    # prevenir duplicatas pelo telefone
    existente = db.query(Cliente).filter(Cliente.telefone == cliente.telefone).first()
    if existente:
        raise HTTPException(status_code=409, detail="Cliente com este telefone já existe")

    novo = Cliente(**cliente.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@app.get("/clientes/{cliente_id}", response_model=ClienteResponse, summary="Buscar Cliente API")
def buscar(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(404, "Cliente não encontrado")
    return cliente

@app.get("/clientes", response_model=list[ClienteResponse], summary="Listar Clientes API")
def listar(db: Session = Depends(get_db)):
    return db.query(Cliente).all()

@app.put("/clientes/{cliente_id}", response_model=ClienteResponse, summary="Atualizar Cliente API")
def atualizar(cliente_id: int, dados: ClienteCreate, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(404, "Cliente não encontrado")

    for k, v in dados.model_dump().items():
        setattr(cliente, k, v)

    db.commit()
    db.refresh(cliente)
    return cliente

@app.delete("/clientes/{cliente_id}", summary="Deletar Cliente API")
def deletar(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(404, "Cliente não encontrado")

    db.delete(cliente)
    db.commit()
    return {"mensagem": "Cliente removido"}

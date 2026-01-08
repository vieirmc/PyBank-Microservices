from pydantic import BaseModel, ConfigDict

class ClienteBase(BaseModel):
    nome: str
    telefone: int
    correntista: bool
    score_credito: float
    saldo_cc: float

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

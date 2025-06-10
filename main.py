from fastapi import FastAPI

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Modelo Pydantic para validar a resposta
class Item(BaseModel):
    id: int
    nome: str
    preco: float

# Bd em memória
fake_items_db = {
    1: {"id": 1, "nome": "Caneta", "preco": 1.99},
    2: {"id": 2, "nome": "Caderno", "preco": 12.50},
}

# Endpoint para buscar um item por ID
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    item = fake_items_db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return item


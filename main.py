from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    id: int
    nome: str
    preco: float

# “Banco de dados” em memória
fake_items_db = {
    1: {"id": 1, "nome": "Caneta", "preco": 1.99},
    2: {"id": 2, "nome": "Caderno", "preco": 12.50},
}

# GET já existente
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    item = fake_items_db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return item


@app.post("/items/", response_model=Item, status_code=201)
async def create_item(item: Item):
    if item.id in fake_items_db:
        raise HTTPException(status_code=400, detail="ID já existe")
    fake_items_db[item.id] = item.dict()
    return item


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    if item_id != item.id:
        raise HTTPException(status_code=400, detail="O ID no corpo não confere com o parâmetro")
    fake_items_db[item_id] = item.dict()
    return item

@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    del fake_items_db[item_id]
    # 204 No Content → não retornamos nada


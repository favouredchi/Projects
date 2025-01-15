from fastapi import FastAPI, Path, Query, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session



app = FastAPI()

class Item(BaseModel):
    Name: str
    Price: float
    Brand: Optional[str] = None

class Updateitem(BaseModel):
    Name: Optional[str] = None
    Price: Optional[float] = None
    Brand: Optional[str] = None

Inventory = ['Milk', 'Tea', 'Rice', 'Bean', 'Soda']

# Get Item
@app.get("/items/{item_id}")
def get_item(item_id: int = Path(..., title="The ID of the item to get")):
    return {"item_id": item_id}

# Get Item by name
@app.get("/get_item_by_name.")
def get_item_by_name(name: str = Query(..., title="Name of the item to get")):
    for item in Inventory:
        if item == name:
            return {"item_name": item}
    raise HTTPException(status_code=400, detail="Item name does not exist")

# Create item
@app.post("/create_item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in Inventory:
        raise HTTPException(status_code=400, detail= "Item already exist.")
    Inventory[item_id] = item
    return Inventory[item_id]

# Update item
@app.put("/update_item")
def update_item(item_id: int, item: Updateitem):
    for item in Inventory:
        Inventory[item_id].updateItem
    if item_id not in Inventory:
        return HTTPException(status_code=400, detail= "item_id not found")

# delete item
@app.delete("/delete_item")
def delete_item(item_id: int = Query(..., title="The ID of the item to be deleted")):
    if item_id in Inventory:
        Inventory[item_id].delete
    return{"Success": "Item deleted"}
    raise HTTPException(status_code=400, detail="Item ID not found")
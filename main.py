WEB-
├── main.py
├── requirements.txt
└── public/
    └── index.html
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

items = []

class Item(BaseModel):
    name: str

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/items")
def get_items():
    return items

@app.post("/items")
def add_item(item: Item):
    items.append(item.name)
    return {"message": "added", "items": items}

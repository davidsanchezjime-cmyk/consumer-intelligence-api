from fastapi import FastAPI
from pydantic import BaseModel
import database

app = FastAPI()

class Producto(BaseModel):
    nombre: str
    precio: float
    categoria: str
    stock: int

@app.get("/productos")
def obtener_productos():
    return database.get_productos()

@app.get("/productos/{id}")
def obtener_producto(id: int):
    return database.get_producto(id)

@app.post("/productos")
def crear_producto(producto: Producto):
    nuevo_id = database.crear_producto(
        producto.nombre,
        producto.precio,
        producto.categoria,
        producto.stock
    )
    return {
        "id": nuevo_id,
        "nombre": producto.nombre,
        "precio": producto.precio,
        "categoria": producto.categoria,
        "stock": producto.stock,
        "mensaje": "Producto creado"
    }
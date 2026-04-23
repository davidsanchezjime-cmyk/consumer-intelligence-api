from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
import database
import pickle
import numpy as np
from scraper import obtener_datos_consumo
from auth import crear_token, verificar_usuario, Usuario, verificar_token

app = FastAPI()

with open('modelo.pkl', 'rb') as f:
    modelo = pickle.load(f)

class Producto(BaseModel):
    nombre: str
    precio: float
    categoria: str
    stock: int

def verificar_token_header(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token requerido")
    token = authorization.replace("Bearer ", "")
    if not verificar_token(token):
        raise HTTPException(status_code=401, detail="Token inválido")
    return token

@app.post("/login")
def login(usuario: Usuario):
    if verificar_usuario(usuario.username, usuario.password):
        token = crear_token({"sub": usuario.username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Credenciales inválidas")

@app.get("/productos")
def obtener_productos(token: str = Depends(verificar_token_header)):
    return database.get_productos()

@app.get("/productos/{id}")
def obtener_producto(id: int, token: str = Depends(verificar_token_header)):
    return database.get_producto(id)

@app.post("/productos")
def crear_producto(producto: Producto, token: str = Depends(verificar_token_header)):
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

@app.put("/productos/{id}")
def actualizar_producto(id: int, producto: Producto, token: str = Depends(verificar_token_header)):
    return database.actualizar_producto(id, producto.nombre, producto.precio, producto.categoria, producto.stock)

@app.delete("/productos/{id}")
def eliminar_producto(id: int, token: str = Depends(verificar_token_header)):
    return database.eliminar_producto(id)

@app.post("/predict")
def predecir(edad: int, ingresos: float, region: str = "CDMX", token: str = Depends(verificar_token_header)):
    datos = np.array([[edad, ingresos]])
    prediccion = modelo.predict(datos)[0]
    factor_region = {"CDMX": 1.2, "Monterrey": 1.1, "Guadalajara": 1.0, "Provincia": 0.8}
    prediccion_ajustada = prediccion * factor_region.get(region, 1.0)
    return {
        "edad": edad,
        "ingresos": ingresos,
        "region": region,
        "consumo_predicho": round(prediccion_ajustada, 2),
        "moneda": "MXN",
        "confianza": "85%"
    }

@app.get("/datos-consumo")
def datos_consumo_region(region: str = "CDMX", token: str = Depends(verificar_token_header)):
    datos = obtener_datos_consumo()
    return {
        "region": region,
        "datos": datos["regiones"].get(region, {}),
        "fecha_recoleccion": datos["fecha"]
    }
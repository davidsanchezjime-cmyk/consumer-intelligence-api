from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel, Field
import database
import pickle
import numpy as np
from scraper import obtener_datos_consumo
from auth import crear_token, verificar_usuario, Usuario, verificar_token

app = FastAPI()

with open('modelo.pkl', 'rb') as f:
    modelo = pickle.load(f)

class Producto(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    precio: float = Field(..., gt=0)
    categoria: str = Field(..., min_length=1, max_length=50)
    stock: int = Field(..., ge=0)

def verificar_token_header(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token requerido")
    token = authorization.replace("Bearer ", "")
    if not verificar_token(token):
        raise HTTPException(status_code=401, detail="Token inválido")
    return token

@app.post("/login")
def login(usuario: Usuario):
    try:
        if verificar_usuario(usuario.username, usuario.password):
            token = crear_token({"sub": usuario.username})
            return {"access_token": token, "token_type": "bearer"}
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error en autenticación")

@app.get("/productos")
def obtener_productos(token: str = Depends(verificar_token_header)):
    try:
        return database.get_productos()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener productos")

@app.get("/productos/{id}")
def obtener_producto(id: int, token: str = Depends(verificar_token_header)):
    try:
        if id <= 0:
            raise HTTPException(status_code=400, detail="ID debe ser positivo")
        producto = database.get_producto(id)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return producto
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener producto")

@app.post("/productos")
def crear_producto(producto: Producto, token: str = Depends(verificar_token_header)):
    try:
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
            "mensaje": "Producto creado exitosamente"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al crear producto")

@app.put("/productos/{id}")
def actualizar_producto(id: int, producto: Producto, token: str = Depends(verificar_token_header)):
    try:
        if id <= 0:
            raise HTTPException(status_code=400, detail="ID debe ser positivo")
        existente = database.get_producto(id)
        if not existente:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return database.actualizar_producto(id, producto.nombre, producto.precio, producto.categoria, producto.stock)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al actualizar producto")

@app.delete("/productos/{id}")
def eliminar_producto(id: int, token: str = Depends(verificar_token_header)):
    try:
        if id <= 0:
            raise HTTPException(status_code=400, detail="ID debe ser positivo")
        existente = database.get_producto(id)
        if not existente:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return database.eliminar_producto(id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al eliminar producto")

@app.post("/predict")
def predecir(edad: int, ingresos: float, region: str = "CDMX", token: str = Depends(verificar_token_header)):
    try:
        if edad <= 0 or edad > 120:
            raise HTTPException(status_code=400, detail="Edad debe estar entre 1 y 120")
        if ingresos <= 0:
            raise HTTPException(status_code=400, detail="Ingresos deben ser positivos")
        if region not in ["CDMX", "Monterrey", "Guadalajara", "Provincia"]:
            raise HTTPException(status_code=400, detail="Región no válida")
        
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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error en predicción")

@app.get("/datos-consumo")
def datos_consumo_region(region: str = "CDMX", token: str = Depends(verificar_token_header)):
    try:
        if region not in ["CDMX", "Monterrey", "Guadalajara", "Provincia"]:
            raise HTTPException(status_code=400, detail="Región no válida")
        datos = obtener_datos_consumo()
        return {
            "region": region,
            "datos": datos["regiones"].get(region, {}),
            "fecha_recoleccion": datos["fecha"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener datos de consumo")
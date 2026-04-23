from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel

SECRET_KEY = "tu_clave_secreta_cambia_esto_en_produccion"
ALGORITHM = "HS256"

class Usuario(BaseModel):
    username: str
    password: str

def crear_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None

usuarios_db = {
    "demo": "demo123"
}

def verificar_usuario(username: str, password: str):
    if username in usuarios_db:
        if usuarios_db[username] == password:
            return True
    return False
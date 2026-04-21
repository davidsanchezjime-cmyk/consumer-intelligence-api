import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="consumer_db",
        user="davidsanchez",
        password=""
    )

def get_productos():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM productos")
    r = cursor.fetchall()
    cursor.close()
    conn.close()
    return r

def get_producto(id: int):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
    r = cursor.fetchone()
    cursor.close()
    conn.close()
    return r

def crear_producto(n: str, p: float, c: str, s: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, precio, categoria, stock) VALUES (%s, %s, %s, %s) RETURNING id", (n, p, c, s))
    nid = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return nid
    
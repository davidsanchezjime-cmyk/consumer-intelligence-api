import psycopg2

# Conectar a PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="consumer_db",
    user="davidsanchez",
    password=""
)

# Crear cursor
cursor = conn.cursor()

# Ejecutar consulta
cursor.execute("SELECT * FROM productos")

# Obtener resultados
resultados = cursor.fetchall()

# Mostrar resultados
for fila in resultados:
    print(fila)

# Cerrar
cursor.close()
conn.close()

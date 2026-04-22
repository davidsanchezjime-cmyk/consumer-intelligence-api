import requests
import json
from datetime import datetime
import database

def recolectar_datos_consumo():
    """
    Simula recolección de datos de consumo de múltiples fuentes
    Después conectarás fuentes reales (INEGI, APIs públicas, etc)
    """
    
    datos = {
        "fecha": datetime.now().isoformat(),
        "regiones": {
            "CDMX": {"consumo_promedio": 750, "edad_promedio": 35, "ingresos_promedio": 3500},
            "Monterrey": {"consumo_promedio": 680, "edad_promedio": 32, "ingresos_promedio": 3200},
            "Guadalajara": {"consumo_promedio": 620, "edad_promedio": 30, "ingresos_promedio": 2800},
            "Provincia": {"consumo_promedio": 450, "edad_promedio": 28, "ingresos_promedio": 2200}
        }
    }
    
    # Guardar en archivo JSON
    with open('datos_consumo.json', 'w') as f:
        json.dump(datos, f, indent=2)
    
    print(f"✓ Datos recolectados: {datetime.now()}")
    return datos

def obtener_datos_consumo():
    """Lee datos de consumo guardados"""
    try:
        with open('datos_consumo.json', 'r') as f:
            return json.load(f)
    except:
        return recolectar_datos_consumo()

if __name__ == "__main__":
    datos = recolectar_datos_consumo()
    print(json.dumps(datos, indent=2))
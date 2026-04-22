import numpy as np
from sklearn.linear_model import LinearRegression
import pickle

# Datos sintéticos: edad, ingresos mensuales → consumo mensual
X = np.array([
    [25, 2000], [30, 2500], [35, 3000], [40, 3500], [45, 4000],
    [50, 4500], [55, 5000], [60, 5500], [65, 6000], [28, 2300],
    [32, 2800], [38, 3300], [42, 3800], [48, 4300], [52, 4800]
])

y = np.array([500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 550, 650, 750, 850, 950, 1050])

# Entrenar modelo
model = LinearRegression()
model.fit(X, y)

# Guardar modelo
with open('modelo.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Modelo entrenado y guardado")

# Prueba
prueba = np.array([[30, 2500]])
prediccion = model.predict(prueba)
print(f"Predicción para edad 30, ingresos $2500: ${prediccion[0]:.2f}")

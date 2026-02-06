import numpy as np
import pandas as pd
import tensorflow as tf
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

app = FastAPI()

# Configuración CORS (Para que Vue pueda hablar con Python)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 1. LÓGICA DE ENTRENAMIENTO (Se ejecuta al iniciar el servidor) ---
# Copiamos tu función de generación de datos para entrenar el scaler y el modelo
print("Inicializando Motor Guardian AI...")

def generar_datos_sensores(n_muestras=2000):
    np.random.seed(42)
    horas_uso = np.random.randint(100, 50000, n_muestras)
    temperatura = np.random.normal(55, 15, n_muestras)
    errores_lectura = np.random.exponential(10, n_muestras)
    sectores_dañados = np.random.poisson(2, n_muestras)
    
    data = pd.DataFrame({
        'horas_uso': horas_uso,
        'temperatura': temperatura,
        'errores_lectura': errores_lectura,
        'sectores_dañados': sectores_dañados
    })
    
    # Lógica de falla
    prob = (data['horas_uso']/50000)*0.4 + (data['temperatura']/100)*0.3 + (data['sectores_dañados']/20)*0.8
    data['va_a_fallar'] = (prob > np.random.uniform(0.4, 0.6, n_muestras)).astype(int)
    return data

# Preparamos el modelo globalmente
df = generar_datos_sensores()
X = df.drop('va_a_fallar', axis=1)
y = df['va_a_fallar']

# IMPORTANTE: Guardamos el scaler para usarlo con los datos nuevos que lleguen de Vue
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(4,)),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_scaled, y, epochs=10, batch_size=32, verbose=0)
print("Modelo Entrenado y Listo.")

# --- 2. DEFINICIÓN DE DATOS (Lo que Vue nos enviará) ---
class SensorData(BaseModel):
    horas_uso: float      # [cite: 11]
    temperatura: float    # [cite: 12]
    errores_lectura: float # [cite: 13]
    sectores_dañados: float # 

# --- 3. ENDPOINT DE PREDICCIÓN ---
@app.post("/predict")
def predict_failure(data: SensorData):
    # 1. Convertir JSON a DataFrame
    input_data = pd.DataFrame([[
        data.horas_uso, 
        data.temperatura, 
        data.errores_lectura, 
        data.sectores_dañados
    ]], columns=['horas_uso', 'temperatura', 'errores_lectura', 'sectores_dañados'])
    
    # 2. Escalar usando el MISMO scaler del entrenamiento
    input_scaled = scaler.transform(input_data)
    
    # 3. Predecir
    prediction = model.predict(input_scaled)
    probabilidad = float(prediction[0][0])
    
    return {
        "probabilidad_falla": probabilidad,
        "estado": "CRITICO" if probabilidad > 0.5 else "OPERATIVO",
        "accion": "Reemplazo Inmediato" if probabilidad > 0.5 else "Ninguna" # [cite: 65]
    }
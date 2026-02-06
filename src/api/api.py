import numpy as np
import pandas as pd
import tensorflow as tf
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.preprocessing import StandardScaler
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime

# ==========================================
# 1. CONFIGURACIÓN DE BASE DE DATOS (SQLite)
# ==========================================
SQLALCHEMY_DATABASE_URL = "sqlite:///./guardian.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definimos la Tabla "historial"
class RegistroPrediccion(Base):
    __tablename__ = "historial"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, default=datetime.now)
    horas_uso = Column(Integer)
    temperatura = Column(Float)
    errores = Column(Integer)
    sectores = Column(Integer)
    probabilidad = Column(Float)
    estado = Column(String)

# Crea el archivo de base de datos si no existe
Base.metadata.create_all(bind=engine)

# Dependencia para obtener la sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# 2. APP Y MODELO TENSORFLOW
# ==========================================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- RE-ENTRENAMIENTO (Simplificado para el ejemplo) ---
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
    
    prob = (data['horas_uso']/50000)*0.4 + (data['temperatura']/100)*0.3 + (data['sectores_dañados']/20)*0.8
    data['va_a_fallar'] = (prob > np.random.uniform(0.4, 0.6, n_muestras)).astype(int)
    return data

df = generar_datos_sensores()
X = df.drop('va_a_fallar', axis=1)
y = df['va_a_fallar']
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(4,)),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_scaled, y, epochs=5, verbose=0)
print("✅ Motor Guardian AI + Base de Datos SQL: LISTO")

# ==========================================
# 3. ENDPOINTS
# ==========================================

class SensorData(BaseModel):
    horas_uso: float
    temperatura: float
    errores_lectura: float
    sectores_dañados: float

@app.post("/predict")
def predict_failure(data: SensorData, db: Session = Depends(get_db)):
    # 1. Predecir
    input_data = pd.DataFrame([[data.horas_uso, data.temperatura, data.errores_lectura, data.sectores_dañados]], 
                              columns=['horas_uso', 'temperatura', 'errores_lectura', 'sectores_dañados'])
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)
    probabilidad = float(prediction[0][0])
    
    estado_str = "CRITICO" if probabilidad > 0.5 else "OPERATIVO"

    # 2. GUARDAR EN BASE DE DATOS (Mágicamente con SQLAlchemy)
    nuevo_registro = RegistroPrediccion(
        horas_uso=int(data.horas_uso),
        temperatura=data.temperatura,
        errores=int(data.errores_lectura),
        sectores=int(data.sectores_dañados),
        probabilidad=probabilidad,
        estado=estado_str
    )
    db.add(nuevo_registro)
    db.commit() # Guarda cambios
    db.refresh(nuevo_registro) # Obtiene el ID generado

    return {
        "id_reporte": nuevo_registro.id,
        "probabilidad_falla": probabilidad,
        "estado": estado_str,
        "accion": "Reemplazo Inmediato" if probabilidad > 0.5 else "Ninguna"
    }

@app.get("/historial")
def leer_historial(db: Session = Depends(get_db)):
    # Obtiene los últimos 10 registros, ordenados del más nuevo al más viejo
    registros = db.query(RegistroPrediccion).order_by(RegistroPrediccion.id.desc()).limit(10).all()
    return registros
# 🚀 TechJulio Solutions | Guardian AI Platform

Plataforma Full-Stack para una empresa proveedora de soluciones tecnológicas integrales. Combina un modelo de negocio de **Hardware as a Service (HaaS)**, estimación de proyectos de **Software a Medida**, y un **Dashboard de Mantenimiento Predictivo impulsado por Inteligencia Artificial (Guardian AI)**.

## 📌 Descripción del Proyecto

TechJulio Solutions no es solo un portal de ventas, es un ecosistema interactivo que permite a los clientes corporativos:
1. Cotizar leasing de hardware de alta gama ajustando especificaciones en tiempo real.
2. Estimar presupuestos para desarrollo de software ágil (Scrum) basado en módulos y plataformas.
3. Monitorear la salud de sus equipos físicos a través de **Guardian AI**, un modelo de Machine Learning que analiza telemetría simulada (temperatura, uso, errores S.M.A.R.T) para predecir fallas críticas con antelación.

## ✨ Características Principales

* **Landing Page Corporativa:** Interfaz moderna y adaptable que presenta los servicios, partners y propuesta de valor.
* **Cotizadores Dinámicos:** Vistas reactivas para configurar hardware y software, calculando costos automáticamente y añadiendo las solicitudes a una base de datos.
* **Motor Guardian AI (TensorFlow):** Red neuronal que evalúa métricas de hardware y determina la probabilidad de falla inminente.
* **Dashboard de Telemetría:** Panel de control con gráficos en tiempo real (Chart.js) que muestran el estrés del dispositivo y el historial de la sesión.
* **Gestión de Pedidos (CRUD):** Historial persistente en base de datos SQLite donde los clientes pueden revisar el estado de sus solicitudes e intervenciones de la IA.

## 🛠️ Stack Tecnológico

**Frontend (Client-Side)**
* [Vue.js 3](https://vuejs.org/) (Composition API)
* [Chart.js](https://www.chartjs.org/) & [vue-chartjs](https://vue-chartjs.org/) (Visualización de datos)
* CSS3 puro (Diseño Dark Mode responsivo y UI corporativa)

**Backend (Server-Side & AI)**
* [Python 3](https://www.python.org/)
* [FastAPI](https://fastapi.tiangolo.com/) (API REST rápida y asíncrona)
* [TensorFlow](https://www.tensorflow.org/) & Keras (Entrenamiento y predicción de la Red Neuronal)
* [Scikit-Learn](https://scikit-learn.org/) / Pandas (Preprocesamiento de datos y escalado)

**Base de Datos**
* [SQLite](https://www.sqlite.org/) (Persistencia ligera)
* [SQLAlchemy](https://www.sqlalchemy.org/) (ORM para gestión de datos)

## ⚙️ Instalación y Ejecución Local

El proyecto está dividido en dos partes que deben ejecutarse en paralelo: el servidor Backend (Python) y el cliente Frontend (Node/Vue).

### 1. Configuración del Backend (Terminal 1)
Asegúrate de tener Python instalado. Navega a la carpeta del backend (donde está `api.py`).

```bash
# Opcional: Crear un entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install fastapi uvicorn pydantic scikit-learn tensorflow pandas sqlalchemy

# Ejecutar el servidor (se iniciará en http://127.0.0.1:8000)
uvicorn api:app --reload
```

*Nota: Al iniciar por primera vez, el modelo de TensorFlow se entrenará automáticamente con datos sintéticos y se creará el archivo `guardian.db`.*

### 2. Configuración del Frontend (Terminal 2)

Asegúrate de tener Node.js instalado. Navega a la carpeta del frontend (donde está el `package.json`).

```bash
# Instalar dependencias de Vue y Chart.js
npm install
npm install chart.js vue-chartjs

# Ejecutar el servidor de desarrollo
npm run dev
```

Abre tu navegador en la dirección que te indique la consola (usualmente `http://localhost:5173`).

## 🧠 Arquitectura de Guardian AI

El modelo de mantenimiento predictivo es un clasificador binario. Utiliza una arquitectura de red neuronal secuencial con capas densas y Dropout para evitar el sobreajuste.

* **Inputs:** Horas de uso, Temperatura CPU, Tasa de errores de lectura, Sectores reasignados.
* **Output:** Probabilidad (0.0 a 1.0) de falla inminente.

## 👨‍💻 Autor

**Julio Romero** Ingeniero en Informática

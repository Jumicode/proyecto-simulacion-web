<template>
  <div id="app" :class="isDarkMode ? 'dark-mode' : ''">
    
    <div v-if="!servicioAdquirido" class="landing-container">
      <h1>TechNova Guardian AI</h1>
      <p class="subtitle">Mantenimiento Predictivo Hardware as a Service</p>
      
      <div class="pricing-card">
        <h2>Plan Enterprise</h2>
        <ul>
          <li> Monitoreo 24/7</li>
          <li> IA Predictiva (TensorFlow)</li>
          <li> Reducción de Costos Logísticos</li>
        </ul>
        <button @click="adquirirServicio" class="btn-primary">
          Activar Servicio HaaS
        </button>
      </div>
    </div>

    <div v-else class="dashboard-container">
      <header>
        <h2>🩺 Monitor de Flota Activa</h2>
        <button @click="servicioAdquirido = false" class="btn-small">Salir</button>
      </header>

      <div class="grid-control">
        <div class="card control-panel">
          <h3>📡 Simular Telemetría</h3>
          
          <label>Horas de Uso: {{ sensores.horas_uso }} hrs</label>
          <input type="range" v-model.number="sensores.horas_uso" min="0" max="50000">
          
          <label>Temperatura CPU: {{ sensores.temperatura }} °C</label>
          <input type="range" v-model.number="sensores.temperatura" min="20" max="100">
          
          <label>Errores de Lectura: {{ sensores.errores_lectura }}</label>
          <input type="range" v-model.number="sensores.errores_lectura" min="0" max="100">
          
          <label>Sectores Dañados (S.M.A.R.T): {{ sensores.sectores_dañados }}</label>
          <input type="range" v-model.number="sensores.sectores_dañados" min="0" max="50">
          
          <button @click="analizarEstado" class="btn-analyze" :disabled="loading">
            {{ loading ? 'Analizando...' : 'ANALIZAR CON IA' }}
          </button>
        </div>

        <div class="card result-panel" :class="claseEstado">
          <h3>Estado del Activo</h3>
          
          <div v-if="resultado" class="result-content">
            <div class="indicator">
              <span class="big-text">{{ (resultado.probabilidad_falla * 100).toFixed(2) }}%</span>
              <small>Probabilidad de Falla</small>
            </div>
            
            <div class="status-badge">
              {{ resultado.estado }}
            </div>
            
            <p><strong>Acción Recomendada:</strong> {{ resultado.accion }}</p>
          </div>
          
          <div v-else class="waiting">
            <p>Esperando datos de sensores...</p>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const servicioAdquirido = ref(false);
const loading = ref(false);
const resultado = ref(null);

// Datos iniciales de sensores (Simulación)
const sensores = ref({
  horas_uso: 500,        // [cite: 33] Caso Equipo Nuevo
  temperatura: 40,
  errores_lectura: 0,
  sectores_dañados: 0
});

const adquirirServicio = () => {
  servicioAdquirido.value = true;
};

const analizarEstado = async () => {
  loading.value = true;
  try {
    // Petición a tu API Python
    const response = await fetch('http://127.0.0.1:8080/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(sensores.value)
    });
    
    const data = await response.json();
    resultado.value = data;
    
  } catch (error) {
    console.error("Error conectando con Guardian AI:", error);
    alert("Error: Asegúrate de que api.py esté corriendo.");
  } finally {
    loading.value = false;
  }
};

// Estilo dinámico según riesgo
const claseEstado = computed(() => {
  if (!resultado.value) return '';
  return resultado.value.estado === 'CRITICO' ? 'risk-critical' : 'risk-safe';
});
</script>

<style scoped>
/* Estilos básicos oscuros "TechNova" */
#app {
  font-family: 'Segoe UI', sans-serif;
  color: #e0e0e0;
  background-color: #121212;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.landing-container { text-align: center; }
.pricing-card {
  background: #1e1e1e;
  padding: 2rem;
  border-radius: 12px;
  border: 1px solid #333;
  margin-top: 20px;
}

.dashboard-container { width: 90%; max-width: 800px; }
.grid-control { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }
.card { background: #1e1e1e; padding: 20px; border-radius: 10px; }

input[type=range] { width: 100%; margin-bottom: 15px; }
label { display: block; margin-bottom: 5px; color: #aaa; font-size: 0.9em; }

.btn-primary, .btn-analyze {
  background: #4caf50; color: white; border: none; padding: 10px 20px;
  border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%;
}
.btn-analyze:hover { background: #45a049; }

/* Estados Visuales */
.risk-critical { border: 2px solid #ff4444; box-shadow: 0 0 15px rgba(255, 68, 68, 0.3); }
.risk-safe { border: 2px solid #00c853; box-shadow: 0 0 15px rgba(0, 200, 83, 0.3); }

.big-text { font-size: 3em; font-weight: bold; display: block; }
.status-badge {
  background: #333; padding: 5px 10px; border-radius: 4px;
  display: inline-block; margin: 10px 0; font-weight: bold;
}
.risk-critical .status-badge { background: #ff4444; color: white; }
.risk-safe .status-badge { background: #00c853; color: white; }
</style>
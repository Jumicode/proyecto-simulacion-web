<template>
  <div class="dashboard-wrapper">
    <header class="dash-header">
      <div class="logo-small" @click="$emit('navegar', 'home')">
        ← Volver a TechJulio
      </div>
      <div class="user-profile">Cliente: <strong>Corp Beta</strong></div>
    </header>

    <div class="dashboard-container">
      
      <div class="grid-control">
        
        <div class="card control-panel">
          <h3>📡 Telemetría en Tiempo Real</h3>
          
          <div class="input-group">
            <label>Horas de Uso: <strong>{{ sensores.horas_uso }} hrs</strong></label>
            <input type="range" v-model.number="sensores.horas_uso" min="0" max="50000" class="slider">
          </div>
          
          <div class="input-group">
            <label>Temp CPU: <strong>{{ sensores.temperatura }}°C</strong></label>
            <input type="range" v-model.number="sensores.temperatura" min="20" max="100" class="slider">
          </div>
          
          <div class="input-group">
            <label>Errores Lectura: <strong>{{ sensores.errores_lectura }}</strong></label>
            <input type="range" v-model.number="sensores.errores_lectura" min="0" max="100" class="slider">
          </div>

          <div class="input-group">
            <label>Sectores Dañados: <strong>{{ sensores.sectores_dañados }}</strong></label>
            <input type="range" v-model.number="sensores.sectores_dañados" min="0" max="50" class="slider critical-slider">
          </div>

          <button @click="analizarEstado" class="btn-analyze" :disabled="loading">
            {{ loading ? 'Procesando Tensor...' : 'EJECUTAR DIAGNÓSTICO IA' }}
          </button>
        </div>

        <div class="card chart-panel">
          <h3>🔍 Huella del Dispositivo</h3>
          <div class="chart-container-radar">
            <Radar v-if="radarData.labels" :data="radarData" :options="radarOptions" />
            <p v-else class="waiting-text">Ejecuta un diagnóstico para ver la huella.</p>
          </div>
        </div>
      </div>

      <div class="history-section card">
        <div class="history-header">
          <h3>📈 Historial de Monitoreo (Sesión Actual)</h3>
          <div v-if="resultado" :class="['badge-large', claseEstado]">
            Riesgo Actual: {{ (resultado.probabilidad_falla * 100).toFixed(1) }}%
          </div>
        </div>
        
        <div class="chart-container-line">
          <Line :data="historyData" :options="lineOptions" />
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  Title
} from 'chart.js';
import { Radar, Line } from 'vue-chartjs';

ChartJS.register(
  RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend, 
  CategoryScale, LinearScale, Title
);

const emit = defineEmits(['navegar']);

// --- ESTADO ---
const loading = ref(false);
const resultado = ref(null);
const checkCount = ref(0);

// Inputs de sensores (Estos SÍ deben ser reactivos para los sliders)
const sensores = ref({ 
  horas_uso: 500, 
  temperatura: 45, 
  errores_lectura: 0, 
  sectores_dañados: 0 
});

// --- SOLUCIÓN: ARRAYS NATIVOS (SIN REACTIVIDAD) ---
// Al quitar 'ref', Vue deja de vigilar cada push dentro de estos arrays.
// Esto elimina la recursión infinita.
const rawLabels = [];
const rawProb = [];
const rawTemp = [];

// --- CONFIGURACIÓN DEL GRÁFICO ---
// Usamos un ref para el objeto de datos COMPLETO.
// Chart.js solo reaccionará cuando reemplacemos este objeto entero.
const historyData = ref({
  labels: [],
  datasets: [
    {
      label: 'Probabilidad de Falla (%)',
      backgroundColor: '#4e8cff',
      borderColor: '#4e8cff',
      data: [],
      tension: 0.4
    },
    {
      label: 'Temperatura (°C)',
      backgroundColor: '#ff9800',
      borderColor: '#ff9800',
      data: [],
      borderDash: [5, 5]
    }
  ]
});

// Radar Data (Ref simple)
const radarData = ref({ labels: [], datasets: [] });

const lineOptions = {
  responsive: true,
  maintainAspectRatio: false,
  animation: false, // Desactivar animación evita conflictos en actualizaciones rápidas
  scales: {
    y: { beginAtZero: true, grid: { color: '#333' } },
    x: { grid: { color: '#333' } }
  },
  plugins: { legend: { labels: { color: 'white' } } }
};

const radarOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    r: {
      angleLines: { color: '#444' },
      grid: { color: '#333' },
      pointLabels: { color: 'white', font: { size: 12 } },
      suggestedMin: 0,
      suggestedMax: 100
    }
  },
  plugins: { legend: { display: false } }
};

// --- LÓGICA DE NEGOCIO ---
const analizarEstado = async () => {
  loading.value = true;
  checkCount.value++;
  
  try {
    const response = await fetch('http://127.0.0.1:8000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(sensores.value)
    });
    
    if (!response.ok) throw new Error("API Error");
    resultado.value = await response.json();
    
  } catch (error) {
    const prob = (sensores.value.horas_uso/50000 * 0.4) + 
                 (sensores.value.temperatura/100 * 0.3) + 
                 (sensores.value.sectores_dañados/20 * 0.8);
    const finalProb = Math.min(prob, 1.0);
    
    resultado.value = {
      probabilidad_falla: finalProb,
      estado: finalProb > 0.5 ? "CRITICO" : "OPERATIVO",
      accion: finalProb > 0.5 ? "Reemplazo" : "Ninguna"
    };
  } finally {
    loading.value = false;
    actualizarGraficos();
  }
};

const actualizarGraficos = () => {
  const probPercent = (resultado.value.probabilidad_falla * 100).toFixed(1);
  
  // 1. Modificamos los arrays NATIVOS (Vue no se entera, no hay error)
  rawLabels.push(`Check #${checkCount.value}`);
  rawProb.push(probPercent);
  rawTemp.push(sensores.value.temperatura);
  
  // Limitar historial a 10
  if(rawLabels.length > 10) {
    rawLabels.shift();
    rawProb.shift();
    rawTemp.shift();
  }

  // 2. SOLUCIÓN FINAL: Reemplazamos el objeto del gráfico ENTERO.
  // Usamos el operador Spread [...] para crear COPIAS de los arrays.
  // Así Chart.js recibe datos frescos y Vue detecta el cambio en 'historyData'.
  historyData.value = {
    labels: [...rawLabels], 
    datasets: [
      {
        label: 'Probabilidad de Falla (%)',
        backgroundColor: '#4e8cff',
        borderColor: '#4e8cff',
        data: [...rawProb], // Copia
        tension: 0.4
      },
      {
        label: 'Temperatura (°C)',
        backgroundColor: '#ff9800',
        borderColor: '#ff9800',
        data: [...rawTemp], // Copia
        borderDash: [5, 5]
      }
    ]
  };

  // Actualizar Radar
  radarData.value = {
    labels: ['Uso', 'Temp', 'Errores I/O', 'Sectores'],
    datasets: [{
      label: 'Estrés',
      backgroundColor: 'rgba(78, 140, 255, 0.2)',
      borderColor: '#4e8cff',
      pointBackgroundColor: '#fff',
      data: [
        (sensores.value.horas_uso / 50000) * 100,
        sensores.value.temperatura,
        sensores.value.errores_lectura,
        (sensores.value.sectores_dañados / 50) * 100
      ]
    }]
  };
};

const claseEstado = computed(() => 
  resultado.value?.estado === 'CRITICO' ? 'risk-critical' : 'risk-safe'
);
</script>

<style scoped>
/* Estilos Base Dark Mode */
.dashboard-wrapper { background: #0f1115; min-height: 100vh; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; }
.dash-header { padding: 1rem 2rem; background: #161920; display: flex; justify-content: space-between; border-bottom: 1px solid #2a2e35; align-items: center; }
.logo-small { cursor: pointer; color: #4e8cff; font-weight: bold; }
.logo-small:hover { color: #fff; }

.dashboard-container { max-width: 1000px; margin: 2rem auto; padding: 0 20px; }

/* Grid Principal */
.grid-control { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
.card { background: #1f232b; padding: 20px; border-radius: 12px; border: 1px solid #2a2e35; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }

/* Inputs */
.input-group { margin-bottom: 15px; }
.input-group label { display: flex; justify-content: space-between; font-size: 0.85rem; color: #aaa; margin-bottom: 5px; }
.slider { width: 100%; -webkit-appearance: none; background: #333; height: 5px; border-radius: 3px; outline: none; }
.slider::-webkit-slider-thumb { -webkit-appearance: none; width: 16px; height: 16px; background: #4e8cff; border-radius: 50%; cursor: pointer; transition: 0.2s; }
.slider:hover::-webkit-slider-thumb { transform: scale(1.2); }
.critical-slider::-webkit-slider-thumb { background: #ff4444; }

.btn-analyze { width: 100%; padding: 12px; margin-top: 10px; background: linear-gradient(45deg, #4e8cff, #2962ff); color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; transition: 0.3s; }
.btn-analyze:hover { filter: brightness(1.2); transform: translateY(-1px); }
.btn-analyze:disabled { opacity: 0.6; cursor: wait; }

/* Gráficos */
.chart-container-radar { position: relative; height: 250px; display: flex; align-items: center; justify-content: center; }
.chart-container-line { position: relative; height: 300px; width: 100%; }
.waiting-text { color: #555; font-style: italic; }

.history-section { margin-top: 20px; }
.history-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }

/* Badges de Estado */
.badge-large { padding: 5px 15px; border-radius: 6px; font-weight: bold; color: white; }
.risk-critical { background-color: rgba(255, 68, 68, 0.2); border: 1px solid #ff4444; color: #ff4444; }
.risk-safe { background-color: rgba(0, 200, 83, 0.2); border: 1px solid #00c853; color: #00c853; }
</style>
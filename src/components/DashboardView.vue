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
            <Radar v-if="radarData.datasets.length > 0" :data="radarData" :options="radarOptions" />
            <p v-else class="waiting-text">Ejecuta un diagnóstico para ver la huella.</p>
          </div>
        </div>
      </div>

      <div class="history-section card">
        <div class="history-header">
          <h3>📈 Tendencia en Vivo (Sesión Actual)</h3>
          <div v-if="resultado" :class="['badge-large', claseEstado]">
            Riesgo Actual: {{ (resultado.probabilidad_falla * 100).toFixed(1) }}%
          </div>
        </div>
        
        <div class="chart-container-line">
          <Line :data="historyData" :options="lineOptions" />
        </div>
      </div>

      <div class="history-table-section card">
        <h3>🗄️ Historial de Reportes (Base de Datos)</h3>
        <div class="table-responsive">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Hora</th>
                <th>Estado</th>
                <th>Probabilidad</th>
                <th>Temp</th>
                <th>Sectores</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in listaHistorial" :key="item.id">
                <td>#{{ item.id }}</td>
                <td>{{ formatearFecha(item.fecha) }}</td>
                <td>
                  <span :class="['badge-small', item.estado === 'CRITICO' ? 'bg-red' : 'bg-green']">
                    {{ item.estado }}
                  </span>
                </td>
                <td>{{ (item.probabilidad * 100).toFixed(1) }}%</td>
                <td>{{ item.temperatura.toFixed(1) }}°C</td>
                <td>{{ item.sectores }}</td>
              </tr>
            </tbody>
          </table>
          <p v-if="listaHistorial.length === 0" class="empty-msg">No hay registros guardados aún.</p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import {
  Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend, CategoryScale, LinearScale, Title
} from 'chart.js';
import { Radar, Line } from 'vue-chartjs';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend, CategoryScale, LinearScale, Title);

const emit = defineEmits(['navegar']);

// --- ESTADO ---
const loading = ref(false);
const resultado = ref(null);
const checkCount = ref(0);
const listaHistorial = ref([]); // Datos de la tabla

const sensores = ref({ 
  horas_uso: 500, temperatura: 45, errores_lectura: 0, sectores_dañados: 0 
});

// --- ARRAYS NATIVOS PARA EL GRÁFICO DE LÍNEA (Evita Recursión) ---
const rawLabels = [];
const rawProb = [];
const rawTemp = [];

// --- CONFIG GRÁFICOS ---
const historyData = ref({
  labels: [],
  datasets: [
    { label: 'Probabilidad de Falla (%)', backgroundColor: '#4e8cff', borderColor: '#4e8cff', data: [], tension: 0.4 },
    { label: 'Temperatura (°C)', backgroundColor: '#ff9800', borderColor: '#ff9800', data: [], borderDash: [5, 5] }
  ]
});

const radarData = ref({ labels: [], datasets: [] });

const lineOptions = {
  responsive: true, maintainAspectRatio: false, animation: false,
  scales: { y: { beginAtZero: true, grid: { color: '#333' } }, x: { grid: { color: '#333' } } },
  plugins: { legend: { labels: { color: 'white' } } }
};

const radarOptions = {
  responsive: true, maintainAspectRatio: false,
  scales: { r: { angleLines: { color: '#444' }, grid: { color: '#333' }, pointLabels: { color: 'white' }, suggestedMin: 0, suggestedMax: 100 } },
  plugins: { legend: { display: false } }
};

// --- LÓGICA DE NEGOCIO ---

// 1. Cargar la tabla al iniciar
const cargarHistorial = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/historial');
    if(res.ok) listaHistorial.value = await res.json();
  } catch (e) { console.error("Error cargando BD (¿Backend apagado?)", e); }
};

// 2. Analizar, Guardar y Actualizar Todo
const analizarEstado = async () => {
  loading.value = true;
  checkCount.value++;
  
  try {
    // A. Petición al Backend (Predicción + Guardado en BD)
    const response = await fetch('http://127.0.0.1:8000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(sensores.value)
    });
    
    if (!response.ok) throw new Error("API Error");
    resultado.value = await response.json();

    // B. Recargar la tabla con el nuevo dato
    await cargarHistorial();
    
  } catch (error) {
    // Fallback Simulación (Si el backend falla, los gráficos siguen funcionando)
    const prob = (sensores.value.horas_uso/50000 * 0.4) + (sensores.value.temperatura/100 * 0.3) + (sensores.value.sectores_dañados/20 * 0.8);
    const finalProb = Math.min(prob, 1.0);
    resultado.value = { probabilidad_falla: finalProb, estado: finalProb > 0.5 ? "CRITICO" : "OPERATIVO", accion: "Fallback Mode" };
  } finally {
    loading.value = false;
    actualizarGraficos(); // C. Actualizar visualización
  }
};

const actualizarGraficos = () => {
  const probPercent = (resultado.value.probabilidad_falla * 100).toFixed(1);
  
  // Actualizar Line Chart (Arrays nativos)
  rawLabels.push(`Check #${checkCount.value}`);
  rawProb.push(probPercent);
  rawTemp.push(sensores.value.temperatura);
  
  if(rawLabels.length > 10) { rawLabels.shift(); rawProb.shift(); rawTemp.shift(); }

  // Reasignar objeto completo para reactividad segura
  historyData.value = {
    labels: [...rawLabels], 
    datasets: [
      { ...historyData.value.datasets[0], data: [...rawProb] },
      { ...historyData.value.datasets[1], data: [...rawTemp] }
    ]
  };

  // Actualizar Radar Chart
  radarData.value = {
    labels: ['Uso', 'Temp', 'Errores', 'Sectores'],
    datasets: [{
      label: 'Nivel', backgroundColor: 'rgba(78, 140, 255, 0.2)', borderColor: '#4e8cff', pointBackgroundColor: '#fff',
      data: [(sensores.value.horas_uso/50000)*100, sensores.value.temperatura, sensores.value.errores_lectura, (sensores.value.sectores_dañados/50)*100]
    }]
  };
};

const formatearFecha = (f) => new Date(f).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
const claseEstado = computed(() => resultado.value?.estado === 'CRITICO' ? 'risk-critical' : 'risk-safe');

onMounted(() => cargarHistorial());
</script>

<style scoped>
/* Estilos Globales del Dashboard */
.dashboard-wrapper { background: #0f1115; min-height: 100vh; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; }
.dash-header { padding: 1rem 2rem; background: #161920; display: flex; justify-content: space-between; border-bottom: 1px solid #2a2e35; align-items: center; }
.logo-small { cursor: pointer; color: #4e8cff; font-weight: bold; }
.logo-small:hover { color: #fff; }

.dashboard-container { max-width: 1000px; margin: 2rem auto; padding: 0 20px 40px 20px; }

/* Grids y Tarjetas */
.grid-control { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
.card { background: #1f232b; padding: 20px; border-radius: 12px; border: 1px solid #2a2e35; box-shadow: 0 4px 6px rgba(0,0,0,0.2); margin-bottom: 20px; }

/* Controles */
.input-group { margin-bottom: 15px; }
.input-group label { display: flex; justify-content: space-between; font-size: 0.85rem; color: #aaa; margin-bottom: 5px; }
.slider { width: 100%; -webkit-appearance: none; background: #333; height: 5px; border-radius: 3px; outline: none; }
.slider::-webkit-slider-thumb { -webkit-appearance: none; width: 16px; height: 16px; background: #4e8cff; border-radius: 50%; cursor: pointer; transition: 0.2s; }
.slider:hover::-webkit-slider-thumb { transform: scale(1.2); }
.critical-slider::-webkit-slider-thumb { background: #ff4444; }

.btn-analyze { width: 100%; padding: 12px; margin-top: 10px; background: linear-gradient(45deg, #4e8cff, #2962ff); color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; transition: 0.3s; }
.btn-analyze:hover { filter: brightness(1.2); }
.btn-analyze:disabled { opacity: 0.6; cursor: wait; }

/* Contenedores de Gráficos */
.chart-container-radar { position: relative; height: 250px; display: flex; align-items: center; justify-content: center; }
.chart-container-line { position: relative; height: 300px; width: 100%; }
.waiting-text { color: #555; font-style: italic; }

/* Badges */
.badge-large { padding: 5px 15px; border-radius: 6px; font-weight: bold; color: white; }
.risk-critical { background-color: rgba(255, 68, 68, 0.2); border: 1px solid #ff4444; color: #ff4444; }
.risk-safe { background-color: rgba(0, 200, 83, 0.2); border: 1px solid #00c853; color: #00c853; }

/* Tabla de Historial */
.history-table-section { overflow: hidden; }
.table-responsive { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9rem; }
th { text-align: left; padding: 12px; color: #888; border-bottom: 1px solid #333; background: #1a1d24; }
td { padding: 12px; border-bottom: 1px solid #2a2e35; }
tr:hover td { background: #252a33; }
.badge-small { padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: bold; }
.bg-red { background: rgba(255, 68, 68, 0.2); color: #ff4444; }
.bg-green { background: rgba(0, 200, 83, 0.2); color: #00c853; }
.empty-msg { text-align: center; color: #555; padding: 20px; font-style: italic; }
</style>
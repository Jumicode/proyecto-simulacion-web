<template>
  <div class="dashboard-wrapper">
    <div class="animated-bg">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
      <div class="stars"></div>
    </div>

    <header class="dashboard-header">
      <button class="back-button" @click="$emit('navegar', 'home')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <line x1="19" y1="12" x2="5" y2="12" stroke-width="2"/>
          <polyline points="12 19 5 12 12 5" stroke-width="2"/>
        </svg>
        <span>Volver a TechJulio</span>
      </button>
      <div class="header-title">
        <h1>Guardian AI Dashboard</h1>
        <div class="user-badge">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="8" r="4" stroke-width="2"/>
            <path d="M 4 20 Q 4 14 12 14 Q 20 14 20 20" stroke-width="2"/>
          </svg>
          <span>Cliente: <strong>Corp Beta</strong></span>
        </div>
      </div>
    </header>

    <div class="dashboard-container">
      <div class="grid-control">
        <div class="card control-panel">
          <div class="card-glow"></div>
          <h3 class="card-title">
            <span class="icon-emoji">📡</span>
            Telemetría en Tiempo Real
          </h3>

          <div class="input-group">
            <div class="label-wrapper">
              <label>Horas de Uso</label>
              <span class="value-display">{{ sensores.horas_uso }} hrs</span>
            </div>
            <input type="range" v-model.number="sensores.horas_uso" min="0" max="50000" class="slider">
          </div>

          <div class="input-group">
            <div class="label-wrapper">
              <label>Temperatura CPU</label>
              <span class="value-display" :class="{ 'temp-warning': sensores.temperatura > 70 }">
                {{ sensores.temperatura }}°C
              </span>
            </div>
            <input type="range" v-model.number="sensores.temperatura" min="20" max="100" class="slider">
          </div>

          <div class="input-group">
            <div class="label-wrapper">
              <label>Errores de Lectura</label>
              <span class="value-display">{{ sensores.errores_lectura }}</span>
            </div>
            <input type="range" v-model.number="sensores.errores_lectura" min="0" max="100" class="slider">
          </div>

          <div class="input-group">
            <div class="label-wrapper">
              <label>Sectores Dañados</label>
              <span class="value-display critical" v-if="sensores.sectores_dañados > 10">
                {{ sensores.sectores_dañados }}
              </span>
              <span class="value-display" v-else>{{ sensores.sectores_dañados }}</span>
            </div>
            <input type="range" v-model.number="sensores.sectores_dañados" min="0" max="50" class="slider critical-slider">
          </div>

          <button @click="analizarEstado" class="btn-analyze" :disabled="loading">
            <span v-if="!loading">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="12" cy="12" r="1" stroke-width="2"/>
                <circle cx="19" cy="12" r="1" stroke-width="2"/>
                <circle cx="5" cy="12" r="1" stroke-width="2"/>
              </svg>
              Ejecutar Diagnóstico IA
            </span>
            <span v-else>
              <svg class="spinner" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="12" cy="12" r="10" stroke-width="2" stroke-dasharray="60" stroke-dashoffset="0"/>
              </svg>
              Procesando Tensor...
            </span>
            <div class="btn-shine"></div>
          </button>
        </div>

        <div class="card chart-panel">
          <div class="card-glow"></div>
          <h3 class="card-title">
            <span class="icon-emoji">🔍</span>
            Huella del Dispositivo
          </h3>
          <div class="chart-container-radar">
            <Radar v-if="radarData.datasets.length > 0" :data="radarData" :options="radarOptions" />
            <p v-else class="waiting-text">Ejecuta un diagnóstico para ver la huella.</p>
          </div>
        </div>
      </div>

      <div class="card history-section">
        <div class="card-glow"></div>
        <div class="history-header">
          <h3 class="card-title">
            <span class="icon-emoji">📈</span>
            Tendencia en Vivo (Sesión Actual)
          </h3>
          <div v-if="resultado" :class="['badge-risk', claseEstado]">
            <span class="risk-indicator"></span>
            Riesgo: {{ (resultado.probabilidad_falla * 100).toFixed(1) }}%
          </div>
        </div>

        <div class="chart-container-line">
          <Line v-if="historyData.labels.length > 0" :data="historyData" :options="lineOptions" />
          <p v-else class="waiting-text">Ejecuta un diagnóstico para ver tendencias.</p>
        </div>
      </div>

      <div class="card history-table-section">
        <div class="card-glow"></div>
        <h3 class="card-title">
          <span class="icon-emoji">🗄️</span>
          Historial de Reportes
        </h3>
        <div class="table-responsive">
          <table v-if="listaHistorial.length > 0">
            <thead>
              <tr>
                <th>ID</th>
                <th>Hora</th>
                <th>Estado</th>
                <th>Probabilidad</th>
                <th>Temperatura</th>
                <th>Sectores</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in listaHistorial" :key="item.id" class="table-row">
                <td class="cell-id">#{{ item.id }}</td>
                <td>{{ formatearFecha(item.fecha) }}</td>
                <td>
                  <span :class="['badge-status', item.estado === 'CRITICO' ? 'status-critical' : 'status-safe']">
                    {{ item.estado }}
                  </span>
                </td>
                <td class="cell-numeric">{{ (item.probabilidad * 100).toFixed(1) }}%</td>
                <td class="cell-numeric">{{ item.temperatura.toFixed(1) }}°C</td>
                <td class="cell-numeric">{{ item.sectores }}</td>
              </tr>
            </tbody>
          </table>
          <p v-else class="empty-msg">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <rect x="3" y="3" width="18" height="18" rx="2" stroke-width="2"/>
              <line x1="9" y1="9" x2="15" y2="15" stroke-width="2"/>
              <line x1="15" y1="9" x2="9" y2="15" stroke-width="2"/>
            </svg>
            No hay registros guardados aún.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import {
  Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend, CategoryScale, LinearScale, Title
} from 'chart.js';
import { Radar, Line } from 'vue-chartjs';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend, CategoryScale, LinearScale, Title);

defineEmits<{
  navegar: [view: string]
}>();

interface SensorData {
  horas_uso: number;
  temperatura: number;
  errores_lectura: number;
  sectores_dañados: number;
}

interface HistorialItem {
  id: number;
  fecha: string;
  estado: string;
  probabilidad: number;
  temperatura: number;
  sectores: number;
}

const loading = ref(false);
const resultado = ref<any>(null);
const checkCount = ref(0);
const listaHistorial = ref<HistorialItem[]>([]);

const sensores = ref<SensorData>({
  horas_uso: 500,
  temperatura: 45,
  errores_lectura: 0,
  sectores_dañados: 0
});

const rawLabels: string[] = [];
const rawProb: number[] = [];
const rawTemp: number[] = [];

const historyData = ref({
  labels: [] as string[],
  datasets: [
    {
      label: 'Probabilidad de Falla (%)',
      backgroundColor: 'rgba(78, 140, 255, 0.2)',
      borderColor: '#4e8cff',
      data: [] as number[],
      tension: 0.4,
      fill: true,
      pointBackgroundColor: '#4e8cff',
      pointBorderColor: '#fff',
      pointRadius: 5
    },
    {
      label: 'Temperatura (°C)',
      backgroundColor: 'rgba(255, 152, 0, 0.1)',
      borderColor: '#ff9800',
      data: [] as number[],
      borderDash: [5, 5],
      tension: 0.4,
      pointBackgroundColor: '#ff9800',
      pointBorderColor: '#fff',
      pointRadius: 5
    }
  ]
});

const radarData = ref({
  labels: [] as string[],
  datasets: [] as any[]
});

const lineOptions: any = {
  responsive: true,
  maintainAspectRatio: false,
  animation: false,
  scales: {
    y: {
      beginAtZero: true,
      grid: { color: 'rgba(255, 255, 255, 0.05)' },
      ticks: { color: 'rgba(255, 255, 255, 0.7)' }
    },
    x: {
      grid: { color: 'rgba(255, 255, 255, 0.05)' },
      ticks: { color: 'rgba(255, 255, 255, 0.7)' }
    }
  },
  plugins: {
    legend: {
      labels: { color: 'rgba(255, 255, 255, 0.8)', useBorderRadius: true, padding: 15 }
    }
  }
};

const radarOptions: any = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    r: {
      angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
      grid: { color: 'rgba(255, 255, 255, 0.1)' },
      pointLabels: { color: 'rgba(255, 255, 255, 0.8)' },
      suggestedMin: 0,
      suggestedMax: 100,
      ticks: { color: 'rgba(255, 255, 255, 0.7)' }
    }
  },
  plugins: { legend: { display: false } }
};

const cargarHistorial = async () => {
  try {
    const res = await fetch('https://proyecto-simulacion-web.onrender.com/historial');
    if (res.ok) listaHistorial.value = await res.json();
  } catch (e) {
    console.error("Error cargando BD (¿Backend apagado?)", e);
  }
};

const analizarEstado = async () => {
  loading.value = true;
  checkCount.value++;

  try {
    const response = await fetch('https://proyecto-simulacion-web.onrender.com/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(sensores.value)
    });

    if (!response.ok) throw new Error("API Error");
    resultado.value = await response.json();
    await cargarHistorial();
  } catch (error) {
    const prob = (sensores.value.horas_uso / 50000 * 0.4) + (sensores.value.temperatura / 100 * 0.3) + (sensores.value.sectores_dañados / 20 * 0.8);
    const finalProb = Math.min(prob, 1.0);
    resultado.value = {
      probabilidad_falla: finalProb,
      estado: finalProb > 0.5 ? "CRITICO" : "OPERATIVO",
      accion: "Fallback Mode"
    };
  } finally {
    loading.value = false;
    actualizarGraficos();
  }
};

const actualizarGraficos = () => {
  if (!resultado.value) return;

  const probPercent = parseFloat((resultado.value.probabilidad_falla * 100).toFixed(1));

  rawLabels.push(`Check #${checkCount.value}`);
  rawProb.push(probPercent);
  rawTemp.push(sensores.value.temperatura);

  if (rawLabels.length > 10) {
    rawLabels.shift();
    rawProb.shift();
    rawTemp.shift();
  }

  historyData.value = {
    labels: [...rawLabels],
    datasets: [
      { ...historyData.value.datasets[0], data: [...rawProb] },
      { ...historyData.value.datasets[1], data: [...rawTemp] }
    ]
  };

  radarData.value = {
    labels: ['Uso', 'Temp', 'Errores', 'Sectores'],
    datasets: [{
      label: 'Nivel',
      backgroundColor: 'rgba(78, 140, 255, 0.2)',
      borderColor: '#4e8cff',
      pointBackgroundColor: '#4e8cff',
      pointBorderColor: '#fff',
      data: [
        (sensores.value.horas_uso / 50000) * 100,
        sensores.value.temperatura,
        sensores.value.errores_lectura,
        (sensores.value.sectores_dañados / 50) * 100
      ]
    }]
  };
};

const formatearFecha = (f: string): string => {
  return new Date(f).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

const claseEstado = computed(() => {
  return resultado.value?.estado === 'CRITICO' ? 'risk-critical' : 'risk-safe';
});

onMounted(() => cargarHistorial());
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.dashboard-wrapper {
  background-color: #0a0b0f;
  min-height: 100vh;
  color: white;
  position: relative;
  overflow-x: hidden;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* ============================================
   ANIMATED BACKGROUND
   ============================================ */
.animated-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.3;
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, #4e8cff 0%, transparent 70%);
  top: -250px;
  left: -250px;
  animation-delay: 0s;
}

.orb-2 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, #00d4ff 0%, transparent 70%);
  bottom: -200px;
  right: -200px;
  animation-delay: -7s;
}

.orb-3 {
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, #0084ff 0%, transparent 70%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -14s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(100px, -50px) scale(1.1);
  }
  66% {
    transform: translate(-50px, 100px) scale(0.9);
  }
}

.stars {
  position: absolute;
  width: 100%;
  height: 100%;
  background-image:
    radial-gradient(2px 2px at 20px 30px, rgba(255, 255, 255, 0.3), transparent),
    radial-gradient(2px 2px at 60px 70px, rgba(255, 255, 255, 0.2), transparent),
    radial-gradient(1px 1px at 50px 50px, rgba(255, 255, 255, 0.4), transparent),
    radial-gradient(1px 1px at 130px 80px, rgba(255, 255, 255, 0.3), transparent),
    radial-gradient(2px 2px at 90px 10px, rgba(255, 255, 255, 0.2), transparent);
  background-repeat: repeat;
  background-size: 200px 200px;
  animation: twinkle 5s ease-in-out infinite;
  opacity: 0.5;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 0.8; }
}

/* ============================================
   HEADER
   ============================================ */
.dashboard-header {
  position: relative;
  z-index: 10;
  background: rgba(15, 17, 21, 0.7);
  backdrop-filter: blur(20px);
  padding: 1.5rem 3rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  align-items: center;
  gap: 2rem;
  animation: slideDown 0.6s ease-out;
}

@keyframes slideDown {
  from {
    transform: translateY(-100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.back-button {
  background: rgba(78, 140, 255, 0.1);
  color: #4e8cff;
  border: 1px solid rgba(78, 140, 255, 0.3);
  padding: 0.7rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.back-button:hover {
  background: rgba(78, 140, 255, 0.2);
  border-color: #4e8cff;
  transform: translateX(-5px);
}

.back-button svg {
  width: 18px;
  height: 18px;
}

.header-title {
  flex: 1;
}

.dashboard-header h1 {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #ffffff 0%, #4e8cff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
}

.user-badge {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.95rem;
}

.user-badge svg {
  width: 18px;
  height: 18px;
  color: #4e8cff;
}

.user-badge strong {
  color: #4e8cff;
}

/* ============================================
   MAIN CONTAINER
   ============================================ */
.dashboard-container {
  position: relative;
  z-index: 1;
  max-width: 1400px;
  margin: 2rem auto;
  padding: 0 2rem 3rem 2rem;
}

.grid-control {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

.card {
  z-index:1;
  background: rgba(20, 24, 33, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.05);
  padding: 2.5rem;
  border-radius: 20px;
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
  transition: all 0.4s ease;
  animation: cardFadeIn 0.6s ease-out backwards;
}

.grid-control .card:nth-child(1) { animation-delay: 0.1s; }
.grid-control .card:nth-child(2) { animation-delay: 0.2s; }
.history-section { animation-delay: 0.3s; }
.history-table-section { animation-delay: 0.4s; }

@keyframes cardFadeIn {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card:hover {
  transform: translateY(-8px);
  border-color: rgba(78, 140, 255, 0.3);
  box-shadow: 0 20px 60px rgba(78, 140, 255, 0.2);
}

.card-glow {
  z-index:0;
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(78, 140, 255, 0.1), transparent 50%);
  opacity: 0;
  transition: opacity 0.4s ease;
}

.card:hover .card-glow {
  opacity: 1;
}

.card-title {
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: white;
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.icon-emoji {
  font-size: 1.5rem;
}

/* ============================================
   CONTROL PANEL
   ============================================ */
.control-panel {
  display: flex;
  flex-direction: column;
}

.input-group {
  margin-bottom: 1.8rem;
  position: relative; z-index: 2;
}

.input-group:last-of-type {
  margin-bottom: 2rem;
}

.label-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
}

.label-wrapper label {
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.95rem;
}

.value-display {
  color: #4e8cff;
  font-weight: 700;
  font-size: 1.1rem;
}

.value-display.temp-warning {
  color: #ff9800;
  animation: pulse-warning 2s ease-in-out infinite;
}

.value-display.critical {
  color: #ff4444;
  animation: pulse-critical 1.5s ease-in-out infinite;
}

@keyframes pulse-warning {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

@keyframes pulse-critical {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.slider {
  width: 100%;
  height: 6px;
  border-radius: 3px;
  background: linear-gradient(to right, #4e8cff, #00d4ff);
  outline: none;
  -webkit-appearance: none;
  appearance: none;
  cursor: pointer;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4e8cff, #00d4ff);
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(78, 140, 255, 0.4);
  transition: all 0.2s ease;
}

.slider::-webkit-slider-thumb:hover {
  transform: scale(1.15);
  box-shadow: 0 6px 20px rgba(78, 140, 255, 0.6);
}

.slider::-moz-range-thumb {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4e8cff, #00d4ff);
  cursor: pointer;
  border: none;
  box-shadow: 0 4px 15px rgba(78, 140, 255, 0.4);
  transition: all 0.2s ease;
}

.slider::-moz-range-thumb:hover {
  transform: scale(1.15);
  box-shadow: 0 6px 20px rgba(78, 140, 255, 0.6);
}

.slider.critical-slider {
  background: linear-gradient(to right, #ff9800, #ff4444);
}

.slider.critical-slider::-webkit-slider-thumb {
  background: linear-gradient(135deg, #ff9800, #ff4444);
}

.slider.critical-slider::-moz-range-thumb {
  background: linear-gradient(135deg, #ff9800, #ff4444);
}

.btn-analyze {
  background: linear-gradient(135deg, #4e8cff 0%, #0066ff 100%);
  color: white;
  padding: 1.1rem 2rem;
  border: none;
  border-radius: 10px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(78, 140, 255, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
  margin-top: auto;
}

.btn-analyze:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 15px 45px rgba(78, 140, 255, 0.6);
}

.btn-analyze:active:not(:disabled) {
  transform: translateY(-1px);
}

.btn-analyze:disabled {
  opacity: 0.7;
  cursor: wait;
}

.btn-analyze svg {
  width: 20px;
  height: 20px;
}

.btn-analyze .spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.btn-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s ease;
}

.btn-analyze:hover:not(:disabled) .btn-shine {
  left: 100%;
}

/* ============================================
   CHART PANELS
   ============================================ */
.chart-panel,
.history-section,
.history-table-section {
  display: flex;
  flex-direction: column;
}

.chart-container-radar,
.chart-container-line {
  position: relative;
  width: 100%;
}

.chart-container-radar {
  height: 280px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-container-line {
  height: 320px;
}

.waiting-text {
  color: rgba(255, 255, 255, 0.4);
  font-style: italic;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

/* ============================================
   HISTORY SECTION
   ============================================ */
.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.badge-risk {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.8rem 1.5rem;
  border-radius: 10px;
  font-weight: 700;
  font-size: 0.95rem;
  border: 1px solid;
}

.risk-critical {
  background: linear-gradient(135deg, rgba(255, 68, 68, 0.15), rgba(255, 68, 68, 0.05));
  border-color: rgba(255, 68, 68, 0.3);
  color: #ff6b6b;
}

.risk-safe {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.15), rgba(76, 175, 80, 0.05));
  border-color: rgba(76, 175, 80, 0.3);
  color: #4caf50;
}

.risk-indicator {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: blink 1.5s ease-in-out infinite;
}

.risk-critical .risk-indicator {
  background: #ff6b6b;
}

.risk-safe .risk-indicator {
  background: #4caf50;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

/* ============================================
   TABLE SECTION
   ============================================ */
.table-responsive {
  overflow-x: auto;
  margin-top: 1rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

thead {
  background: rgba(78, 140, 255, 0.1);
  border-bottom: 2px solid rgba(78, 140, 255, 0.2);
}

th {
  text-align: left;
  padding: 1rem;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 600;
}

.table-row {
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.2s ease;
}

.table-row:hover {
  background: rgba(78, 140, 255, 0.05);
}

td {
  padding: 1rem;
  color: rgba(255, 255, 255, 0.8);
}

.cell-id {
  color: #4e8cff;
  font-weight: 600;
}

.cell-numeric {
  font-family: 'Courier New', monospace;
  color: rgba(255, 255, 255, 0.7);
}

.badge-status {
  display: inline-block;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 700;
  border: 1px solid;
}

.status-critical {
  background: rgba(255, 68, 68, 0.1);
  color: #ff6b6b;
  border-color: rgba(255, 68, 68, 0.3);
}

.status-safe {
  background: rgba(76, 175, 80, 0.1);
  color: #4caf50;
  border-color: rgba(76, 175, 80, 0.3);
}

.empty-msg {
  text-align: center;
  padding: 3rem 1rem;
  color: rgba(255, 255, 255, 0.4);
  font-style: italic;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.empty-msg svg {
  width: 32px;
  height: 32px;
  opacity: 0.5;
}

/* ============================================
   RESPONSIVE
   ============================================ */
@media (max-width: 1024px) {
  .grid-control {
    grid-template-columns: 1fr;
  }

  .history-header {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    padding: 1.5rem;
    gap: 1rem;
  }

  .dashboard-header h1 {
    font-size: 1.5rem;
  }

  .dashboard-container {
    padding: 1rem;
  }

  .card {
    padding: 1.5rem;
  }

  .card-title {
    font-size: 1.1rem;
  }

  .user-badge {
    font-size: 0.85rem;
  }

  .chart-container-line {
    height: 250px;
  }

  .chart-container-radar {
    height: 250px;
  }

  table {
    font-size: 0.8rem;
  }

  th, td {
    padding: 0.7rem;
  }
}

@media (max-width: 480px) {
  .dashboard-header {
    padding: 1rem;
  }

  .dashboard-header h1 {
    font-size: 1.2rem;
  }

  .dashboard-container {
    padding: 0.5rem;
    margin: 1rem auto;
  }

  .card {
    padding: 1rem;
    margin-bottom: 1rem;
  }

  .card-title {
    font-size: 1rem;
    gap: 0.5rem;
  }

  .icon-emoji {
    font-size: 1.2rem;
  }

  .grid-control {
    gap: 1rem;
  }

  .chart-container-line,
  .chart-container-radar {
    height: 200px;
  }

  .badge-risk {
    width: 100%;
    justify-content: center;
  }

  table {
    font-size: 0.7rem;
  }

  th, td {
    padding: 0.5rem;
  }
}
</style>

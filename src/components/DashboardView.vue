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
          <h3>📡 Telemetría (Simulación)</h3>
          
          <label>Horas de Uso: {{ sensores.horas_uso }}</label>
          <input type="range" v-model.number="sensores.horas_uso" min="0" max="50000" class="slider">
          
          <label>Temp CPU: {{ sensores.temperatura }}°C</label>
          <input type="range" v-model.number="sensores.temperatura" min="20" max="100" class="slider">
          
          <label>Errores de Lectura: {{ sensores.errores_lectura }}</label>
          <input type="range" v-model.number="sensores.errores_lectura" min="0" max="100" class="slider">

              <label>Sectores Dañados: {{ sensores.sectores_dañados }}</label>
            <input type="range" v-model.number="sensores.sectores_dañados" min="0" max="100" class="slider">

          <button @click="analizarEstado" class="btn-analyze" :disabled="loading">
            {{ loading ? 'Procesando...' : 'Diagnóstico IA' }}
          </button>
        </div>

        <div class="card result-panel" :class="claseEstado">
          <div v-if="resultado">
            <h2>{{ (resultado.probabilidad_falla * 100).toFixed(1) }}%</h2>
            <div class="status-badge">{{ resultado.estado }}</div>
            <p>{{ resultado.accion }}</p>
          </div>
          <div v-else>Esperando datos...</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
const emit = defineEmits(['navegar']);

// --- LÓGICA DE NEGOCIO Y API ---
const loading = ref(false);
const resultado = ref(null);
const sensores = ref({ horas_uso: 500, temperatura: 45, errores_lectura: 0, sectores_dañados: 0 });

const analizarEstado = async () => {
  loading.value = true;
  try {
    const response = await fetch('http://127.0.0.1:8000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(sensores.value)
    });
    if (!response.ok) throw new Error("API Error");
    resultado.value = await response.json();
  } catch (error) {
    // Fallback Simulación Local
    const prob = (sensores.value.horas_uso/50000 * 0.4) + (sensores.value.temperatura/100 * 0.3);
    resultado.value = {
      probabilidad_falla: prob,
      estado: prob > 0.5 ? "CRITICO" : "OPERATIVO",
      accion: prob > 0.5 ? "Reemplazo" : "Ninguna"
    };
  } finally {
    loading.value = false;
  }
};

const claseEstado = computed(() => resultado.value?.estado === 'CRITICO' ? 'risk-critical' : 'risk-safe');
</script>

<style scoped>
/* CSS Específico del Dashboard */
.dashboard-wrapper { background: #0f1115; min-height: 100vh; color: white; }
.dash-header { padding: 1rem; background: #161920; display: flex; justify-content: space-between; }
.logo-small { cursor: pointer; color: #4e8cff; }
.dashboard-container { max-width: 800px; margin: 2rem auto; }
.grid-control { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.card { background: #1f232b; padding: 20px; border-radius: 10px; }
.btn-analyze { width: 100%; padding: 10px; margin-top: 10px; background: #4e8cff; color: white; border: none; cursor: pointer; }
.risk-critical { border: 2px solid #ff4444; } .risk-safe { border: 2px solid #00c853; }
</style>
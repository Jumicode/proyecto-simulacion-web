<template>
  <div class="order-wrapper">
    <header class="order-header">
      <div class="logo-small" @click="$emit('navegar', 'home')">
        ← Volver al Home
      </div>
      <h2>Configurador HaaS</h2>
    </header>

    <div class="order-container">
      
      <div class="config-panel">
        <h3>1. Selecciona tu Equipo Base</h3>
        <div class="device-grid">
          <div 
            v-for="device in devices" 
            :key="device.id"
            class="device-card"
            :class="{ active: selectedDevice.id === device.id }"
            @click="selectedDevice = device"
          >
            <div class="icon">{{ device.icon }}</div>
            <h4>{{ device.name }}</h4>
            <p class="base-price">Desde ${{ device.basePrice }}/mes</p>
          </div>
        </div>

        <h3>2. Personaliza la Potencia</h3>
        <div class="specs-control">
          <div class="control-group">
            <label>Memoria RAM: <strong>{{ config.ram }} GB</strong></label>
            <input type="range" v-model.number="config.ram" min="8" max="128" step="8" class="slider">
            <div class="scale">
              <span>8GB</span><span>128GB</span>
            </div>
          </div>

          <div class="control-group">
            <label>Almacenamiento SSD: <strong>{{ config.storage }} TB</strong></label>
            <input type="range" v-model.number="config.storage" min="1" max="10" step="1" class="slider">
            <div class="scale">
              <span>1TB</span><span>10TB</span>
            </div>
          </div>
        </div>

        <h3>3. Servicios Adicionales</h3>
        <div class="addons">
          <label class="checkbox-container">
            <input type="checkbox" v-model="config.includeAI">
            <span class="checkmark"></span>
            <div class="text">
              <strong>Guardian AI Monitoring (+ $20/mes)</strong>
              <p>Mantenimiento predictivo con TensorFlow para evitar fallos.</p>
            </div>
          </label>
        </div>
      </div>

      <div class="summary-panel">
        <div class="receipt">
          <h3>Resumen del Plan</h3>
          <div class="line-item">
            <span>{{ selectedDevice.name }} (Base)</span>
            <span>${{ selectedDevice.basePrice }}</span>
          </div>
          <div class="line-item">
            <span>Upgrade RAM ({{ config.ram - 8 }}GB)</span>
            <span>+${{ ramCost }}</span>
          </div>
          <div class="line-item">
            <span>SSD Extra ({{ config.storage - 1 }}TB)</span>
            <span>+${{ storageCost }}</span>
          </div>
          <div class="line-item" v-if="config.includeAI">
            <span>Guardian AI License</span>
            <span>+$20</span>
          </div>
          
          <hr>
          
          <div class="total">
            <span>Total Mensual (Leasing)</span>
            <span class="price">${{ totalPrice }}</span>
          </div>

          <button @click="procesarPedido" class="btn-checkout">
            SOLICITAR COTIZACIÓN FORMAL
          </button>
          <p class="disclaimer">Contrato mínimo a 24 meses. Sujeto a aprobación crediticia.</p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const emit = defineEmits(['navegar']);

// Datos de los equipos base
const devices = [
  { id: 1, name: 'Dell Latitude Pro', icon: '💻', basePrice: 45 },
  { id: 2, name: 'Lenovo ThinkStation', icon: '🖥️', basePrice: 80 },
  { id: 3, name: 'MacBook Pro M4', icon: '🍎', basePrice: 95 },
];

// Estado de la selección
const selectedDevice = ref(devices[0]);
const config = ref({
  ram: 16,
  storage: 1,
  includeAI: true
});

// Lógica de Precios (Simulada)
// Asumimos: $2 por cada GB extra de RAM, $10 por cada TB extra de SSD
const ramCost = computed(() => {
  const extraRam = Math.max(0, config.value.ram - 8); 
  return extraRam * 2;
});

const storageCost = computed(() => {
  const extraStorage = Math.max(0, config.value.storage - 1);
  return extraStorage * 15;
});

const totalPrice = computed(() => {
  let total = selectedDevice.value.basePrice + ramCost.value + storageCost.value;
  if (config.value.includeAI) total += 20;
  return total;
});

const procesarPedido = () => {
  alert(`¡Gracias! Hemos recibido tu solicitud para ${selectedDevice.value.name} con ${config.value.ram}GB RAM. Un agente de TechJulio te contactará.`);
  emit('navegar', 'home');
};
</script>

<style scoped>
/* Estilos Dark Mode Corporativo */
.order-wrapper { background: #0f1115; min-height: 100vh; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; }
.order-header { background: #161920; padding: 1.5rem; display: flex; align-items: center; border-bottom: 1px solid #2a2e35; }
.logo-small { cursor: pointer; color: #4e8cff; margin-right: 20px; font-weight: bold; }
.logo-small:hover { text-decoration: underline; }

.order-container { display: grid; grid-template-columns: 2fr 1fr; gap: 40px; max-width: 1200px; margin: 40px auto; padding: 0 20px; }

/* Tarjetas de Equipos */
.device-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 30px; }
.device-card { background: #1f232b; padding: 20px; border-radius: 10px; border: 1px solid #333; cursor: pointer; text-align: center; transition: 0.3s; }
.device-card:hover { transform: translateY(-5px); }
.device-card.active { border-color: #4e8cff; background: rgba(78, 140, 255, 0.1); }
.icon { font-size: 2.5rem; margin-bottom: 10px; }
.base-price { color: #888; font-size: 0.9rem; }

/* Sliders */
.control-group { margin-bottom: 25px; }
.control-group label { display: block; margin-bottom: 10px; }
.slider { width: 100%; -webkit-appearance: none; background: #333; height: 6px; border-radius: 3px; }
.slider::-webkit-slider-thumb { -webkit-appearance: none; width: 20px; height: 20px; background: #4e8cff; border-radius: 50%; cursor: pointer; }
.scale { display: flex; justify-content: space-between; font-size: 0.8rem; color: #666; margin-top: 5px; }

/* Checkbox AI */
.addons { margin-top: 20px; }
.checkbox-container { display: flex; align-items: center; gap: 15px; background: #1f232b; padding: 15px; border-radius: 8px; cursor: pointer; border: 1px solid #333; }
.checkbox-container:hover { border-color: #555; }
.checkbox-container input { width: 20px; height: 20px; }
.text strong { color: #4e8cff; }
.text p { font-size: 0.85rem; color: #888; margin: 0; }

/* Resumen / Recibo */
.summary-panel { position: sticky; top: 20px; }
.receipt { background: #fff; color: #333; padding: 30px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
.line-item { display: flex; justify-content: space-between; margin-bottom: 15px; font-size: 0.95rem; }
hr { border: 0; border-top: 1px solid #eee; margin: 20px 0; }
.total { display: flex; justify-content: space-between; align-items: center; font-size: 1.2rem; font-weight: bold; margin-bottom: 25px; }
.total .price { color: #4e8cff; font-size: 1.5rem; }

.btn-checkout { width: 100%; background: #000; color: white; padding: 15px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.3s; }
.btn-checkout:hover { background: #333; }
.disclaimer { font-size: 0.7rem; color: #999; text-align: center; margin-top: 15px; }
</style>
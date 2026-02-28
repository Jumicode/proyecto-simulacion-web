<template>
  <div class="order-wrapper">
    <div class="animated-bg">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
      <div class="stars"></div>
    </div>

    <header class="order-header">
      <button class="back-button" @click="$emit('navegar', 'home')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <line x1="19" y1="12" x2="5" y2="12" stroke-width="2"/>
          <polyline points="12 19 5 12 12 5" stroke-width="2"/>
        </svg>
        <span>Volver al Home</span>
      </button>
      <h1>Configurador HaaS</h1>
    </header>

    <div class="order-container">
      <div class="config-panel">
        <h3 class="section-title">1. Selecciona tu Equipo Base</h3>
        <div class="device-grid">
          <div
            v-for="device in devices"
            :key="device.id"
            class="device-card"
            :class="{ active: selectedDevice.id === device.id }"
            @click="selectedDevice = device"
          >
            <div class="card-glow"></div>
            <div class="icon-large">{{ device.icon }}</div>
            <h4>{{ device.name }}</h4>
            <p class="base-price">Desde <strong>${{ device.basePrice }}</strong>/mes</p>
          </div>
        </div>

        <h3 class="section-title">2. Personaliza la Potencia</h3>
        <div class="specs-control">
          <div class="control-group">
            <div class="label-wrapper">
              <label>Memoria RAM</label>
              <span class="value-display">{{ config.ram }} GB</span>
            </div>
            <input type="range" v-model.number="config.ram" min="8" max="128" step="8" class="slider">
            <div class="scale">
              <span>8GB</span><span>128GB</span>
            </div>
          </div>

          <div class="control-group">
            <div class="label-wrapper">
              <label>Almacenamiento SSD</label>
              <span class="value-display">{{ config.storage }} TB</span>
            </div>
            <input type="range" v-model.number="config.storage" min="1" max="10" step="1" class="slider">
            <div class="scale">
              <span>1TB</span><span>10TB</span>
            </div>
          </div>
        </div>

        <h3 class="section-title">3. Servicios Adicionales</h3>
        <div class="addons">
          <label class="checkbox-container">
            <input type="checkbox" v-model="config.includeAI" class="checkbox-input">
            <span class="checkmark"></span>
            <div class="checkbox-text">
              <strong>Guardian AI Monitoring</strong>
              <p>Mantenimiento predictivo con TensorFlow para evitar fallos.</p>
              <span class="badge-price">+$20/mes</span>
            </div>
          </label>
        </div>
      </div>

      <div class="summary-panel">
        <div class="receipt">
          <h3 class="receipt-title">Resumen del Plan</h3>

          <div class="receipt-items">
            <div class="line-item">
              <span class="item-label">{{ selectedDevice.name }} (Base)</span>
              <span class="item-price">${{ selectedDevice.basePrice }}</span>
            </div>
            <div class="line-item">
              <span class="item-label">Upgrade RAM ({{ config.ram - 8 }}GB)</span>
              <span class="item-price">+${{ ramCost }}</span>
            </div>
            <div class="line-item">
              <span class="item-label">SSD Extra ({{ config.storage - 1 }}TB)</span>
              <span class="item-price">+${{ storageCost }}</span>
            </div>
            <div class="line-item" v-if="config.includeAI">
              <span class="item-label">Guardian AI License</span>
              <span class="item-price">+$20</span>
            </div>
          </div>

          <div class="receipt-divider"></div>

          <div class="total">
            <span class="total-label">Total Mensual (Leasing)</span>
            <span class="total-price">${{ totalPrice }}</span>
          </div>

          <button @click="procesarPedido" class="btn-checkout">
            <span>Solicitar Cotización Formal</span>
            <div class="btn-shine"></div>
          </button>
          <p class="disclaimer">
            <strong>Contrato mínimo a 24 meses.</strong> Sujeto a aprobación crediticia.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

const emit = defineEmits<{
  navegar: [view: string]
}>();

interface Device {
  id: number;
  name: string;
  icon: string;
  basePrice: number;
}

const devices: Device[] = [
  { id: 1, name: 'Dell Latitude Pro', icon: '💻', basePrice: 45 },
  { id: 2, name: 'Lenovo ThinkStation', icon: '🖥️', basePrice: 80 },
  { id: 3, name: 'MacBook Pro M4', icon: '🍎', basePrice: 95 },
];

const selectedDevice = ref<Device>(devices[0]);
const config = ref({
  ram: 16,
  storage: 1,
  includeAI: true
});

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

const procesarPedido = async () => {
  // Construimos el objeto para enviar al backend
  const pedidoData = {
    categoria: "Hardware",
    producto: selectedDevice.value.name,
    detalles: `${config.value.ram}GB RAM, ${config.value.storage}TB SSD ` + (config.value.includeAI ? '+ Guardian AI' : ''),
    precio: totalPrice.value
  };

  try {
    const res = await fetch('https://proyecto-simulacion-web.onrender.com/pedidos', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(pedidoData)
    });

    if(res.ok) {
      alert("✅ Solicitud enviada correctamente.");
      emit('navegar', 'orders'); // <-- Redirigir a "Mis Pedidos"
    }
  } catch (e) {
    alert("Error enviando pedido");
  }
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.order-wrapper {
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
.order-header {
  position: relative;
  z-index: 10;
  background: rgba(15, 17, 21, 0.7);
  backdrop-filter: blur(20px);
  padding: 2rem 3rem;
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

.order-header h1 {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #ffffff 0%, #4e8cff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* ============================================
   MAIN CONTAINER
   ============================================ */
.order-container {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 3rem;
  max-width: 1400px;
  margin: 3rem auto;
  padding: 0 2rem;
}

.config-panel {
  animation: fadeInUp 1s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.section-title {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  margin-top: 2.5rem;
  color: white;
}

.section-title:first-of-type {
  margin-top: 0;
}

/* ============================================
   DEVICE GRID
   ============================================ */
.device-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.device-card {
  background: rgba(20, 24, 33, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.05);
  padding: 1.5rem;
  border-radius: 16px;
  backdrop-filter: blur(10px);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.4s ease;
  text-align: center;
  animation: cardFadeIn 0.6s ease-out backwards;
}

.device-card:nth-child(1) { animation-delay: 0.1s; }
.device-card:nth-child(2) { animation-delay: 0.2s; }
.device-card:nth-child(3) { animation-delay: 0.3s; }

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

.device-card:hover {
  transform: translateY(-8px);
  border-color: rgba(78, 140, 255, 0.3);
  box-shadow: 0 20px 60px rgba(78, 140, 255, 0.2);
}

.device-card.active {
  border-color: #4e8cff;
  background: linear-gradient(135deg, rgba(78, 140, 255, 0.15), rgba(0, 212, 255, 0.08));
  box-shadow: 0 20px 60px rgba(78, 140, 255, 0.3);
}

.card-glow {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(78, 140, 255, 0.1), transparent 50%);
  opacity: 0;
  transition: opacity 0.4s ease;
}

.device-card:hover .card-glow {
  opacity: 1;
}

.icon-large {
  font-size: 3rem;
  margin-bottom: 0.8rem;
  display: inline-block;
}

.device-card h4 {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: white;
}

.base-price {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.base-price strong {
  color: #4e8cff;
  font-weight: 600;
}

/* ============================================
   SPECS CONTROL
   ============================================ */
.specs-control {
  background: rgba(20, 24, 33, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.05);
  padding: 2rem;
  border-radius: 16px;
  backdrop-filter: blur(10px);
}

.control-group {
  margin-bottom: 2.5rem;
}

.control-group:last-child {
  margin-bottom: 0;
}

.label-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.label-wrapper label {
  font-weight: 600;
  font-size: 1rem;
  color: white;
}

.value-display {
  color: #4e8cff;
  font-weight: 700;
  font-size: 1.1rem;
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

.scale {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.5);
  margin-top: 0.5rem;
}

/* ============================================
   ADDONS
   ============================================ */
.addons {
  margin-top: 1.5rem;
}

.checkbox-container {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  background: linear-gradient(135deg, rgba(78, 140, 255, 0.1), rgba(0, 212, 255, 0.05));
  border: 1px solid rgba(78, 140, 255, 0.3);
  padding: 1.5rem;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.checkbox-container:hover {
  background: linear-gradient(135deg, rgba(78, 140, 255, 0.15), rgba(0, 212, 255, 0.1));
  border-color: #4e8cff;
}

.checkbox-input {
  width: 20px;
  height: 20px;
  margin-top: 2px;
  cursor: pointer;
  accent-color: #4e8cff;
}

.checkbox-text {
  flex: 1;
}

.checkbox-text strong {
  display: block;
  color: white;
  margin-bottom: 0.3rem;
}

.checkbox-text p {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.badge-price {
  display: inline-block;
  padding: 0.3rem 0.8rem;
  background: rgba(78, 140, 255, 0.2);
  border: 1px solid rgba(78, 140, 255, 0.4);
  border-radius: 20px;
  color: #4e8cff;
  font-size: 0.8rem;
  font-weight: 600;
}

/* ============================================
   SUMMARY PANEL
   ============================================ */
.summary-panel {
  position: sticky;
  top: 2rem;
  animation: fadeInUp 1s ease-out 0.2s backwards;
}

.receipt {
  background: rgba(20, 24, 33, 0.95);
  border: 1px solid rgba(78, 140, 255, 0.2);
  padding: 2rem;
  border-radius: 20px;
  backdrop-filter: blur(20px);
  box-shadow: 0 20px 60px rgba(78, 140, 255, 0.2);
}

.receipt-title {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: white;
  text-align: center;
}

.receipt-items {
  margin-bottom: 1.5rem;
}

.line-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.8rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  font-size: 0.95rem;
}

.line-item:last-child {
  border-bottom: none;
}

.item-label {
  color: rgba(255, 255, 255, 0.7);
}

.item-price {
  color: #4e8cff;
  font-weight: 600;
}

.receipt-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(78, 140, 255, 0.3), transparent);
  margin: 1.5rem 0;
}

.total {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.total-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.95rem;
}

.total-price {
  color: #4e8cff;
  font-size: 1.8rem;
  font-weight: 800;
}

.btn-checkout {
  width: 100%;
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
}

.btn-checkout:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 45px rgba(78, 140, 255, 0.6);
}

.btn-checkout:active {
  transform: translateY(-1px);
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

.btn-checkout:hover .btn-shine {
  left: 100%;
}

.disclaimer {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.5);
  text-align: center;
  margin-top: 1rem;
  line-height: 1.5;
}

.disclaimer strong {
  color: rgba(255, 255, 255, 0.7);
}

/* ============================================
   RESPONSIVE
   ============================================ */
@media (max-width: 1024px) {
  .order-container {
    grid-template-columns: 1fr;
  }

  .summary-panel {
    position: static;
  }

  .device-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  }
}

@media (max-width: 768px) {
  .order-header {
    flex-direction: column;
    align-items: flex-start;
    padding: 1.5rem;
  }

  .order-header h1 {
    font-size: 1.5rem;
    width: 100%;
  }

  .order-container {
    padding: 1rem;
    gap: 1.5rem;
    margin: 1.5rem auto;
  }

  .specs-control {
    padding: 1.5rem;
  }

  .device-grid {
    grid-template-columns: 1fr 1fr;
  }

  .section-title {
    font-size: 1.1rem;
  }

  .receipt {
    padding: 1.5rem;
  }

  .total-price {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .device-grid {
    grid-template-columns: 1fr;
  }

  .order-header {
    padding: 1rem;
  }

  .order-header h1 {
    font-size: 1.2rem;
  }

  .icon-large {
    font-size: 2.5rem;
  }

  .btn-checkout {
    padding: 1rem;
  }

  .receipt {
    padding: 1rem;
  }
}
</style>

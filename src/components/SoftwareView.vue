<template>
  <div class="software-wrapper">
    <div class="animated-bg">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
      <div class="stars"></div>
    </div>

    <header class="software-header">
      <button class="back-button" @click="$emit('navegar', 'home')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <line x1="19" y1="12" x2="5" y2="12" stroke-width="2"/>
          <polyline points="12 19 5 12 12 5" stroke-width="2"/>
        </svg>
        <span>Volver al Home</span>
      </button>
      <h1>Cotizador de Desarrollo (Scrum)</h1>
    </header>

    <div class="software-container">
      <div class="config-panel">
        <h3 class="section-title">1. ¿Qué vamos a construir?</h3>
        <div class="project-grid">
          <div
            v-for="type in projectTypes"
            :key="type.id"
            class="project-card"
            :class="{ active: selectedType.id === type.id }"
            @click="selectedType = type"
          >
            <div class="card-glow"></div>
            <div class="project-icon">{{ type.icon }}</div>
            <h4>{{ type.name }}</h4>
            <p class="project-desc">{{ type.desc }}</p>
          </div>
        </div>

        <h3 class="section-title">2. Alcance y Plataformas</h3>
        <div class="scope-control">
          <div class="platform-selector">
            <label class="platform-label">Plataformas:</label>
            <div class="checkbox-group">
              <label class="platform-checkbox">
                <input type="checkbox" v-model="scope.web">
                <span class="checkbox-mark"></span>
                <span class="checkbox-text">Web App</span>
              </label>
              <label class="platform-checkbox">
                <input type="checkbox" v-model="scope.mobile">
                <span class="checkbox-mark"></span>
                <span class="checkbox-text">Móvil (iOS/Android)</span>
              </label>
            </div>
          </div>

          <div class="slider-group">
            <div class="label-wrapper">
              <label>Nivel de Diseño UI/UX</label>
              <span class="design-label">{{ designLabel }}</span>
            </div>
            <input type="range" v-model.number="scope.designLevel" min="1" max="3" class="slider">
            <div class="scale">
              <span>Plantilla</span><span>Custom</span><span>Premium</span>
            </div>
          </div>
        </div>

        <h3 class="section-title">3. Módulos Específicos</h3>
        <div class="modules-grid">
          <label class="module-check" v-for="mod in modules" :key="mod.id">
            <input type="checkbox" v-model="mod.selected" class="module-input">
            <span class="module-box">
              <span class="module-content">
                <strong>{{ mod.name }}</strong>
                <small class="module-price">+${{ mod.price }}</small>
              </span>
            </span>
          </label>
        </div>
      </div>

      <div class="summary-panel">
        <div class="receipt">
          <h3 class="receipt-title">Estimación de Inversión</h3>

          <div class="receipt-items">
            <div class="line-item main-item">
              <span>{{ selectedType.name }}</span>
              <span>${{ selectedType.basePrice }}</span>
            </div>

            <div class="line-item" v-if="platformCost > 0">
              <span>Plataformas Extra</span>
              <span>+${{ platformCost }}</span>
            </div>

            <div class="line-item">
              <span>Diseño {{ designLabel }}</span>
              <span>+${{ designCost }}</span>
            </div>

            <div v-for="mod in selectedModules" :key="mod.id" class="line-item">
              <span>{{ mod.name }}</span>
              <span>+${{ mod.price }}</span>
            </div>
          </div>

          <div class="receipt-divider"></div>

          <div class="total">
            <span class="total-label">Estimado Total</span>
            <span class="total-price">${{ totalEstimate }}</span>
          </div>

          <div class="timeline-box">
            <div class="timeline-item">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="12" cy="12" r="10" stroke-width="2"/>
                <polyline points="12 6 12 12 16 14" stroke-width="2"/>
              </svg>
              <div>
                <span class="timeline-label">Tiempo estimado</span>
                <strong>{{ estimatedWeeks }} semanas</strong>
              </div>
            </div>
            <div class="timeline-item">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" stroke-width="2"/>
                <circle cx="9" cy="7" r="4" stroke-width="2"/>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87" stroke-width="2"/>
                <path d="M16 3.13a4 4 0 0 1 0 7.75" stroke-width="2"/>
              </svg>
              <div>
                <span class="timeline-label">Equipo</span>
                <strong>{{ teamSize }}</strong>
              </div>
            </div>
          </div>

          <button @click="solicitarReunion" class="btn-consult">
            <span>Agendar Briefing Técnico</span>
            <div class="btn-shine"></div>
          </button>
          <p class="disclaimer">Presupuesto sujeto a levantamiento de requerimientos final.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

defineEmits<{
  navegar: [view: string]
}>();

interface ProjectType {
  id: number;
  name: string;
  icon: string;
  basePrice: number;
  desc: string;
  baseWeeks: number;
}

interface Module {
  id: number;
  name: string;
  price: number;
  selected: boolean;
}

interface Scope {
  web: boolean;
  mobile: boolean;
  designLevel: number;
}

const projectTypes: ProjectType[] = [
  { id: 1, name: 'MVP Startup', icon: '🚀', basePrice: 5000, desc: 'Producto mínimo viable para validar mercado.', baseWeeks: 4 },
  { id: 2, name: 'SaaS / Web App', icon: '☁️', basePrice: 12000, desc: 'Plataforma completa con gestión de usuarios.', baseWeeks: 10 },
  { id: 3, name: 'ERP Corporativo', icon: '🏢', basePrice: 25000, desc: 'Automatización de procesos a medida.', baseWeeks: 16 },
];

const modules = ref<Module[]>([
  { id: 1, name: 'Pasarela Pagos', price: 1500, selected: false },
  { id: 2, name: 'Panel Admin', price: 2000, selected: true },
  { id: 3, name: 'Chat en Vivo', price: 1200, selected: false },
  { id: 4, name: 'IA Integration', price: 3500, selected: false },
]);

const selectedType = ref<ProjectType>(projectTypes[1]);
const scope = ref<Scope>({
  web: true,
  mobile: false,
  designLevel: 2
});

const designLabel = computed(() => {
  if (scope.value.designLevel === 1) return 'Básico (Bootstrap)';
  if (scope.value.designLevel === 2) return 'A Medida (Figma)';
  return 'Award Winning (Animaciones)';
});

const designCost = computed(() => {
  return (scope.value.designLevel - 1) * 3000;
});

const platformCost = computed(() => {
  return scope.value.mobile ? 5000 : 0;
});

const selectedModules = computed(() => modules.value.filter(m => m.selected));

const totalEstimate = computed(() => {
  const modsTotal = selectedModules.value.reduce((acc, m) => acc + m.price, 0);
  return selectedType.value.basePrice + platformCost.value + designCost.value + modsTotal;
});

const estimatedWeeks = computed(() => {
  let weeks = selectedType.value.baseWeeks;
  if (scope.value.mobile) weeks += 4;
  if (scope.value.designLevel === 3) weeks += 3;
  weeks += selectedModules.value.length;
  return weeks;
});

const teamSize = computed(() => {
  if (totalEstimate.value > 20000) return '3 Devs + 1 PM';
  return '2 Devs Full Stack';
});

const solicitarReunion = () => {
  alert(`¡Genial! Tu proyecto estimado en $${totalEstimate.value} requiere un equipo de ${teamSize.value}. Te contactaremos para definir el Sprint 0.`);
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.software-wrapper {
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
.software-header {
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

.software-header h1 {
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
.software-container {
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
   PROJECT CARDS
   ============================================ */
.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.project-card {
  background: rgba(20, 24, 33, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.05);
  padding: 2rem;
  border-radius: 16px;
  backdrop-filter: blur(10px);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.4s ease;
  text-align: center;
  animation: cardFadeIn 0.6s ease-out backwards;
}

.project-card:nth-child(1) { animation-delay: 0.1s; }
.project-card:nth-child(2) { animation-delay: 0.2s; }
.project-card:nth-child(3) { animation-delay: 0.3s; }

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

.project-card:hover {
  transform: translateY(-10px);
  border-color: rgba(78, 140, 255, 0.3);
  box-shadow: 0 20px 60px rgba(78, 140, 255, 0.2);
}

.project-card.active {
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

.project-card:hover .card-glow {
  opacity: 1;
}

.project-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: inline-block;
}

.project-card h4 {
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 0.8rem;
  color: white;
}

.project-desc {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.95rem;
  line-height: 1.5;
}

/* ============================================
   SCOPE CONTROL
   ============================================ */
.scope-control {
  background: rgba(20, 24, 33, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.05);
  padding: 2rem;
  border-radius: 16px;
  backdrop-filter: blur(10px);
  margin-bottom: 2rem;
}

.platform-selector {
  margin-bottom: 2rem;
}

.platform-label {
  display: block;
  font-weight: 600;
  color: white;
  margin-bottom: 1rem;
}

.checkbox-group {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.platform-checkbox {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  cursor: pointer;
  position: relative;
}

.platform-checkbox input {
  display: none;
}

.checkbox-mark {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(78, 140, 255, 0.5);
  border-radius: 6px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.platform-checkbox input:checked + .checkbox-mark {
  background: linear-gradient(135deg, #4e8cff, #00d4ff);
  border-color: #4e8cff;
}

.platform-checkbox input:checked + .checkbox-mark::after {
  content: '✓';
  color: white;
  font-weight: bold;
  font-size: 0.9rem;
}

.checkbox-text {
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

.slider-group {
  margin-top: 2rem;
}

.label-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.label-wrapper label {
  font-weight: 600;
  color: white;
}

.design-label {
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
   MODULES GRID
   ============================================ */
.modules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.module-check {
  position: relative;
  cursor: pointer;
}

.module-input {
  display: none;
}

.module-box {
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, rgba(78, 140, 255, 0.1), rgba(0, 212, 255, 0.05));
  border: 1px solid rgba(78, 140, 255, 0.2);
  padding: 1.5rem;
  border-radius: 12px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.module-check .module-input:checked + .module-box {
  background: linear-gradient(135deg, rgba(78, 140, 255, 0.25), rgba(0, 212, 255, 0.15));
  border-color: #4e8cff;
  box-shadow: 0 10px 30px rgba(78, 140, 255, 0.2);
}

.module-box:hover {
  border-color: rgba(78, 140, 255, 0.4);
}

.module-content {
  width: 100%;
}

.module-content strong {
  display: block;
  color: white;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.module-price {
  color: #4e8cff;
  font-weight: 700;
  display: block;
  font-size: 1rem;
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
  padding: 2.5rem;
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
  color: rgba(255, 255, 255, 0.7);
}

.line-item:last-child {
  border-bottom: none;
}

.main-item {
  font-weight: 700;
  color: white;
  font-size: 1.1rem;
  margin-bottom: 1rem !important;
  padding-bottom: 1rem !important;
  border-bottom: 2px solid rgba(78, 140, 255, 0.2) !important;
}

.main-item span:last-child {
  color: #4e8cff;
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

/* ============================================
   TIMELINE BOX
   ============================================ */
.timeline-box {
  background: linear-gradient(135deg, rgba(78, 140, 255, 0.1), rgba(0, 212, 255, 0.05));
  border: 1px solid rgba(78, 140, 255, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.timeline-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.timeline-item svg {
  width: 24px;
  height: 24px;
  color: #4e8cff;
  flex-shrink: 0;
}

.timeline-label {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.85rem;
  display: block;
  margin-bottom: 0.3rem;
}

.timeline-item strong {
  color: white;
  font-size: 1.1rem;
}

/* ============================================
   BUTTON
   ============================================ */
.btn-consult {
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
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-consult:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 45px rgba(78, 140, 255, 0.6);
}

.btn-consult:active {
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

.btn-consult:hover .btn-shine {
  left: 100%;
}

.disclaimer {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.5);
  text-align: center;
  margin-top: 1rem;
  line-height: 1.5;
}

/* ============================================
   RESPONSIVE
   ============================================ */
@media (max-width: 1024px) {
  .software-container {
    grid-template-columns: 1fr;
  }

  .summary-panel {
    position: static;
  }

  .project-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }
}

@media (max-width: 768px) {
  .software-header {
    flex-direction: column;
    align-items: flex-start;
    padding: 1.5rem;
  }

  .software-header h1 {
    font-size: 1.5rem;
    width: 100%;
  }

  .software-container {
    padding: 1rem;
    gap: 1.5rem;
    margin: 1.5rem auto;
  }

  .scope-control {
    padding: 1.5rem;
  }

  .project-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
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

  .timeline-box {
    flex-direction: row;
    flex-wrap: wrap;
  }

  .timeline-item {
    flex: 1;
    min-width: 150px;
  }
}

@media (max-width: 480px) {
  .project-grid {
    grid-template-columns: 1fr;
  }

  .software-header {
    padding: 1rem;
  }

  .software-header h1 {
    font-size: 1.2rem;
  }

  .software-container {
    padding: 0.5rem;
    margin: 1rem auto;
  }

  .scope-control {
    padding: 1rem;
  }

  .project-icon {
    font-size: 2.5rem;
  }

  .modules-grid {
    grid-template-columns: 1fr;
  }

  .checkbox-group {
    flex-direction: column;
  }

  .receipt {
    padding: 1rem;
  }

  .btn-consult {
    padding: 1rem;
  }

  .timeline-item {
    flex: 1 0 100%;
  }
}
</style>
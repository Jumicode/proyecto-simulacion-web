<template>
  <div class="software-wrapper">
    <header class="sw-header">
      <div class="logo-small" @click="$emit('navegar', 'home')">
        ← Volver al Home
      </div>
      <h2>Cotizador de Desarrollo (Scrum)</h2>
    </header>

    <div class="sw-container">
      
      <div class="config-panel">
        
        <h3>1. ¿Qué vamos a construir?</h3>
        <div class="project-grid">
          <div 
            v-for="type in projectTypes" 
            :key="type.id"
            class="project-card"
            :class="{ active: selectedType.id === type.id }"
            @click="selectedType = type"
          >
            <div class="icon">{{ type.icon }}</div>
            <h4>{{ type.name }}</h4>
            <p class="desc">{{ type.desc }}</p>
          </div>
        </div>

        <h3>2. Alcance y Plataformas</h3>
        <div class="scope-control">
          <div class="platform-selector">
            <label>Plataformas:</label>
            <div class="checkbox-group">
              <label><input type="checkbox" v-model="scope.web"> Web App</label>
              <label><input type="checkbox" v-model="scope.mobile"> Móvil (iOS/Android)</label>
            </div>
          </div>

          <div class="slider-group">
            <label>Nivel de Diseño UI/UX: <strong>{{ designLabel }}</strong></label>
            <input type="range" v-model.number="scope.designLevel" min="1" max="3" class="slider">
            <div class="scale">
              <span>Plantilla</span><span>Custom</span><span>Premium</span>
            </div>
          </div>
        </div>

        <h3>3. Módulos Específicos</h3>
        <div class="modules-grid">
          <label class="module-check" v-for="mod in modules" :key="mod.id">
            <input type="checkbox" v-model="mod.selected">
            <span class="box">
              <strong>{{ mod.name }}</strong>
              <small>+${{ mod.price }}</small>
            </span>
          </label>
        </div>

      </div>

      <div class="summary-panel">
        <div class="receipt">
          <h3>Estimación de Inversión</h3>
          
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
          
          <hr>
          
          <div class="total">
            <span>Estimado Total</span>
            <span class="price">~${{ totalEstimate }}</span>
          </div>

          <div class="timeline-box">
            ⏱️ Tiempo estimado: <strong>{{ estimatedWeeks }} semanas</strong>
            <br>
            👥 Equipo: <strong>{{ teamSize }} personas</strong>
          </div>

          <button @click="solicitarReunion" class="btn-consult">
            AGENDAR BRIEFING TÉCNICO
          </button>
          <p class="disclaimer">Presupuesto sujeto a levantamiento de requerimientos final.</p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const emit = defineEmits(['navegar']);

// DATOS
const projectTypes = [
  { id: 1, name: 'MVP Startup', icon: '🚀', basePrice: 5000, desc: 'Producto mínimo viable para validar mercado.', baseWeeks: 4 },
  { id: 2, name: 'SaaS / Web App', icon: '☁️', basePrice: 12000, desc: 'Plataforma completa con gestión de usuarios.', baseWeeks: 10 },
  { id: 3, name: 'ERP Corporativo', icon: '🏢', basePrice: 25000, desc: 'Automatización de procesos a medida.', baseWeeks: 16 },
];

const modules = ref([
  { id: 1, name: 'Pasarela Pagos', price: 1500, selected: false },
  { id: 2, name: 'Panel Admin', price: 2000, selected: true },
  { id: 3, name: 'Chat en Vivo', price: 1200, selected: false },
  { id: 4, name: 'IA Integration', price: 3500, selected: false },
]);

const selectedType = ref(projectTypes[1]);
const scope = ref({
  web: true,
  mobile: false,
  designLevel: 2 // 1: Básico, 2: Custom, 3: Premium
});

// LÓGICA COMPUTADA
const designLabel = computed(() => {
  if (scope.value.designLevel === 1) return 'Básico (Bootstrap)';
  if (scope.value.designLevel === 2) return 'A Medida (Figma)';
  return 'Award Winning (Animaciones)';
});

const designCost = computed(() => {
  return (scope.value.designLevel - 1) * 3000;
});

const platformCost = computed(() => {
  // Si quiere móvil Y web, sumamos costo. Asumimos Web incluida en base.
  return scope.value.mobile ? 5000 : 0;
});

const selectedModules = computed(() => modules.value.filter(m => m.selected));

const totalEstimate = computed(() => {
  const modsTotal = selectedModules.value.reduce((acc, m) => acc + m.price, 0);
  return selectedType.value.basePrice + platformCost.value + designCost.value + modsTotal;
});

// Estimación de tiempo y equipo basada en complejidad (Lógica simple)
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
  emit('navegar', 'home');
};
</script>

<style scoped>
/* Estilos Dark Mode (Consistente con TechJulio) */
.software-wrapper { background: #0f1115; min-height: 100vh; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; }
.sw-header { background: #161920; padding: 1.5rem; display: flex; align-items: center; border-bottom: 1px solid #2a2e35; }
.logo-small { cursor: pointer; color: #4e8cff; margin-right: 20px; font-weight: bold; }

.sw-container { display: grid; grid-template-columns: 2fr 1fr; gap: 40px; max-width: 1200px; margin: 40px auto; padding: 0 20px; }

/* Tarjetas Tipo Proyecto */
.project-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 30px; }
.project-card { background: #1f232b; padding: 20px; border-radius: 10px; border: 1px solid #333; cursor: pointer; transition: 0.3s; }
.project-card:hover { transform: translateY(-5px); border-color: #555; }
.project-card.active { border-color: #4e8cff; background: rgba(78, 140, 255, 0.1); }
.project-card .desc { font-size: 0.8rem; color: #888; margin-top: 5px; }

/* Controles de Alcance */
.scope-control { background: #1f232b; padding: 20px; border-radius: 10px; margin-bottom: 30px; }
.checkbox-group { display: flex; gap: 20px; margin-top: 10px; }
.slider-group { margin-top: 20px; }
.slider { width: 100%; margin-top: 10px; -webkit-appearance: none; background: #333; height: 6px; border-radius: 3px; }
.slider::-webkit-slider-thumb { -webkit-appearance: none; width: 20px; height: 20px; background: #4e8cff; border-radius: 50%; cursor: pointer; }
.scale { display: flex; justify-content: space-between; font-size: 0.8rem; color: #666; margin-top: 5px; }

/* Módulos */
.modules-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.module-check input { display: none; }
.module-check .box { display: flex; justify-content: space-between; padding: 15px; background: #1f232b; border: 1px solid #333; border-radius: 8px; cursor: pointer; transition: 0.2s; }
.module-check input:checked + .box { border-color: #4e8cff; background: rgba(78, 140, 255, 0.05); }

/* Resumen (Receipt) */
.summary-panel { position: sticky; top: 20px; }
.receipt { background: #fff; color: #333; padding: 30px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
.line-item { display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 0.9rem; color: #555; }
.main-item { font-weight: bold; color: #000; font-size: 1rem; margin-bottom: 15px; }
hr { border: 0; border-top: 1px solid #eee; margin: 20px 0; }
.total { display: flex; justify-content: space-between; align-items: center; font-size: 1.2rem; font-weight: bold; }
.total .price { color: #4e8cff; font-size: 1.6rem; }

.timeline-box { margin: 20px 0; padding: 15px; background: #f4f6f8; border-radius: 8px; font-size: 0.9rem; border-left: 4px solid #4e8cff; }

.btn-consult { width: 100%; background: #000; color: white; padding: 15px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.3s; }
.btn-consult:hover { background: #333; }
.disclaimer { font-size: 0.7rem; color: #999; text-align: center; margin-top: 15px; }
</style>
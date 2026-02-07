<template>
  <div class="orders-wrapper">
    <header class="orders-header">
      <div class="logo-small" @click="$emit('navegar', 'home')">← Volver</div>
      <h2>Mis Solicitudes</h2>
    </header>

    <div class="orders-container">
      
      <div class="stats-row">
        <div class="stat-card">
          <span class="number">{{ pedidos.length }}</span>
          <span class="label">Total Pedidos</span>
        </div>
        <div class="stat-card">
          <span class="number">$ {{ totalInversion.toLocaleString() }}</span>
          <span class="label">Inversión Estimada</span>
        </div>
        <div class="stat-card active-stat">
          <span class="number">{{ pendientes }}</span>
          <span class="label">En Revisión</span>
        </div>
      </div>

      <div v-if="loading" class="loading">Cargando pedidos...</div>
      
      <div v-else-if="pedidos.length > 0" class="orders-list">
        <div v-for="p in pedidos" :key="p.id" class="order-card">
          
          <div class="card-icon">
            {{ p.categoria === 'Hardware' ? '💻' : '🚀' }}
          </div>
          
          <div class="card-info">
            <div class="header-info">
              <h3>{{ p.producto }}</h3>
              <span :class="['status-badge', getStatusClass(p.estado)]">{{ p.estado }}</span>
            </div>
            <p class="detalles">{{ p.detalles }}</p>
            <div class="meta">
              <span class="date">📅 {{ new Date(p.fecha).toLocaleDateString() }}</span>
              <span class="price">💰 ${{ p.precio }} / mes</span>
            </div>
          </div>

        </div>
      </div>

      <div v-else class="empty-state">
        <div class="empty-icon">📭</div>
        <h3>No tienes pedidos activos</h3>
        <p>Explora nuestros servicios de Hardware o Software para comenzar.</p>
        <div class="buttons">
          <button @click="$emit('navegar', 'order')" class="btn-outline">Ver Hardware</button>
          <button @click="$emit('navegar', 'software')" class="btn-outline">Ver Software</button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const emit = defineEmits(['navegar']);
const pedidos = ref([]);
const loading = ref(true);

// Cargar datos del Backend
const fetchPedidos = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/pedidos');
    if (res.ok) pedidos.value = await res.json();
  } catch (e) {
    console.error("Error API:", e);
  } finally {
    loading.value = false;
  }
};

// Computados para las estadísticas
const totalInversion = computed(() => pedidos.value.reduce((acc, p) => acc + p.precio, 0));
const pendientes = computed(() => pedidos.value.filter(p => p.estado === 'Pendiente').length);

const getStatusClass = (status) => {
  if (status === 'Pendiente') return 'status-pending';
  if (status === 'Aprobado') return 'status-approved';
  return 'status-shipped';
};

onMounted(() => fetchPedidos());
</script>

<style scoped>
.orders-wrapper { background: #0f1115; min-height: 100vh; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; }
.orders-header { padding: 1.5rem; background: #161920; display: flex; align-items: center; gap: 20px; border-bottom: 1px solid #2a2e35; }
.logo-small { cursor: pointer; color: #4e8cff; font-weight: bold; }

.orders-container { max-width: 800px; margin: 40px auto; padding: 0 20px; }

/* Stats */
.stats-row { display: flex; gap: 20px; margin-bottom: 40px; }
.stat-card { flex: 1; background: #1f232b; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #2a2e35; }
.stat-card .number { display: block; font-size: 2rem; font-weight: bold; color: #fff; }
.stat-card .label { font-size: 0.9rem; color: #888; }
.active-stat { border-color: #ff9800; background: rgba(255, 152, 0, 0.05); }

/* Lista */
.order-card { background: #1f232b; padding: 20px; border-radius: 12px; margin-bottom: 15px; display: flex; gap: 20px; align-items: center; border: 1px solid #333; transition: 0.2s; }
.order-card:hover { transform: translateX(5px); border-color: #4e8cff; }

.card-icon { font-size: 2.5rem; background: #252a33; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; border-radius: 50%; }
.card-info { flex: 1; }

.header-info { display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px; }
.header-info h3 { margin: 0; color: #fff; font-size: 1.1rem; }

.detalles { color: #aaa; font-size: 0.9rem; margin-bottom: 10px; }
.meta { display: flex; gap: 20px; font-size: 0.85rem; color: #666; font-weight: bold; }

/* Badges */
.status-badge { padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; text-transform: uppercase; font-weight: bold; }
.status-pending { background: rgba(255, 152, 0, 0.2); color: #ff9800; }
.status-approved { background: rgba(0, 200, 83, 0.2); color: #00c853; }

/* Empty State */
.empty-state { text-align: center; padding: 60px 20px; }
.empty-icon { font-size: 4rem; margin-bottom: 20px; opacity: 0.5; }
.buttons { margin-top: 30px; display: flex; justify-content: center; gap: 15px; }
.btn-outline { background: transparent; border: 1px solid #4e8cff; color: #4e8cff; padding: 10px 20px; border-radius: 5px; cursor: pointer; transition: 0.3s; }
.btn-outline:hover { background: #4e8cff; color: #fff; }
</style>
<template>
  <div id="app">
    <HomeView 
      v-if="currentView === 'home'" 
      @navegar="cambiarVista" 
    />

    <DashboardView 
      v-else-if="currentView === 'dashboard'"
      @navegar="cambiarVista" 
    />

    <OrderView
    v-else-if="currentView === 'order'"
    @navegar="cambiarVista"
    />

    <SoftwareView
    v-else-if="currentView === 'software'"
    @navegar="cambiarVista"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import HomeView from './components/HomeView.vue';
import DashboardView from './components/DashboardView.vue';
import OrderView from './components/OrderView.vue';
import SoftwareView from './components/SoftwareView.vue';

// Estado global de navegación
const currentView = ref('home');

// Función para cambiar de vista (la reciben los hijos)
const cambiarVista = (vistaDestino) => {
  currentView.value = vistaDestino;
};
</script>

<style>
/* Estilos Globales (Reset) */
body { margin: 0; font-family: 'Segoe UI', sans-serif; background: #0f1115; }
</style>
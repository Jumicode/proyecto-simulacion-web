<template>
  <div id="app">
    <HomeView 
      v-if="currentView === 'home'" 
      @navegar="cambiarVista" 
    />

    <DashboardView 
      v-else 
      @navegar="cambiarVista" 
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import HomeView from './components/HomeView.vue';
import DashboardView from './components/DashboardView.vue';

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
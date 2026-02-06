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
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  width: 100%;
  min-height: 100vh;
}

.app {
  width: 100%;
  min-height: 100vh;
}
</style>
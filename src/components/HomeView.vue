<template>
  <div class="corporate-container">
    <nav class="navbar">
      <div class="logo">
        <span class="tech">Tech</span><span class="julio">Julio</span> Solutions
      </div>
      <div class="nav-links">
        <a href="#servicios">Servicios</a>
        <a href="#partners">Partners</a>
        <button @click="$emit('navegar', 'dashboard')" class="btn-login">
           Acceso Clientes
        </button>
      </div>
    </nav>

    <header class="hero">
      <div class="hero-content">
        <h1>Transformación Digital Integral</h1>
        <p class="hero-subtitle">
          Unimos <strong>Hardware de Alta Gama</strong> con <strong>Software a Medida</strong>.
        </p>
        <div class="hero-buttons">
          <button @click="$emit('navegar', 'dashboard')" class="btn-primary">Ver Demo Guardian AI</button>
          <button @click="$emit('navegar', 'order')" class="btn-outline">Consultar Leasing</button>
        </div>
      </div>
    </header>

    <section id="servicios" class="services-section">
      <h2>Nuestros Pilares</h2>
      <div class="cards-grid">
        <div class="service-card">
          <div class="icon"></div>
          <h3>Hardware as a Service</h3>
          <p>Leasing de equipos Dell & Lenovo configurados a medida.</p>
        </div>
        <div class="service-card highlight-card">
          <div class="icon"></div>
          <h3>Guardian AI</h3>
          <p>Mantenimiento Predictivo potenciado por TensorFlow.</p>
        </div>

        <div class="service-card">
  <div class="icon"></div>
  <h3>Desarrollo de Software</h3>
  <p>Ingeniería de software ágil (Scrum) para soluciones escalables.</p>
  <ul>
    <li>Apps a Medida (ERP/CRM)</li>
    <li>Equipos Full Stack Senior</li>
  </ul>
  
  <button @click="$emit('navegar', 'software')" class="btn-card">
    Cotizar Proyecto
  </button>
</div>
      </div>
    </section>

    <footer class="footer">
      <p>© 2026 TechJulio Solutions.</p>
    </footer>
  </div>
</template>

<script setup>
// Definimos que este componente puede enviar un evento llamado 'navegar'
const emit = defineEmits(['navegar']);
</script>

<style scoped>
/* Pega aquí todo el CSS relacionado con la Home, Navbar, Hero, etc. */
.corporate-container { background-color: #0f1115; color: white; min-height: 100vh; }
.navbar { display: flex; justify-content: space-between; padding: 1.5rem; background: #161920; }
.logo { font-size: 1.5rem; font-weight: 700; color: white; }
.julio { color: #4e8cff; }
.btn-primary { background: #4e8cff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
.cards-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; padding: 2rem; }
.service-card { background: #1f232b; padding: 20px; border-radius: 10px; }
.footer { text-align: center; padding: 20px; color: #555; }
</style>
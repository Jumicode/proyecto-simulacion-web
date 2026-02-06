<template>
  <div class="corporate-container">
    <!-- Animated Background -->
    <div class="animated-bg">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
      <div class="stars"></div>
    </div>

    <nav class="navbar">
      <div class="logo">
        <span class="tech">Tech</span><span class="julio">Julio</span> Solutions
      </div>
      <div class="nav-links">
        <a href="#servicios" class="nav-link">Servicios</a>
        <a href="#partners" class="nav-link">Partners</a>
        <button @click="$emit('navegar', 'dashboard')" class="btn-login">
          <span>Acceso Clientes</span>
          <div class="btn-glow"></div>
        </button>
      </div>
    </nav>

    <header class="hero">
      <div class="hero-content">
        <h1 class="hero-title">
          <span class="word">Transformación</span>
          <span class="word">Digital</span>
          <span class="word">Integral</span>
        </h1>
        <p class="hero-subtitle">
          Unimos <strong>Hardware de Alta Gama</strong> con <strong>Software a Medida</strong>.
        </p>
        <div class="hero-buttons">
          <button @click="$emit('navegar', 'dashboard')" class="btn-primary">
            <span>Ver Demo Guardian AI</span>
            <div class="btn-shine"></div>
          </button>
          <button @click="$emit('navegar', 'order')" class="btn-outline">
            <span>Consultar Leasing</span>
          </button>
        </div>
      </div>
      <div class="hero-decoration">
        <div class="floating-card card-1"></div>
        <div class="floating-card card-2"></div>
        <div class="floating-card card-3"></div>
      </div>
    </header>

    <section id="servicios" class="services-section">
      <h2 class="section-title">Nuestros Pilares</h2>
      <div class="cards-grid">
        <div class="service-card">
          <div class="card-glow"></div>
          <div class="icon icon-hardware">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <rect x="2" y="3" width="20" height="14" rx="2" stroke-width="2"/>
              <line x1="8" y1="21" x2="16" y2="21" stroke-width="2"/>
              <line x1="12" y1="17" x2="12" y2="21" stroke-width="2"/>
            </svg>
          </div>
          <h3>Hardware as a Service</h3>
          <p>Leasing de equipos Dell & Lenovo configurados a medida.</p>
          <div class="card-bottom">
            <span class="badge">Premium</span>
          </div>
        </div>

        <div class="service-card highlight-card">
          <div class="card-glow highlight-glow"></div>
          <div class="icon icon-ai">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M12 2L2 7l10 5 10-5-10-5z" stroke-width="2"/>
              <path d="M2 17l10 5 10-5" stroke-width="2"/>
              <path d="M2 12l10 5 10-5" stroke-width="2"/>
            </svg>
          </div>
          <h3>Guardian AI</h3>
          <p>Mantenimiento Predictivo potenciado por TensorFlow.</p>
          <div class="card-bottom">
            <span class="badge badge-featured">IA Avanzada</span>
          </div>
        </div>

        <div class="service-card">
          <div class="card-glow"></div>
          <div class="icon icon-code">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <polyline points="16 18 22 12 16 6" stroke-width="2"/>
              <polyline points="8 6 2 12 8 18" stroke-width="2"/>
            </svg>
          </div>
          <h3>Desarrollo de Software</h3>
          <p>Ingeniería de software ágil (Scrum) para soluciones escalables.</p>
          <ul class="feature-list">
            <li>Apps a Medida (ERP/CRM)</li>
            <li>Equipos Full Stack Senior</li>
          </ul>
          <button @click="$emit('navegar', 'software')" class="btn-card">
            Cotizar Proyecto
            <svg class="arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <line x1="5" y1="12" x2="19" y2="12" stroke-width="2"/>
              <polyline points="12 5 19 12 12 19" stroke-width="2"/>
            </svg>
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
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.corporate-container {
  background-color: #0a0b0f;
  color: white;
  min-height: 100vh;
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
   NAVBAR
   ============================================ */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 3rem;
  background: rgba(15, 17, 21, 0.7);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  position: sticky;
  top: 0;
  z-index: 100;
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

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  letter-spacing: -0.5px;
}

.tech {
  color: white;
}

.julio {
  color: #4e8cff;
  text-shadow: 0 0 20px rgba(78, 140, 255, 0.5);
}

.nav-links {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.nav-link {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-weight: 500;
  position: relative;
  transition: color 0.3s ease;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #4e8cff, #00d4ff);
  transition: width 0.3s ease;
}

.nav-link:hover {
  color: white;
}

.nav-link:hover::after {
  width: 100%;
}

.btn-login {
  background: rgba(78, 140, 255, 0.1);
  color: #4e8cff;
  padding: 0.7rem 1.5rem;
  border: 1px solid rgba(78, 140, 255, 0.3);
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.btn-login:hover {
  background: rgba(78, 140, 255, 0.2);
  border-color: #4e8cff;
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(78, 140, 255, 0.3);
}

.btn-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(78, 140, 255, 0.4), transparent);
  transform: translate(-50%, -50%) scale(0);
  transition: transform 0.5s ease;
}

.btn-login:hover .btn-glow {
  transform: translate(-50%, -50%) scale(2);
}

/* ============================================
   HERO SECTION
   ============================================ */
.hero {
  position: relative;
  z-index: 1;
  padding: 8rem 3rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-height: 70vh;
}

.hero-content {
  max-width: 700px;
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

.hero-title {
  font-size: 4rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, #ffffff 0%, #4e8cff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.word {
  display: inline-block;
  animation: wordFadeIn 0.8s ease-out backwards;
}

.word:nth-child(1) { animation-delay: 0.2s; }
.word:nth-child(2) { animation-delay: 0.4s; }
.word:nth-child(3) { animation-delay: 0.6s; }

@keyframes wordFadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero-subtitle {
  font-size: 1.3rem;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 2.5rem;
  line-height: 1.6;
  animation: fadeInUp 1s ease-out 0.3s backwards;
}

.hero-subtitle strong {
  color: #4e8cff;
  font-weight: 600;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
  animation: fadeInUp 1s ease-out 0.5s backwards;
}

.btn-primary {
  background: linear-gradient(135deg, #4e8cff 0%, #0066ff 100%);
  color: white;
  padding: 1rem 2rem;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(78, 140, 255, 0.3);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 40px rgba(78, 140, 255, 0.5);
}

.btn-primary:active {
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

.btn-primary:hover .btn-shine {
  left: 100%;
}

.btn-outline {
  background: transparent;
  color: white;
  padding: 1rem 2rem;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.btn-outline:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.4);
  transform: translateY(-3px);
}

.hero-decoration {
  position: relative;
  width: 400px;
  height: 400px;
}

.floating-card {
  position: absolute;
  background: linear-gradient(135deg, rgba(78, 140, 255, 0.1), rgba(0, 212, 255, 0.1));
  border: 1px solid rgba(78, 140, 255, 0.2);
  border-radius: 15px;
  backdrop-filter: blur(10px);
  animation: floatCard 6s ease-in-out infinite;
}

.card-1 {
  width: 200px;
  height: 150px;
  top: 0;
  left: 0;
  animation-delay: 0s;
}

.card-2 {
  width: 180px;
  height: 120px;
  top: 100px;
  right: 50px;
  animation-delay: -2s;
}

.card-3 {
  width: 150px;
  height: 100px;
  bottom: 50px;
  left: 100px;
  animation-delay: -4s;
}

@keyframes floatCard {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(2deg);
  }
}

/* ============================================
   SERVICES SECTION
   ============================================ */
.services-section {
  position: relative;
  z-index: 1;
  padding: 6rem 3rem;
}

.section-title {
  text-align: center;
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 4rem;
  background: linear-gradient(135deg, #ffffff 0%, #4e8cff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.service-card {
  background: rgba(20, 24, 33, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.05);
  padding: 2.5rem;
  border-radius: 20px;
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
  transition: all 0.4s ease;
  animation: cardFadeIn 0.6s ease-out backwards;
}

.service-card:nth-child(1) { animation-delay: 0.1s; }
.service-card:nth-child(2) { animation-delay: 0.2s; }
.service-card:nth-child(3) { animation-delay: 0.3s; }

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

.service-card:hover {
  transform: translateY(-10px);
  border-color: rgba(78, 140, 255, 0.3);
  box-shadow: 0 20px 60px rgba(78, 140, 255, 0.2);
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

.service-card:hover .card-glow {
  opacity: 1;
}

.highlight-card {
  background: linear-gradient(135deg, rgba(78, 140, 255, 0.1), rgba(0, 212, 255, 0.05));
  border: 1px solid rgba(78, 140, 255, 0.3);
}

.highlight-glow {
  background: radial-gradient(circle, rgba(78, 140, 255, 0.2), transparent 50%);
}

.icon {
  width: 60px;
  height: 60px;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, rgba(78, 140, 255, 0.2), rgba(0, 212, 255, 0.1));
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #4e8cff;
  transition: all 0.3s ease;
}

.service-card:hover .icon {
  transform: scale(1.1) rotate(5deg);
  box-shadow: 0 10px 30px rgba(78, 140, 255, 0.3);
}

.icon svg {
  width: 30px;
  height: 30px;
}

.service-card h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: white;
}

.service-card p {
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.feature-list {
  list-style: none;
  margin-bottom: 1.5rem;
}

.feature-list li {
  color: rgba(255, 255, 255, 0.7);
  padding-left: 1.5rem;
  margin-bottom: 0.5rem;
  position: relative;
}

.feature-list li::before {
  content: '→';
  position: absolute;
  left: 0;
  color: #4e8cff;
  font-weight: bold;
}

.card-bottom {
  margin-top: 1.5rem;
}

.badge {
  display: inline-block;
  padding: 0.4rem 1rem;
  background: rgba(78, 140, 255, 0.1);
  border: 1px solid rgba(78, 140, 255, 0.3);
  border-radius: 20px;
  color: #4e8cff;
  font-size: 0.85rem;
  font-weight: 600;
}

.badge-featured {
  background: linear-gradient(135deg, rgba(78, 140, 255, 0.2), rgba(0, 212, 255, 0.2));
  border-color: #4e8cff;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(78, 140, 255, 0.4);
  }
  50% {
    box-shadow: 0 0 0 10px rgba(78, 140, 255, 0);
  }
}

.btn-card {
  background: linear-gradient(135deg, rgba(78, 140, 255, 0.1), rgba(0, 212, 255, 0.1));
  color: #4e8cff;
  padding: 0.8rem 1.5rem;
  border: 1px solid rgba(78, 140, 255, 0.3);
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  margin-top: 1rem;
}

.btn-card:hover {
  background: linear-gradient(135deg, rgba(78, 140, 255, 0.2), rgba(0, 212, 255, 0.2));
  border-color: #4e8cff;
  transform: translateX(5px);
}

.arrow-icon {
  width: 16px;
  height: 16px;
  transition: transform 0.3s ease;
}

.btn-card:hover .arrow-icon {
  transform: translateX(5px);
}

/* ============================================
   FOOTER
   ============================================ */
.footer {
  position: relative;
  z-index: 1;
  text-align: center;
  padding: 3rem;
  color: rgba(255, 255, 255, 0.3);
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  background: rgba(10, 11, 15, 0.5);
  backdrop-filter: blur(10px);
}

/* ============================================
   RESPONSIVE
   ============================================ */
@media (max-width: 768px) {
  .navbar {
    padding: 1rem;
    flex-direction: column;
    gap: 1rem;
  }

  .nav-links {
    flex-direction: column;
    gap: 1rem;
  }

  .hero {
    flex-direction: column;
    padding: 4rem 1.5rem;
    text-align: center;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    font-size: 1.1rem;
  }

  .hero-buttons {
    flex-direction: column;
    width: 100%;
  }

  .hero-buttons button {
    width: 100%;
  }

  .hero-decoration {
    display: none;
  }

  .cards-grid {
    grid-template-columns: 1fr;
    padding: 1rem;
  }

  .services-section {
    padding: 3rem 1rem;
  }

  .section-title {
    font-size: 2rem;
  }
}
</style>

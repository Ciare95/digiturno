<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">
          <span class="highlight">Transforma</span> la experiencia de atención al cliente
        </h1>
        <p class="hero-subtitle">
          El sistema de gestión de turnos más avanzado para tu negocio
        </p>
        <div class="cta-buttons">
          <router-link to="/login" class="btn btn-outline">Iniciar Ahora</router-link>
          <router-link to="/solicitar-turno" class="btn btn-outline">Solicitar turno</router-link>
        </div>
      </div>
      <div class="scroll-indicator">
        <span>Desliza para descubrir</span>
        <svg width="24" height="24" viewBox="0 0 24 24"><path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>
    </section>

    <!-- Value Proposition -->
    <section id="solucion" class="section value-prop">
      <div class="container">
        <h2 class="section-title">Solución Integral para la Gestión de Turnos</h2>
        <div class="value-grid">
          <div class="value-card" v-for="(item, index) in valueProps" :key="index" :style="{'--delay': index * 0.1 + 's'}">
            <div class="value-icon">
              <i :class="['fas', item.icon]"></i>
            </div>
            <h3>{{ item.title }}</h3>
            <p>{{ item.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Industries Section -->
    <section class="section industries">
      <div class="container">
        <h2 class="section-title">Perfecto para todo tipo de negocios</h2>
        <div class="industry-grid">
          <div v-for="(industry, index) in industries" :key="index" class="industry-item">
            <div class="industry-icon">
              <i :class="['fas', 'fa-2x', industry.icon]"></i>
            </div>
            <span>{{ industry.name }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Porque elegirnos -->
    <section class="section why-us">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">¿Por qué elegirnos?</h2>
          <p class="section-subtitle">La solución de gestión de turnos que tu negocio necesita</p>
        </div>
        <div class="benefits-grid">
          <div class="benefit-card" v-for="(benefit, index) in benefits" :key="index" :style="{ '--accent-color': benefit.color }">
            <div class="benefit-icon">
              <i :class="['fas', benefit.icon]"></i>
            </div>
            <h3>{{ benefit.title }}</h3>
            <p>{{ benefit.description }}</p>
            <div class="benefit-features">
              <div class="feature" v-for="(feature, fIndex) in benefit.features" :key="fIndex">
                <i class="fas fa-check"></i>
                <span>{{ feature }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="section cta-section">
      <div class="container">
        <h2>¿Listo para la revolución de la atención al cliente?</h2>
        <p>Únete a miles de negocios que ya optimizan su servicio</p>
        <div class="cta-buttons">
          <router-link to="/login" class="btn btn-primary btn-large">Comenzar Ahora</router-link>
          <a href="#precios" class="btn btn-outline btn-large">Ver Planes</a>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  data() {
    return {
      valueProps: [
        { icon: 'fa-clock', title: 'Ahorro de Tiempo', description: 'Reducción de hasta un 60% en tiempos de espera' },
        { icon: 'fa-chart-line', title: 'Métricas en Tiempo Real', description: 'Toma decisiones basadas en datos actualizados' },
        { icon: 'fa-users', title: 'Satisfacción del Cliente', description: 'Mejora la experiencia de tus clientes significativamente' },
        { icon: 'fa-bolt', title: 'Implementación Rápida', description: 'Comienza en menos de 24 horas' },
        { icon: 'fa-mobile-alt', title: 'Acceso Móvil', description: 'Gestiona desde cualquier dispositivo' },
        { icon: 'fa-shield-alt', title: 'Seguro y Confiable', description: 'Tus datos siempre protegidos' }
      ],
      industries: [
        { name: 'Bancos', icon: 'fa-bank' },
        { name: 'Restaurantes', icon: 'fa-utensils' },
        { name: 'Gobierno', icon: 'fa-landmark' },
        { name: 'Tiendas', icon: 'fa-shopping-bag' },
        { name: 'Servicios', icon: 'fa-briefcase' }
      ],
      benefits: [
        {
          icon: 'fa-rocket',
          title: 'Implementación Rápida',
          description: 'Comienza a operar en cuestión de minutos, no de días',
          color: '#4f46e5',
          features: ['Configuración guiada paso a paso', 'Plantillas personalizables', 'Migración de datos incluida']
        },
        {
          icon: 'fa-shield-alt',
          title: 'Seguridad Garantizada',
          description: 'Protección de datos de nivel empresarial',
          color: '#10b981',
          features: ['Cifrado de extremo a extremo', 'Cumplimiento normativo', 'Copias de seguridad automáticas']
        },
        {
          icon: 'fa-headset',
          title: 'Soporte Premium',
          description: 'Asistencia cuando más la necesitas',
          color: '#f59e0b',
          features: ['Soporte 24/7', 'Tiempo de respuesta garantizado', 'Asesoría personalizada']
        },
        {
          icon: 'fa-sync',
          title: 'Actualizaciones Constantes',
          description: 'Siempre tendrás la mejor versión',
          color: '#ec4899',
          features: ['Mejoras continuas', 'Nuevas características', 'Sin costos adicionales']
        }
      ]
    };
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

:root {
  --primary: #2563eb;
  --primary-dark: #1d4ed8;
  --text: #1f2937;
  --text-light: #6b7280;
  --bg-light: #f9fafb;
}

* { box-sizing: border-box; }

body {
  font-family: 'Inter', sans-serif;
  color: var(--text);
  line-height: 1.6;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.section {
  padding: 4rem 0;
}

.section-title {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 2rem;
  position: relative;
}

.section-title::after {
  content: '';
  display: block;
  margin: 0.5rem auto 0;
  width: 60px;
  height: 4px;
  background: linear-gradient(90deg, var(--primary), #3b82f6);
  border-radius: 2px;
}

.hero {
  min-height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
  color: white;
  text-align: center;
  position: relative;
  padding: 2rem 1rem;
}

.hero-content {
  z-index: 2;
  max-width: 900px;
  margin: 0 auto;
}

.hero-title {
  font-size: 2.5rem;
  margin-bottom: 1.5rem;
}

.hero-subtitle {
  font-size: 1.25rem;
  opacity: 0.9;
  margin-bottom: 2rem;
}

.highlight {
  background: linear-gradient(90deg, #60a5fa, #93c5fd);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.cta-buttons {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 1rem;
  margin: 2rem 0;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  transition: background 0.3s;
  cursor: pointer;
  border: 2px solid transparent;
  font-size: 1rem;
  margin: 0.5rem;
}

.btn-primary {
  background: var(--primary);
  color: white;
}

.btn-primary:hover {
  background: var(--primary-dark);
}

.btn-outline {
  background: transparent;
  color: white;
  border-color: rgba(255,255,255,0.3);
}

.btn-outline:hover {
  background: rgba(255,255,255,0.1);
  border-color: white;
}

.btn-large {
  padding: 1rem 2.5rem;
  font-size: 1.1rem;
}

.scroll-indicator {
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  color: rgba(255,255,255,0.7);
  font-size: 0.875rem;
  z-index: 2;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0) translateX(-50%); }
  40% { transform: translateY(-10px) translateX(-50%); }
  60% { transform: translateY(-5px) translateX(-50%); }
}

.value-prop {
  background: white;
}

.value-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.value-card {
  background: white;
  border-radius: 1rem;
  padding: 2rem 1.5rem;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.6s ease-out forwards;
  animation-delay: var(--delay, 0s);
}

@keyframes fadeInUp {
  to { opacity: 1; transform: translateY(0); }
}

.value-icon {
  width: 60px;
  height: 60px;
  margin: 0 auto 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e0f2fe 0%, #dbeafe 100%);
  border-radius: 50%;
  color: var(--primary);
  font-size: 2rem;
}

.industries {
  background: var(--bg-light);
}

.industry-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.industry-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 1.5rem 1rem;
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.industry-icon {
  width: 40px;
  height: 40px;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e0f2fe 0%, #dbeafe 100%);
  border-radius: 50%;
  color: var(--primary);
  font-size: 1.5rem;
}

.why-us {
  background: #f8fafc;
}

.section-header {
  text-align: center;
  margin-bottom: 2rem;
}

.benefits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.benefit-card {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  border-top: 4px solid var(--accent-color);
}

.benefit-icon {
  width: 40px;
  height: 40px;
  background: rgba(79,70,229,0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
  font-size: 1.5rem;
  color: var(--accent-color);
}

.benefit-features {
  border-top: 1px solid #e5e7eb;
  padding-top: 1rem;
}

.feature {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
  color: #4b5563;
  font-size: 0.95rem;
}

.feature i {
  color: #10b981;
  margin-right: 0.5rem;
  font-size: 0.875rem;
}

.cta-section {
  padding: 4rem 2rem;
  text-align: center;
  background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
  color: white;
}

.cta-section h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.cta-section p {
  font-size: 1.1rem;
  margin-bottom: 2rem;
  color: rgba(255,255,255,0.9);
}

@media (max-width: 768px) {
  .section { padding: 2rem 0; }
  .hero-title { font-size: 1.5rem; }
  .value-grid, .benefits-grid, .industry-grid { grid-template-columns: 1fr; }
  .cta-section h2 { font-size: 1.25rem; }
}
</style>
<template>
  <div class="home">
    <!-- Hero Section with Animated Background -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">
          <span class="highlight">Transforma</span> la experiencia de atención al cliente
        </h1>
        <p class="hero-subtitle">
          El sistema de gestión de turnos más avanzado para tu negocio
        </p>
        <div class="cta-buttons">
          <router-link to="/login" class="btn btn-primary">
            Iniciar Ahora
          </router-link>
          <a href="#solucion" class="btn btn-outline">
            Ver Demo
          </a>
        </div>
      </div>
      <div class="scroll-indicator">
        <span>Desliza para descubrir</span>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
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

    <!-- Metrics Section -->
    <section class="section metrics">
      <div class="container">
        <h2 class="section-title">Métricas que hablan por sí solas</h2>
        <div class="metrics-grid">
          <div class="metric-card" v-for="(metric, index) in metrics" :key="index">
            <div class="metric-value" v-html="metric.value"></div>
            <div class="metric-label">{{ metric.label }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonials Section -->
    <section class="section testimonials">
      <div class="container">
        <h2 class="section-title">Lo que dicen nuestros clientes</h2>
        <div class="testimonials-grid">
          <div class="testimonial-card" v-for="(testimonial, index) in testimonials" :key="index">
            <div class="testimonial-content">
              <p>"{{ testimonial.quote }}"</p>
            </div>
            <div class="testimonial-author">
              <div class="author-avatar">
                <i :class="['fas', testimonial.avatar]"></i>
              </div>
              <div class="author-info">
                <h4>{{ testimonial.name }}</h4>
                <span>{{ testimonial.position }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Why Choose Us Section -->
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
        
        <div class="stats-container">
          <div class="stat-item" v-for="(stat, index) in stats" :key="index">
            <div class="stat-value">{{ stat.value }}<span v-if="stat.unit">{{ stat.unit }}</span></div>
            <div class="stat-label">{{ stat.label }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section class="section how-it-works" id="como-funciona">
      <div class="container">
        <div class="section-header text-center">
          <span class="section-pre-title">Proceso Simple</span>
          <h2 class="section-title">Optimiza tu flujo de trabajo en 4 pasos</h2>
          <p class="section-subtitle">Una solución integral diseñada para simplificar la gestión de turnos en tu negocio</p>
        </div>
        
        <div class="process-steps">
          <div class="process-track"></div>
          
          <div class="step" v-for="(step, index) in howItWorks" :key="index" 
               :class="{ 'active': activeStep === index + 1, 'step-reverse': index % 2 !== 0 }" 
               @mouseenter="setActiveStep(index + 1)" 
               @mouseleave="resetActiveStep">
            
            <div class="step-number-container">
              <div class="step-number">{{ index + 1 }}</div>
              <div class="step-connector"></div>
            </div>
            
            <div class="step-content-wrapper">
              <div class="step-content">
                <div class="step-icon-container">
                  <div class="step-icon">
                    <font-awesome-icon :icon="step.icon" />
                  </div>
                </div>
                <div class="step-text">
                  <h3 class="step-title">{{ step.title }}</h3>
                  <p class="step-description">{{ step.description }}</p>
                  <ul class="step-features">
                    <li v-for="(feature, fIndex) in step.features" :key="fIndex" class="feature-item">
                      <font-awesome-icon icon="check-circle" />
                      <span>{{ feature }}</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            
            <div class="step-illustration">
              <div class="illustration-container">
                <div class="illustration-bg" :style="{ backgroundColor: step.color + '15' }"></div>
                <div class="illustration-content">
                  <img v-if="step.image" :src="step.image" :alt="step.title" class="illustration-img">
                  <div v-else class="illustration-placeholder">
                    <font-awesome-icon :icon="step.illustrationIcon || 'mobile-alt'" size="2x" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="cta-container">
          <div class="cta-card">
            <div class="cta-content">
              <h3>¿Listo para optimizar tu negocio?</h3>
              <p>Únete a miles de empresas que ya mejoraron su gestión de turnos con nuestra solución</p>
            </div>
            <router-link to="/registro" class="btn btn-primary btn-large btn-icon">
              Comenzar Ahora <font-awesome-icon icon="arrow-right" />
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing Plans Section -->
    <section class="section pricing" id="precios">
      <div class="container">
        <h2 class="section-title">Planes a tu medida</h2>
        <p class="section-subtitle">Elige el plan que mejor se adapte a las necesidades de tu negocio</p>
        
        <div class="pricing-grid">
          <div class="pricing-card" v-for="(plan, index) in pricingPlans" :key="index" :class="{ 'popular': plan.popular }">
            <div class="pricing-header">
              <h3>{{ plan.name }}</h3>
              <div class="price">
                <span class="amount">{{ plan.price }}</span>
                <span class="period">/mes</span>
              </div>
              <p class="description">{{ plan.description }}</p>
              <router-link :to="plan.ctaLink" class="btn" :class="plan.popular ? 'btn-primary' : 'btn-outline'">
                {{ plan.ctaText }}
              </router-link>
            </div>
            <div class="pricing-features">
              <h4>Incluye:</h4>
              <ul>
                <li v-for="(feature, fIndex) in plan.features" :key="fIndex">
                  <i class="fas fa-check"></i> {{ feature }}
                </li>
              </ul>
            </div>
            <div v-if="plan.popular" class="popular-badge">Más Popular</div>
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
          <router-link to="/login" class="btn btn-primary btn-large">
            Comenzar Ahora
          </router-link>
          <a href="#precios" class="btn btn-outline btn-large">
            Ver Planes
          </a>
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
      activeStep: 0,
      howItWorks: [
        {
          icon: 'fa-user-cog',
          title: 'Configuración Inicial',
          description: 'Comienza en minutos con nuestra plataforma intuitiva. Configura tu negocio, servicios y disponibilidad en simples pasos.',
          features: [
            'Registro rápido y sencillo',
            'Personalización de marca',
            'Configuración guiada paso a paso',
            'Soporte 24/7 durante la configuración'
          ],
          illustrationIcon: 'fa-cog',
          color: '#4f46e5',
          image: ''
        },
        {
          icon: 'fa-calendar-plus',
          title: 'Programación Inteligente',
          description: 'Gestiona horarios, servicios y personal con nuestra avanzada herramienta de programación.',
          features: [
            'Calendario interactivo',
            'Múltiples ubicaciones',
            'Personalización de servicios',
            'Gestión de recursos'
          ],
          illustrationIcon: 'fa-calendar-check',
          color: '#10b981',
          image: ''
        },
        {
          icon: 'fa-mobile-alt',
          title: 'Experiencia del Cliente',
          description: 'Ofrece a tus clientes una forma moderna y conveniente de agendar citas en cualquier momento y lugar.',
          features: [
            'Portal de autoservicio',
            'Confirmaciones automáticas',
            'Recordatorios personalizables',
            'Integración con calendarios'
          ],
          illustrationIcon: 'fa-calendar-plus',
          color: '#f59e0b',
          image: ''
        },
        {
          icon: 'fa-chart-line',
          title: 'Crecimiento y Análisis',
          description: 'Toma decisiones basadas en datos y haz crecer tu negocio con nuestras herramientas analíticas.',
          features: [
            'Panel de control en tiempo real',
            'Reportes personalizables',
            'Métricas de rendimiento',
            'Encuestas de satisfacción'
          ],
          illustrationIcon: 'fa-chart-pie',
          color: '#ec4899',
          image: ''
        }
      ],
      valueProps: [
        {
          icon: 'fa-clock',
          title: 'Ahorro de Tiempo',
          description: 'Reducción de hasta un 60% en tiempos de espera'
        },
        {
          icon: 'fa-chart-line',
          title: 'Métricas en Tiempo Real',
          description: 'Toma decisiones basadas en datos actualizados'
        },
        {
          icon: 'fa-users',
          title: 'Satisfacción del Cliente',
          description: 'Mejora la experiencia de tus clientes significativamente'
        },
        {
          icon: 'fa-bolt',
          title: 'Implementación Rápida',
          description: 'Comienza en menos de 24 horas'
        },
        {
          icon: 'fa-mobile-alt',
          title: 'Acceso Móvil',
          description: 'Gestiona desde cualquier dispositivo'
        },
        {
          icon: 'fa-shield-alt',
          title: 'Seguro y Confiable',
          description: 'Tus datos siempre protegidos'
        }
      ],
      industries: [
        { name: 'Bancos', icon: 'fa-bank' },
        { name: 'Clínicas', icon: 'fa-hospital' },
        { name: 'Restaurantes', icon: 'fa-utensils' },
        { name: 'Gobierno', icon: 'fa-landmark' },
        { name: 'Retail', icon: 'fa-shopping-bag' },
        { name: 'Servicios', icon: 'fa-briefcase' }
      ],
      metrics: [
        { value: '98<small>%</small>', label: 'Satisfacción del Cliente' },
        { value: '10k<small>+</small>', label: 'Turnos Gestionados' },
        { value: '500<small>+</small>', label: 'Empresas Confían en Nosotros' },
        { value: '60<small>%</small>', label: 'Reducción en Tiempos de Espera' }
      ],
      testimonials: [
        {
          quote: 'La implementación fue sencilla y el impacto en nuestro negocio fue inmediato. Nuestros clientes están más satisfechos y nuestro personal más organizado.',
          name: 'Carlos Méndez',
          position: 'Gerente General, Clínica Central',
          avatar: 'fa-user-md'
        },
        {
          quote: 'El sistema de gestión de turnos ha transformado nuestra forma de atender. Ahora podemos manejar el flujo de clientes de manera más eficiente y profesional.',
          name: 'Ana Rodríguez',
          position: 'Directora de Operaciones, Banco Nacional',
          avatar: 'fa-building'
        },
        {
          quote: 'La plataforma es intuitiva y poderosa. Hemos reducido los tiempos de espera y mejorado significativamente la experiencia de nuestros clientes.',
          name: 'Luis Torres',
          position: 'Dueño, Restaurante El Buen Sabor',
          avatar: 'fa-utensils'
        }
      ],
      benefits: [
        {
          icon: 'fa-rocket',
          title: 'Implementación Rápida',
          description: 'Comienza a operar en cuestión de minutos, no de días',
          color: '#4f46e5',
          features: [
            'Configuración guiada paso a paso',
            'Plantillas personalizables',
            'Migración de datos incluida'
          ]
        },
        {
          icon: 'fa-shield-alt',
          title: 'Seguridad Garantizada',
          description: 'Protección de datos de nivel empresarial',
          color: '#10b981',
          features: [
            'Cifrado de extremo a extremo',
            'Cumplimiento normativo',
            'Copias de seguridad automáticas'
          ]
        },
        {
          icon: 'fa-headset',
          title: 'Soporte Premium',
          description: 'Asistencia cuando más la necesitas',
          color: '#f59e0b',
          features: [
            'Soporte 24/7',
            'Tiempo de respuesta garantizado',
            'Asesoría personalizada'
          ]
        },
        {
          icon: 'fa-sync',
          title: 'Actualizaciones Constantes',
          description: 'Siempre tendrás la mejor versión',
          color: '#ec4899',
          features: [
            'Mejoras continuas',
            'Nuevas características',
            'Sin costos adicionales'
          ]
        }
      ],
      stats: [
        { value: '99.9', unit: '%', label: 'Tiempo de actividad' },
        { value: '24/7', label: 'Soporte disponible' },
        { value: '5', unit: 'min', label: 'Tiempo promedio de respuesta' },
        { value: '10k+', label: 'Clientes satisfechos' }
      ],
      metrics: [
        { value: '98<small>%</small>', label: 'Satisfacción del Cliente' },
        { value: '10k<small>+</small>', label: 'Turnos Gestionados' },
        { value: '500<small>+</small>', label: 'Empresas Confían en Nosotros' },
        { value: '60<small>%</small>', label: 'Reducción en Tiempos de Espera' }
      ],
      testimonials: [
        {
          quote: 'La implementación fue sencilla y el impacto en nuestro negocio fue inmediato. Nuestros clientes están más satisfechos y nuestro personal más organizado.',
          name: 'Carlos Méndez',
          position: 'Gerente General, Clínica Central',
          avatar: 'fa-user-md'
        },
        {
          quote: 'El sistema de gestión de turnos ha transformado nuestra forma de atender. Ahora podemos manejar el flujo de clientes de manera más eficiente y profesional.',
          name: 'Ana Rodríguez',
          position: 'Directora de Operaciones, Banco Nacional',
          avatar: 'fa-building'
        },
        {
          quote: 'La plataforma es intuitiva y poderosa. Hemos reducido los tiempos de espera y mejorado significativamente la experiencia de nuestros clientes.',
          name: 'Luis Torres',
          position: 'Dueño, Restaurante El Buen Sabor',
          avatar: 'fa-utensils'
        }
      ],
      featuresComparison: [
        { name: 'Panel de Control en Tiempo Real', others: true, details: 'Con análisis avanzados' },
        { name: 'Integración con Sistemas Existentes', others: false, details: 'API abierta y documentada' },
        { name: 'Soporte 24/7', others: false, details: 'Asistencia prioritaria' },
        { name: 'Personalización Total', others: true, details: 'Sin límites de personalización' },
        { name: 'Capacitación Incluida', others: false, details: 'Sesiones personalizadas' },
        { name: 'Actualizaciones Gratuitas', others: true, details: 'Mejoras continuas' }
      ]
    };
  },
  methods: {
    setActiveStep(step) {
      this.activeStep = step;
    },
    resetActiveStep() {
      this.activeStep = 0;
    }
  },
  metaInfo: {
    title: 'Sistema de Gestión de Turnos | Mejora la Atención al Cliente',
    meta: [
      { name: 'description', content: 'La solución definitiva para la gestión de turnos en cualquier negocio. Optimiza tiempos, mejora la experiencia del cliente y aumenta la eficiencia operativa.' },
      { property: 'og:image', content: '/images/og-image.jpg' }
    ]
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');
/* How It Works Section */
.how-it-works {
  background-color: #fcfcff;
  position: relative;
  overflow: hidden;
  padding: 6rem 0;
}

.section-header {
  max-width: 800px;
  margin: 0 auto 5rem;
  text-align: center;
}

.section-pre-title {
  display: inline-block;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--primary);
  margin-bottom: 1rem;
  position: relative;
  padding-left: 2.5rem;
}

.section-pre-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  width: 2rem;
  height: 2px;
  background: var(--primary);
  transform: translateY(-50%);
}

.process-steps {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 0;
}

.process-track {
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(to bottom, 
    rgba(79, 70, 229, 0.1) 0%, 
    rgba(79, 70, 229, 0.6) 20%, 
    rgba(79, 70, 229, 0.6) 80%, 
    rgba(79, 70, 229, 0.1) 100%);
  transform: translateX(-50%);
  z-index: 1;
}

.step {
  display: flex;
  margin-bottom: 8rem;
  position: relative;
  z-index: 2;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  opacity: 0.9;
}

.step:last-child {
  margin-bottom: 4rem;
}

.step-reverse {
  flex-direction: row-reverse;
}

.step.active {
  opacity: 1;
}

.step-number-container {
  flex: 0 0 100px;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 3;
}

.step-number {
  width: 60px;
  height: 60px;
  background: white;
  border: 2px solid var(--primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary);
  box-shadow: 0 10px 25px rgba(79, 70, 229, 0.15);
  position: relative;
  z-index: 2;
  transition: all 0.3s ease;
}

.step.active .step-number {
  background: var(--primary);
  color: white;
  transform: scale(1.1);
  box-shadow: 0 15px 30px rgba(79, 70, 229, 0.25);
}

.step-connector {
  position: absolute;
  top: 60px;
  bottom: -8rem;
  width: 2px;
  background: linear-gradient(to bottom, 
    rgba(79, 70, 229, 0.6),
    rgba(79, 70, 229, 0.3) 50%,
    rgba(79, 70, 229, 0.1));
  z-index: 1;
}

.step:last-child .step-connector {
  display: none;
}

.step-content-wrapper {
  flex: 1;
  padding: 0 3rem;
  position: relative;
  z-index: 2;
}

.step-content {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(0, 0, 0, 0.03);
  position: relative;
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.step.active .step-content {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
}

.step-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(to bottom, var(--primary), #60a5fa);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.step.active .step-content::before {
  opacity: 1;
}

.step-icon-container {
  padding: 2rem 2rem 0;
}

.step-icon {
  width: 60px;
  height: 60px;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
  background: linear-gradient(135deg, var(--primary), #60a5fa);
  box-shadow: 0 10px 20px rgba(79, 70, 229, 0.25);
  transition: all 0.3s ease;
}

.step.active .step-icon {
  transform: rotate(5deg) scale(1.05);
  box-shadow: 0 15px 30px rgba(79, 70, 229, 0.35);
}

.step-text {
  padding: 0 2rem 2rem;
}

.step-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
  margin: 1.5rem 0 1rem;
  position: relative;
  display: inline-block;
}

.step-title::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 40px;
  height: 3px;
  background: linear-gradient(90deg, var(--primary), #60a5fa);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.step.active .step-title::after {
  width: 60px;
}

.step-description {
  color: #6b7280;
  margin-bottom: 1.5rem;
  line-height: 1.7;
  font-size: 1.05rem;
}

.step-features {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px dashed rgba(0, 0, 0, 0.08);
  list-style: none;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 0.75rem;
  color: #4b5563;
  font-size: 0.95rem;
  line-height: 1.6;
  transition: all 0.2s ease;
}

.step.active .feature-item {
  transform: translateX(5px);
}

.feature-item i {
  color: #10b981;
  margin-right: 0.75rem;
  font-size: 1rem;
  margin-top: 0.2rem;
  flex-shrink: 0;
}

.step-illustration {
  flex: 0 0 45%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
  position: relative;
  z-index: 1;
}

.illustration-container {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 300px;
  border-radius: 1rem;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.step.active .illustration-container {
  transform: translateY(-5px);
}

.illustration-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 1rem;
  opacity: 0.1;
  transition: all 0.4s ease;
}

.step.active .illustration-bg {
  opacity: 0.15;
}

.illustration-content {
  position: relative;
  z-index: 2;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.illustration-placeholder {
  width: 100%;
  height: 100%;
  min-height: 260px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.7));
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary);
  font-size: 4rem;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.03);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(5px);
}

.step.active .illustration-placeholder {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
}

.illustration-img {
  max-width: 100%;
  height: auto;
  border-radius: 0.5rem;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.08);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(0, 0, 0, 0.03);
}

.step.active .illustration-img {
  transform: translateY(-5px);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.12);
}

.cta-container {
  max-width: 1000px;
  margin: 6rem auto 0;
  padding: 0 2rem;
}

.cta-card {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  border-radius: 1.5rem;
  padding: 3.5rem 4rem;
  color: white;
  text-align: center;
  position: relative;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(79, 70, 229, 0.25);
}

.cta-card::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 100%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
  transform: rotate(30deg);
  pointer-events: none;
}

.cta-card h3 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1rem;
  position: relative;
  z-index: 2;
}

.cta-card p {
  font-size: 1.125rem;
  opacity: 0.9;
  margin-bottom: 2rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  position: relative;
  z-index: 2;
}

.btn-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.875rem 2rem;
  font-weight: 600;
  border-radius: 0.75rem;
  transition: all 0.3s ease;
  position: relative;
  z-index: 2;
  background: white;
  color: var(--primary);
  border: none;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.btn-icon:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
  background: #f8fafc;
}

.btn-icon i {
  transition: transform 0.3s ease;
}

.btn-icon:hover i {
  transform: translateX(3px);
}

/* Responsive Styles */
@media (max-width: 1200px) {
  .step {
    margin-bottom: 6rem;
  }
  
  .step-illustration {
    flex: 0 0 50%;
  }
}

@media (max-width: 992px) {
  .section-title {
    font-size: 2.25rem;
  }
  
  .step {
    flex-direction: column !important;
    margin-bottom: 5rem;
  }
  
  .step-number-container {
    flex: 0 0 auto;
    margin-bottom: 2rem;
  }
  
  .step-connector {
    display: none;
  }
  
  .step-content-wrapper {
    padding: 0;
    margin-bottom: 2rem;
  }
  
  .step-illustration {
    flex: 0 0 100%;
    padding: 0;
  }
  
  .illustration-container {
    min-height: 250px;
  }
}

@media (max-width: 768px) {
  .section {
    padding: 4rem 0;
  }
  
  .section-title {
    font-size: 2rem;
    margin-bottom: 2rem;
  }
  
  .section-subtitle {
    font-size: 1.125rem;
  }
  
  .cta-card {
    padding: 2.5rem 2rem;
  }
  
  .cta-card h3 {
    font-size: 1.75rem;
  }
}

@media (max-width: 576px) {
  .section {
    padding: 3rem 0;
  }
  
  .section-title {
    font-size: 1.75rem;
  }
  
  .section-pre-title {
    font-size: 0.75rem;
    padding-left: 2rem;
  }
  
  .section-pre-title::before {
    width: 1.5rem;
  }
  
  .cta-card {
    padding: 2rem 1.5rem;
  }
  
  .cta-card h3 {
    font-size: 1.5rem;
  }
  
  .cta-card p {
    font-size: 1rem;
  }
  
  .btn-icon {
    width: 100%;
    padding: 0.75rem 1.5rem;
  }
}

/* Base Styles */
:root {
  --primary: #2563eb;
  --primary-dark: #1d4ed8;
  --text: #1f2937;
  --text-light: #6b7280;
  --bg-light: #f9fafb;
  --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  color: var(--text);
  line-height: 1.6;
  overflow-x: hidden;
}

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.section {
  padding: 6rem 0;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 1rem;
  color: var(--text);
}

.hero-title {
  font-size: clamp(2.5rem, 8vw, 4.5rem);
  max-width: 1000px;
  margin: 0 auto 1.5rem;
  text-align: center;
  color: white;
}

.hero-subtitle {
  font-size: clamp(1.25rem, 4vw, 1.5rem);
  opacity: 0.9;
  max-width: 700px;
  margin: 0 auto 3rem;
  text-align: center;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 400;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 3rem;
  position: relative;
  display: inline-block;
  left: 50%;
  transform: translateX(-50%);
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, var(--primary), #3b82f6);
  border-radius: 2px;
}

/* Hero Section */
.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
  color: white;
  overflow: hidden;
  padding: 2rem 1rem;
  text-align: center;
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 30%, rgba(37, 99, 235, 0.5) 0%, transparent 40%),
    radial-gradient(circle at 80% 70%, rgba(59, 130, 246, 0.5) 0%, transparent 40%);
  z-index: 1;
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 0;
}

.highlight {
  background: linear-gradient(90deg, #60a5fa, #93c5fd);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  position: relative;
  display: inline-block;
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  transition: var(--transition);
  cursor: pointer;
  border: 2px solid transparent;
  font-size: 1rem;
  text-align: center;
  margin: 0.5rem;
}

.btn-primary {
  background: var(--primary);
  color: white;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
}

.btn-primary:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
}

.btn-outline {
  background: transparent;
  color: white;
  border-color: rgba(255, 255, 255, 0.3);
}

.btn-outline:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
  border-color: white;
}

.btn-large {
  padding: 1rem 2.5rem;
  font-size: 1.1rem;
}

.cta-buttons {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  margin: 2rem 0;
}

/* Scroll Indicator */
.scroll-indicator {
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.875rem;
  z-index: 2;
  animation: bounce 2s infinite;
}

.scroll-indicator svg {
  margin-top: 0.5rem;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0) translateX(-50%);
  }
  40% {
    transform: translateY(-10px) translateX(-50%);
  }
  60% {
    transform: translateY(-5px) translateX(-50%);
  }
}

/* Value Proposition */
.value-prop {
  background-color: white;
}

.value-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}

.value-card {
  background: white;
  border-radius: 1rem;
  padding: 2.5rem 2rem;
  text-align: center;
  transition: var(--transition);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.6s ease-out forwards;
  animation-delay: var(--delay, 0s);
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.value-card:hover {
  transform: translateY(-5px) !important;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.value-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e0f2fe 0%, #dbeafe 100%);
  border-radius: 50%;
  color: var(--primary);
  font-size: 2rem;
}

.value-card h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: var(--text);
}

.value-card p {
  color: var(--text-light);
  font-size: 1rem;
  line-height: 1.6;
}

/* Industries Section */
.industries {
  background-color: var(--bg-light);
}

.industry-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}

.industry-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 2rem 1rem;
  background: white;
  border-radius: 0.75rem;
  transition: var(--transition);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.industry-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.industry-icon {
  width: 60px;
  height: 60px;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e0f2fe 0%, #dbeafe 100%);
  border-radius: 50%;
  color: var(--primary);
  font-size: 1.5rem;
}

.industry-item span {
  font-weight: 600;
  color: var(--text);
}

/* CTA Section */
.cta-section {
  padding: 6rem 2rem;
  text-align: center;
  background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
  color: white;
  position: relative;
  overflow: hidden;
}

.cta-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%233b82f6' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
  opacity: 0.5;
}

.cta-section .container {
  position: relative;
  z-index: 2;
  max-width: 800px;
  margin: 0 auto;
}

.cta-section h2 {
  font-size: 2.5rem;
  margin-bottom: 1.5rem;
  color: white;
}

.cta-section p {
  font-size: 1.25rem;
  margin-bottom: 2.5rem;
  color: rgba(255, 255, 255, 0.9);
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

/* Metrics Section */
.metrics {
  background-color: #f8fafc;
  text-align: center;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}

.metric-card {
  background: white;
  padding: 2rem 1rem;
  border-radius: 0.75rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: var(--transition);
}

.metric-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.metric-value {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--primary);
  margin-bottom: 0.5rem;
  line-height: 1.2;
}

.metric-value small {
  font-size: 1.5rem;
}

.metric-label {
  color: var(--text-light);
  font-size: 1rem;
  font-weight: 500;
}

/* Testimonials Section */
.testimonials {
  background-color: white;
}

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.testimonial-card {
  background: white;
  border-radius: 0.75rem;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: var(--transition);
  border: 1px solid #e2e8f0;
}

.testimonial-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.testimonial-content {
  position: relative;
  padding-bottom: 1.5rem;
  margin-bottom: 1.5rem;
  font-style: italic;
  color: var(--text);
  line-height: 1.7;
}

.testimonial-content::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 50px;
  height: 3px;
  background: var(--primary);
  border-radius: 3px;
}

.testimonial-author {
  display: flex;
  align-items: center;
}

.author-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #e0f2fe;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  color: var(--primary);
  font-size: 1.25rem;
}

.author-info h4 {
  font-size: 1rem;
  margin-bottom: 0.25rem;
  color: var(--text);
}

.author-info span {
  font-size: 0.875rem;
  color: var(--text-light);
}

/* Comparison Section */
.comparison {
  background-color: #f8fafc;
}

.comparison-table {
  max-width: 900px;
  margin: 0 auto;
  background: white;
  border-radius: 0.75rem;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.comparison-header, .comparison-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1.5fr;
  align-items: center;
  padding: 1rem 1.5rem;
}

.comparison-header {
  background: var(--primary);
  color: white;
  font-weight: 600;
}

.comparison-row {
  border-bottom: 1px solid #e2e8f0;
  transition: var(--transition);
}

.comparison-row:last-child {
  border-bottom: none;
}

.comparison-row:hover {
  background-color: #f8fafc;
}

.comparison-feature {
  font-weight: 500;
  color: var(--text);
}

.comparison-option {
  text-align: center;
  padding: 0.5rem;
  color: var(--text-light);
}

.comparison-option.highlight {
  background: rgba(37, 99, 235, 0.05);
  color: var(--primary);
  font-weight: 600;
  border-radius: 0.375rem;
  padding: 0.75rem 1rem;
  margin: 0.25rem;
}

.comparison-option i {
  font-size: 1.25rem;
}

.comparison-option .fa-check {
  color: #10b981;
}

.comparison-option .fa-times {
  color: #ef4444;
}

.feature-details {
  display: block;
  font-size: 0.8rem;
  font-weight: normal;
  color: var(--text-light);
  margin-top: 0.25rem;
}

/* How It Works Section */
.how-it-works {
  background-color: white;
  position: relative;
  overflow: hidden;
}

.section-subtitle {
  text-align: center;
  color: var(--text-light);
  max-width: 700px;
  margin: 0 auto 3rem;
  font-size: 1.1rem;
  line-height: 1.6;
}

.timeline {
  position: relative;
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem 0;
}

.timeline::before {
  content: '';
  position: absolute;
  width: 4px;
  background: linear-gradient(to bottom, var(--primary), #60a5fa);
  top: 0;
  bottom: 0;
  left: 50%;
  margin-left: -2px;
  border-radius: 2px;
}

.timeline-item {
  padding: 1rem 0;
  position: relative;
  width: 50%;
  box-sizing: border-box;
}

.timeline-item:nth-child(odd) {
  padding-right: 3rem;
  padding-left: 0;
  left: 0;
  text-align: right;
}

.timeline-item:nth-child(even) {
  padding-left: 3rem;
  padding-right: 0;
  left: 50%;
  text-align: left;
}

.timeline-number {
  position: absolute;
  width: 40px;
  height: 40px;
  background: var(--primary);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.2rem;
  box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3);
  z-index: 1;
}

.timeline-item:nth-child(odd) .timeline-number {
  right: -20px;
  top: 20px;
}

.timeline-item:nth-child(even) .timeline-number {
  left: -20px;
  top: 20px;
}

.timeline-content {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  position: relative;
  transition: var(--transition);
  border: 1px solid #e2e8f0;
}

.timeline-item:hover .timeline-content {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.timeline-content h3 {
  margin-top: 0;
  color: var(--text);
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}

.timeline-content p {
  margin: 0;
  color: var(--text-light);
  line-height: 1.6;
}

.timeline-icon {
  position: absolute;
  width: 50px;
  height: 50px;
  background: #e0f2fe;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary);
  font-size: 1.5rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  z-index: 1;
}

.timeline-item:nth-child(odd) .timeline-icon {
  right: -70px;
  top: 20px;
}

.timeline-item:nth-child(even) .timeline-icon {
  left: -70px;
  top: 20px;
}

/* How It Works Section */
.how-it-works {
  background-color: white;
  position: relative;
  overflow: hidden;
}

.process-steps {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 0;
}

.process-track {
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  width: 4px;
  background: linear-gradient(to bottom, var(--primary), #60a5fa);
  transform: translateX(-50%);
  z-index: 1;
  border-radius: 2px;
}

.step {
  display: flex;
  margin-bottom: 4rem;
  position: relative;
  z-index: 2;
  transition: all 0.3s ease;
  opacity: 0.7;
  transform: scale(0.95);
}

.step:nth-child(odd) {
  flex-direction: row;
  text-align: right;
  padding-right: 52%;
}

.step:nth-child(even) {
  flex-direction: row-reverse;
  text-align: left;
  padding-left: 52%;
}

.step.active {
  opacity: 1;
  transform: scale(1);
}

.step-number {
  position: absolute;
  width: 50px;
  height: 50px;
  background: white;
  border: 3px solid var(--primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  z-index: 3;
  transition: all 0.3s ease;
}

.step:nth-child(odd) .step-number {
  right: calc(48% - 25px);
}

.step:nth-child(even) .step-number {
  left: calc(48% - 25px);
}

.step-content {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  width: 100%;
  transition: all 0.3s ease;
  border: 1px solid #e5e7eb;
  position: relative;
  overflow: hidden;
}

.step:nth-child(odd) .step-content {
  margin-right: 2rem;
}

.step:nth-child(even) .step-content {
  margin-left: 2rem;
}

.step-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: var(--primary);
}

.step-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, var(--primary), #60a5fa);
  box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
}

.step h3 {
  font-size: 1.5rem;
  margin: 0 0 1rem;
  color: #1f2937;
  position: relative;
  display: inline-block;
}

.step h3::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 50px;
  height: 3px;
  background: var(--primary);
  border-radius: 3px;
}

.step p {
  color: #6b7280;
  margin-bottom: 1.5rem;
  line-height: 1.7;
}

.step-features {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px dashed #e5e7eb;
}

.step-features .feature {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
  color: #4b5563;
  font-size: 0.95rem;
}

.step-features .feature i {
  color: #10b981;
  margin-right: 0.75rem;
  font-size: 0.875rem;
}

.step-illustration {
  flex: 0 0 40%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.illustration-placeholder {
  width: 100%;
  height: 250px;
  background: #f9fafb;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary);
  font-size: 4rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  border: 1px dashed #e5e7eb;
  transition: all 0.3s ease;
}

.step.active .illustration-placeholder {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.illustration-img {
  max-width: 100%;
  height: auto;
  border-radius: 0.5rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.step.active .illustration-img {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
}

.cta-process {
  text-align: center;
  margin-top: 4rem;
  padding: 2rem;
  background: #f8fafc;
  border-radius: 1rem;
  border: 1px dashed #e5e7eb;
}

.cta-process p {
  font-size: 1.25rem;
  color: #4b5563;
  margin-bottom: 1.5rem;
}

/* Responsive Styles */
@media (max-width: 1024px) {
  .step {
    padding: 0 10% !important;
    margin-bottom: 3rem;
  }
  
  .step:nth-child(odd),
  .step:nth-child(even) {
    flex-direction: column;
    text-align: left;
    padding-right: 10% !important;
    padding-left: 10% !important;
  }
  
  .step-number {
    top: -25px;
    left: 50% !important;
    transform: translateX(-50%);
  }
  
  .step-content {
    margin: 1.5rem 0 0 0 !important;
  }
  
  .step-illustration {
    margin-top: 2rem;
  }
  
  .process-track {
    left: 3rem;
  }
}

@media (max-width: 640px) {
  .step {
    padding: 0 1rem !important;
  }
  
  .process-track {
    left: 1.5rem;
  }
  
  .step-content {
    padding: 1.5rem;
  }
  
  .step h3 {
    font-size: 1.25rem;
  }
}

/* Why Choose Us Section */
.why-us {
  background-color: #f8fafc;
  position: relative;
  overflow: hidden;
}

.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.benefits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin-bottom: 4rem;
}

.benefit-card {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  border-top: 4px solid var(--accent-color);
  position: relative;
  overflow: hidden;
}

.benefit-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--accent-color), transparent);
  opacity: 0.2;
}

.benefit-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.benefit-icon {
  width: 60px;
  height: 60px;
  background: rgba(79, 70, 229, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  color: var(--accent-color);
}

.benefit-card h3 {
  font-size: 1.25rem;
  margin-bottom: 1rem;
  color: #1f2937;
}

.benefit-card > p {
  color: #6b7280;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.benefit-features {
  border-top: 1px solid #e5e7eb;
  padding-top: 1.5rem;
}

.feature {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
  color: #4b5563;
  font-size: 0.95rem;
}

.feature i {
  color: #10b981;
  margin-right: 0.75rem;
  font-size: 0.875rem;
}

.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  background: white;
  border-radius: 1rem;
  padding: 2.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  margin-top: 3rem;
}

.stat-item {
  text-align: center;
  padding: 1rem;
  position: relative;
}

.stat-item:not(:last-child)::after {
  content: '';
  position: absolute;
  right: -1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1px;
  height: 60%;
  background: #e5e7eb;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--primary);
  margin-bottom: 0.5rem;
  line-height: 1.2;
}

.stat-value span {
  font-size: 1.5rem;
  font-weight: 600;
  margin-left: 0.25rem;
}

.stat-label {
  color: #6b7280;
  font-size: 0.95rem;
  font-weight: 500;
}

/* Responsive Adjustments */
@media (max-width: 1024px) {
  .stats-container {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
    padding: 1.5rem;
  }
  
  .stat-item:not(:last-child)::after {
    display: none;
  }
  
  .stat-item:nth-child(2n)::after {
    display: none;
  }
}

@media (max-width: 640px) {
  .stats-container {
    grid-template-columns: 1fr;
  }
  
  .stat-item:not(:last-child) {
    border-bottom: 1px solid #e5e7eb;
    padding-bottom: 1.5rem;
    margin-bottom: 1rem;
  }
  
  .stat-item:not(:last-child)::after {
    display: none;
  }
}

/* Pricing Section */
.pricing {
  background-color: #f8fafc;
  position: relative;
  overflow: hidden;
}

.pricing-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}

.pricing-card {
  background: white;
  border-radius: 0.75rem;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  position: relative;
  transition: var(--transition);
  border: 1px solid #e2e8f0;
}

.pricing-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
}

.pricing-card.popular {
  border: 2px solid var(--primary);
  transform: scale(1.05);
  z-index: 1;
}

.pricing-card.popular:hover {
  transform: scale(1.06) translateY(-5px);
}

.pricing-header {
  padding: 2rem;
  text-align: center;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.pricing-card.popular .pricing-header {
  background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
  color: white;
}

.pricing-card h3 {
  margin: 0 0 0.5rem;
  font-size: 1.5rem;
  color: var(--text);
}

.pricing-card.popular h3 {
  color: white;
}

.price {
  margin: 1.5rem 0;
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--primary);
}

.pricing-card.popular .price {
  color: white;
}

.amount {
  font-size: 3rem;
  line-height: 1;
}

.period {
  font-size: 1rem;
  font-weight: 500;
  opacity: 0.8;
}

.pricing-card .description {
  color: var(--text-light);
  margin: 1rem 0 1.5rem;
  font-size: 0.95rem;
}

.pricing-card.popular .description {
  color: rgba(255, 255, 255, 0.9);
}

.pricing-features {
  padding: 1.5rem 2rem 2rem;
}

.pricing-features h4 {
  margin: 0 0 1rem;
  color: var(--text);
  font-size: 1rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  text-align: center;
}

.pricing-features ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.pricing-features li {
  padding: 0.5rem 0;
  color: var(--text-light);
  display: flex;
  align-items: center;
}

.pricing-features i {
  color: #10b981;
  margin-right: 0.75rem;
  font-size: 0.875rem;
  width: 1.25rem;
  text-align: center;
}

.popular-badge {
  position: absolute;
  top: 1rem;
  right: -2rem;
  background: #10b981;
  color: white;
  padding: 0.25rem 2rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  transform: rotate(45deg);
  transform-origin: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .timeline::before {
    left: 2rem;
  }
  
  .timeline-item {
    width: 100%;
    padding-left: 4rem !important;
    padding-right: 1rem !important;
    text-align: left !important;
  }
  
  .timeline-item:nth-child(odd) .timeline-number,
  .timeline-item:nth-child(even) .timeline-number {
    left: 0;
    right: auto;
  }
  
  .timeline-item:nth-child(odd) .timeline-icon,
  .timeline-item:nth-child(even) .timeline-icon {
    left: -50px;
    right: auto;
  }
  
  .pricing-card.popular {
    transform: none;
  }
  
  .pricing-card.popular:hover {
    transform: translateY(-5px);
  }
}

/* Responsive Styles */
@media (max-width: 1024px) {
  .hero-title {
    font-size: 3.5rem;
  }
  
  .section {
    padding: 4rem 0;
  }
  
  .section-title {
    font-size: 2rem;
  }
}

@media (max-width: 768px) {
  .hero {
    min-height: auto;
    padding: 6rem 1rem;
  }
  
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    font-size: 1.25rem;
  }
  
  .value-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .industry-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
  
  .cta-section h2 {
    font-size: 2rem;
  }
  
  .cta-section p {
    font-size: 1.1rem;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
  }
  
  .btn {
    width: 100%;
    margin: 0.5rem 0;
  }
  
  .cta-buttons {
    flex-direction: column;
    width: 100%;
  }
  
  .industry-grid {
    grid-template-columns: 1fr;
  }
}
</style>
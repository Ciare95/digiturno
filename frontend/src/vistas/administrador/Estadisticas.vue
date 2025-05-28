<template>
  <div class="estadisticas-admin">
    <h1>Estadísticas Generales del Sistema</h1>

    <div class="filtros-globales">
      <div class="campo-filtro">
        <label for="periodo">Periodo</label>
        <select id="periodo" v-model="filtros.periodo" @change="cargarTodasLasEstadisticas">
          <option value="hoy">Hoy</option>
          <option value="semana_actual">Esta Semana</option>
          <option value="mes_actual">Este Mes</option>
          <option value="ultimo_mes">Últimos 30 días</option>
          <option value="trimestre_actual">Este Trimestre</option>
          <option value="personalizado">Personalizado</option>
        </select>
      </div>
      <div class="campo-filtro fechas-personalizadas" v-if="filtros.periodo === 'personalizado'">
        <div>
          <label for="fechaInicio">Desde</label>
          <input type="date" id="fechaInicio" v-model="filtros.fechaInicio" @change="cargarTodasLasEstadisticas" />
        </div>
        <div>
          <label for="fechaFin">Hasta</label>
          <input type="date" id="fechaFin" v-model="filtros.fechaFin" @change="cargarTodasLasEstadisticas" />
        </div>
      </div>
      <div class="campo-filtro">
        <label for="sucursal">Sucursal (Opcional)</label>
        <select id="sucursal" v-model="filtros.sucursalId" @change="cargarTodasLasEstadisticas">
          <option :value="null">Todas las Sucursales</option>
          <option v-for="sucursal in sucursales" :key="sucursal.id" :value="sucursal.id">
            {{ sucursal.nombre }}
          </option>
        </select>
      </div>
    </div>

    <div class="tarjetas-resumen-global">
      <div class="tarjeta-global">
        <div class="icono"><i class="fas fa-ticket"></i></div>
        <div class="datos">
          <div class="valor">{{ resumenGlobal.totalTurnos }}</div>
          <div class="titulo">Total de Turnos Generados</div>
        </div>
      </div>
      <div class="tarjeta-global">
        <div class="icono"><i class="fas fa-check-circle"></i></div>
        <div class="datos">
          <div class="valor">{{ resumenGlobal.turnosCompletados }}</div>
          <div class="titulo">Turnos Completados</div>
        </div>
      </div>
      <div class="tarjeta-global">
        <div class="icono"><i class="fas fa-clock"></i></div>
        <div class="datos">
          <div class="valor">{{ resumenGlobal.tiempoMedioEspera }}</div>
          <div class="titulo">Tiempo Medio de Espera</div>
        </div>
      </div>
      <div class="tarjeta-global">
        <div class="icono"><i class="fas fa-users"></i></div>
        <div class="datos">
          <div class="valor">{{ resumenGlobal.usuariosActivos }}</div>
          <div class="titulo">Usuarios Activos</div>
        </div>
      </div>
    </div>

    <div class="seccion-graficos">
      <div class="grafico-contenedor">
        <h3><i class="fas fa-chart-line"></i> Tendencia de Turnos (Día/Semana/Mes)</h3>
        <div class="grafico" ref="graficoTendenciaTurnos"></div>
        <small>Visualiza la cantidad de turnos generados a lo largo del tiempo.</small>
      </div>
      <div class="grafico-contenedor">
        <h3><i class="fas fa-pie-chart"></i> Distribución de Turnos por Servicio</h3>
        <div class="grafico" ref="graficoDistribucionServicios"></div>
        <small>Porcentaje de turnos solicitados para cada servicio.</small>
      </div>
      <div class="grafico-contenedor">
        <h3><i class="fas fa-store"></i> Rendimiento por Sucursal</h3>
        <div class="grafico" ref="graficoRendimientoSucursales"></div>
        <small>Comparativa de turnos atendidos y tiempos medios por sucursal.</small>
      </div>
      <div class="grafico-contenedor">
        <h3><i class="fas fa-hourglass-half"></i> Horas Pico de Demanda</h3>
        <div class="grafico" ref="graficoHorasPico"></div>
        <small>Identifica las horas del día con mayor afluencia de solicitudes.</small>
      </div>
    </div>

    <div class="seccion-tablas-detalle">
      <h2><i class="fas fa-list-alt"></i> Datos Detallados</h2>
      <!-- Aquí podrían ir tablas con datos más específicos, exportables, etc. -->
      <p class="placeholder-tablas">
        Próximamente: Tablas detalladas con opción de exportar datos en CSV/Excel para análisis avanzado.
      </p>
    </div>

  </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  name: 'EstadisticasAdmin',
  data() {
    return {
      filtros: {
        periodo: 'mes_actual',
        fechaInicio: new Date(new Date().setDate(1)).toISOString().split('T')[0], // Primer día del mes actual
        fechaFin: new Date().toISOString().split('T')[0], // Hoy
        sucursalId: null
      },
      sucursales: [],
      resumenGlobal: {
        totalTurnos: 0,
        turnosCompletados: 0,
        tiempoMedioEspera: '00:00',
        usuariosActivos: 0
      },
      graficosInstancias: {
        tendenciaTurnos: null,
        distribucionServicios: null,
        rendimientoSucursales: null,
        horasPico: null
      }
    };
  },
  mounted() {
    this.cargarSucursales();
    this.cargarTodasLasEstadisticas();
  },
  methods: {
    cargarSucursales() {
      // Simulación de carga de sucursales
      setTimeout(() => {
        this.sucursales = [
          { id: 1, nombre: 'Sucursal Central' },
          { id: 2, nombre: 'Sucursal Norte' },
          { id: 3, nombre: 'Sucursal Sur Corporativa' }
        ];
      }, 300);
    },
    cargarTodasLasEstadisticas() {
      console.log('Cargando estadísticas con filtros:', this.filtros);
      // Simulación de carga de datos de resumen global
      setTimeout(() => {
        this.resumenGlobal = {
          totalTurnos: Math.floor(Math.random() * 5000) + 1000,
          turnosCompletados: Math.floor(Math.random() * 4000) + 800,
          tiempoMedioEspera: `${Math.floor(Math.random() * 15) + 5}:${Math.floor(Math.random() * 60).toString().padStart(2, '0')}`,
          usuariosActivos: Math.floor(Math.random() * 500) + 100
        };
        
        this.$nextTick(() => {
          this.renderizarGraficos();
        });
      }, 600);
    },
    renderizarGraficos() {
      console.log('Renderizando gráficos. Asegúrate de tener Chart.js instalado y configurado.');
      // Destruir gráficos anteriores para evitar duplicados o errores
      Object.values(this.graficosInstancias).forEach(chart => chart?.destroy());

      // Datos de ejemplo para los gráficos
      const etiquetasDias = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'];
      const datosTurnosDia = etiquetasDias.map(() => Math.floor(Math.random() * 200) + 50);
      
      const etiquetasServicios = ['Atención Cliente', 'Pagos', 'Reclamos', 'Info General', 'Soporte VIP'];
      const datosDistribucion = etiquetasServicios.map(() => Math.floor(Math.random() * 100) + 20);

      const etiquetasSucursales = this.sucursales.length > 0 ? this.sucursales.map(s => s.nombre) : ['Suc. A', 'Suc. B', 'Suc. C'];
      const datosTurnosSucursal = etiquetasSucursales.map(() => Math.floor(Math.random() * 1000) + 200);
      const datosTiempoSucursal = etiquetasSucursales.map(() => Math.floor(Math.random() * 15) + 5);

      const etiquetasHoras = Array.from({ length: 12 }, (_, i) => `${i + 8}:00`); // 8 AM a 7 PM
      const datosHorasPico = etiquetasHoras.map(() => Math.floor(Math.random() * 150) + 30);

      // Gráfico de Tendencia de Turnos
      if (this.$refs.graficoTendenciaTurnos) {
        const ctxTendencia = this.$refs.graficoTendenciaTurnos.getContext('2d');
        
        this.graficosInstancias.tendenciaTurnos = new Chart(ctxTendencia, {
          type: 'line',
          data: { labels: etiquetasDias, datasets: [{ label: 'Turnos Generados', data: datosTurnosDia, borderColor: '#007bff', tension: 0.1 }] },
          options: { responsive: true, maintainAspectRatio: false }
        });
      }

      // Gráfico de Distribución por Servicio
      if (this.$refs.graficoDistribucionServicios) {
        const ctxDistribucion = this.$refs.graficoDistribucionServicios.getContext('2d');
        
        this.graficosInstancias.distribucionServicios = new Chart(ctxDistribucion, {
          type: 'doughnut',
          data: { labels: etiquetasServicios, datasets: [{ label: 'Distribución', data: datosDistribucion, backgroundColor: ['#007bff', '#28a745', '#ffc107', '#dc3545', '#17a2b8'] }] },
          options: { responsive: true, maintainAspectRatio: false }
        });
      }

      // Gráfico de Rendimiento por Sucursal
      if (this.$refs.graficoRendimientoSucursales) {
        const ctxRendimiento = this.$refs.graficoRendimientoSucursales.getContext('2d');
        
        this.graficosInstancias.rendimientoSucursales = new Chart(ctxRendimiento, {
          type: 'bar',
          data: {
            labels: etiquetasSucursales,
            datasets: [
              { label: 'Turnos Atendidos', data: datosTurnosSucursal, backgroundColor: '#28a745', yAxisID: 'yTurnos' },
              { label: 'Tiempo Medio (min)', data: datosTiempoSucursal, backgroundColor: '#ffc107', yAxisID: 'yTiempo' }
            ]
          },
          options: {
            responsive: true, maintainAspectRatio: false,
            scales: {
              yTurnos: { type: 'linear', display: true, position: 'left', title: { display: true, text: 'Nº Turnos'} },
              yTiempo: { type: 'linear', display: true, position: 'right', title: { display: true, text: 'Minutos'}, grid: { drawOnChartArea: false } }
            }
          }
        });
      }

      // Gráfico de Horas Pico
      if (this.$refs.graficoHorasPico) {
        const ctxHorasPico = this.$refs.graficoHorasPico.getContext('2d');
        
        this.graficosInstancias.horasPico = new Chart(ctxHorasPico, {
          type: 'bar',
          data: { labels: etiquetasHoras, datasets: [{ label: 'Promedio de Turnos', data: datosHorasPico, backgroundColor: '#17a2b8' }] },
          options: { responsive: true, maintainAspectRatio: false }
        });
      }
    }
  },
  beforeUnmount() {
    // Destruir instancias de Chart.js al desmontar el componente para liberar recursos
    Object.values(this.graficosInstancias).forEach(chart => chart?.destroy());
  }
};
</script>

<style scoped>
.estadisticas-admin {
  padding: 2rem;
  background-color: #f4f6f9;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 2rem;
  font-size: 1.8rem;
}

.filtros-globales {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
  padding: 1.5rem;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}

.campo-filtro {
  flex: 1;
  min-width: 220px;
}

.campo-filtro label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #555;
}

.campo-filtro select,
.campo-filtro input[type="date"] {
  width: 100%;
  padding: 0.7rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9rem;
}

.fechas-personalizadas {
  display: flex;
  gap: 1rem;
}
.fechas-personalizadas > div {
  flex: 1;
}

.tarjetas-resumen-global {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

.tarjeta-global {
  background-color: #fff;
  border-radius: 8px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
  transition: transform 0.2s, box-shadow 0.2s;
}

.tarjeta-global:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.tarjeta-global .icono {
  font-size: 2.5rem;
  color: #007bff;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #e7f3ff;
  border-radius: 50%;
}

.tarjeta-global .datos .valor {
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
}

.tarjeta-global .datos .titulo {
  font-size: 0.9rem;
  color: #666;
}

.seccion-graficos {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
  margin-bottom: 2.5rem;
}

.grafico-contenedor {
  background-color: #fff;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}

.grafico-contenedor h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  font-size: 1.1rem;
  color: #333;
}

.grafico-contenedor h3 i {
  margin-right: 0.5rem;
  color: #007bff;
}

.grafico-contenedor small {
  display: block;
  margin-top: 0.8rem;
  font-size: 0.85rem;
  color: #777;
  text-align: center;
}

.grafico {
  height: 300px; /* Altura fija para los gráficos */
  width: 100%;
  background-color: #f0f0f0; /* Placeholder si Chart.js no carga */
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  border-radius: 4px;
}

.seccion-tablas-detalle {
  background-color: #fff;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}

.seccion-tablas-detalle h2 {
  margin-top: 0;
  margin-bottom: 1rem;
  font-size: 1.3rem;
}

.seccion-tablas-detalle h2 i {
  margin-right: 0.5rem;
  color: #007bff;
}

.placeholder-tablas {
  color: #777;
  text-align: center;
  padding: 2rem;
  border: 2px dashed #ddd;
  border-radius: 4px;
}

@media (max-width: 768px) {
  .filtros-globales,
  .tarjetas-resumen-global,
  .seccion-graficos {
    grid-template-columns: 1fr;
  }
  .fechas-personalizadas {
    flex-direction: column;
  }
}
</style>

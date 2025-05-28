<template>
  <div class="estadisticas-empleado">
    <h1>Estadísticas de Atención</h1>
    
    <div class="filtros">
      <div class="campo-filtro">
        <label for="periodo">Periodo</label>
        <select id="periodo" v-model="filtros.periodo" @change="cargarEstadisticas">
          <option value="hoy">Hoy</option>
          <option value="semana">Esta semana</option>
          <option value="mes">Este mes</option>
          <option value="personalizado">Personalizado</option>
        </select>
      </div>
      
      <div class="campo-filtro fecha" v-if="filtros.periodo === 'personalizado'">
        <div>
          <label for="fechaInicio">Desde</label>
          <input type="date" id="fechaInicio" v-model="filtros.fechaInicio" @change="cargarEstadisticas" />
        </div>
        <div>
          <label for="fechaFin">Hasta</label>
          <input type="date" id="fechaFin" v-model="filtros.fechaFin" @change="cargarEstadisticas" />
        </div>
      </div>
      
      <div class="campo-filtro">
        <label for="servicio">Servicio</label>
        <select id="servicio" v-model="filtros.servicio" @change="cargarEstadisticas">
          <option value="">Todos</option>
          <option v-for="servicio in servicios" :key="servicio.id" :value="servicio.id">
            {{ servicio.nombre }}
          </option>
        </select>
      </div>
    </div>
    
    <div class="tarjetas-resumen">
      <div class="tarjeta">
        <div class="tarjeta-titulo">Turnos Atendidos</div>
        <div class="tarjeta-valor">{{ resumen.turnosAtendidos }}</div>
      </div>
      <div class="tarjeta">
        <div class="tarjeta-titulo">Tiempo Promedio</div>
        <div class="tarjeta-valor">{{ resumen.tiempoPromedio }}</div>
      </div>
      <div class="tarjeta">
        <div class="tarjeta-titulo">Satisfacción</div>
        <div class="tarjeta-valor">{{ resumen.satisfaccion }}%</div>
      </div>
      <div class="tarjeta">
        <div class="tarjeta-titulo">Eficiencia</div>
        <div class="tarjeta-valor">{{ resumen.eficiencia }}%</div>
      </div>
    </div>
    
    <div class="graficos">
      <div class="grafico-contenedor">
        <h2>Turnos por Día</h2>
        <div class="grafico" ref="graficoTurnos"></div>
      </div>
      
      <div class="grafico-contenedor">
        <h2>Tiempo Promedio por Servicio</h2>
        <div class="grafico" ref="graficoTiempos"></div>
      </div>
    </div>
    
    <div class="tabla-contenedor">
      <h2>Detalle de Turnos</h2>
      <table v-if="turnos.length > 0" class="tabla-turnos">
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Número</th>
            <th>Cliente</th>
            <th>Servicio</th>
            <th>Tiempo de Atención</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="turno in turnos" :key="turno.id">
            <td>{{ formatearFecha(turno.fecha) }}</td>
            <td><strong>{{ turno.numero }}</strong></td>
            <td>{{ turno.cliente.nombre }} {{ turno.cliente.apellido }}</td>
            <td>{{ turno.servicio.nombre }}</td>
            <td>{{ turno.tiempoAtencion }}</td>
            <td>
              <span class="estado" :class="'estado-' + turno.estado">
                {{ traducirEstado(turno.estado) }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="mensaje-vacio">
        No hay datos para mostrar con los filtros seleccionados.
      </div>
    </div>
  </div>
</template>

<script>
// Importar biblioteca de gráficos (se debe instalar)
// import Chart from 'chart.js/auto';

export default {
  name: 'EstadisticasEmpleado',
  data() {
    return {
      filtros: {
        periodo: 'hoy',
        fechaInicio: new Date().toISOString().split('T')[0],
        fechaFin: new Date().toISOString().split('T')[0],
        servicio: ''
      },
      servicios: [],
      resumen: {
        turnosAtendidos: 0,
        tiempoPromedio: '00:00',
        satisfaccion: 0,
        eficiencia: 0
      },
      turnos: [],
      graficos: {
        turnos: null,
        tiempos: null
      }
    };
  },
  mounted() {
    this.cargarServicios();
    this.cargarEstadisticas();
  },
  methods: {
    // Cargar servicios disponibles
    cargarServicios() {
      // Simulación de carga de servicios
      setTimeout(() => {
        this.servicios = [
          { id: 1, nombre: 'Atención al Cliente' },
          { id: 2, nombre: 'Pagos' },
          { id: 3, nombre: 'Reclamos' },
          { id: 4, nombre: 'Información' }
        ];
      }, 300);
    },
    
    // Cargar estadísticas según filtros
    cargarEstadisticas() {
      // Aquí se implementaría la lógica para cargar las estadísticas
      // desde el servidor según los filtros aplicados
      
      // Simulación de carga de datos de resumen
      setTimeout(() => {
        this.resumen = {
          turnosAtendidos: 45,
          tiempoPromedio: '08:23',
          satisfaccion: 92,
          eficiencia: 87
        };
        
        // Simulación de carga de turnos
        this.turnos = [
          {
            id: 1,
            fecha: new Date(2023, 4, 15, 9, 30),
            numero: 'A001',
            cliente: { nombre: 'Juan', apellido: 'Pérez' },
            servicio: { id: 1, nombre: 'Atención al Cliente' },
            tiempoAtencion: '07:45',
            estado: 'completado'
          },
          {
            id: 2,
            fecha: new Date(2023, 4, 15, 10, 0),
            numero: 'A002',
            cliente: { nombre: 'María', apellido: 'González' },
            servicio: { id: 2, nombre: 'Pagos' },
            tiempoAtencion: '05:20',
            estado: 'completado'
          },
          {
            id: 3,
            fecha: new Date(2023, 4, 15, 10, 15),
            numero: 'A003',
            cliente: { nombre: 'Carlos', apellido: 'Rodríguez' },
            servicio: { id: 1, nombre: 'Atención al Cliente' },
            tiempoAtencion: '12:10',
            estado: 'completado'
          },
          {
            id: 4,
            fecha: new Date(2023, 4, 15, 10, 30),
            numero: 'A004',
            cliente: { nombre: 'Ana', apellido: 'Martínez' },
            servicio: { id: 3, nombre: 'Reclamos' },
            tiempoAtencion: '15:35',
            estado: 'completado'
          },
          {
            id: 5,
            fecha: new Date(2023, 4, 15, 11, 0),
            numero: 'A005',
            cliente: { nombre: 'Pedro', apellido: 'López' },
            servicio: { id: 4, nombre: 'Información' },
            tiempoAtencion: '03:15',
            estado: 'completado'
          }
        ];
        
        // Renderizar gráficos después de cargar datos
        this.$nextTick(() => {
          this.renderizarGraficos();
        });
      }, 500);
    },
    
    // Renderizar gráficos con los datos cargados
    renderizarGraficos() {
      // Comentado porque requiere la instalación de Chart.js
      // Si Chart.js está instalado, descomentar este código
      
      /*
      // Destruir gráficos anteriores si existen
      if (this.graficos.turnos) {
        this.graficos.turnos.destroy();
      }
      if (this.graficos.tiempos) {
        this.graficos.tiempos.destroy();
      }
      
      // Gráfico de turnos por día
      const ctxTurnos = this.$refs.graficoTurnos.getContext('2d');
      this.graficos.turnos = new Chart(ctxTurnos, {
        type: 'bar',
        data: {
          labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
          datasets: [{
            label: 'Turnos Atendidos',
            data: [12, 19, 15, 8, 22, 14, 0],
            backgroundColor: 'rgba(74, 144, 226, 0.7)',
            borderColor: 'rgba(74, 144, 226, 1)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
      
      // Gráfico de tiempo promedio por servicio
      const ctxTiempos = this.$refs.graficoTiempos.getContext('2d');
      this.graficos.tiempos = new Chart(ctxTiempos, {
        type: 'horizontalBar',
        data: {
          labels: this.servicios.map(s => s.nombre),
          datasets: [{
            label: 'Minutos',
            data: [8.5, 5.2, 15.3, 3.8],
            backgroundColor: 'rgba(40, 167, 69, 0.7)',
            borderColor: 'rgba(40, 167, 69, 1)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              beginAtZero: true
            }
          }
        }
      });
      */
      
      // Mensaje para indicar que se necesita instalar Chart.js
      console.log('Para visualizar los gráficos, instale Chart.js con: npm install chart.js');
    },
    
    // Formatear fecha para mostrar en la tabla
    formatearFecha(fecha) {
      return new Date(fecha).toLocaleDateString('es-ES');
    },
    
    // Traducir estado del turno
    traducirEstado(estado) {
      const traducciones = {
        'pendiente': 'Pendiente',
        'en_proceso': 'En Proceso',
        'completado': 'Completado',
        'cancelado': 'Cancelado'
      };
      return traducciones[estado] || estado;
    }
  }
};
</script>

<style scoped>
.estadisticas-empleado {
  padding: 2rem;
}

h1 {
  margin-bottom: 2rem;
  color: #333;
}

h2 {
  margin-bottom: 1rem;
  color: #555;
  font-size: 1.2rem;
}

.filtros {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
  background-color: #f5f5f5;
  padding: 1rem;
  border-radius: 8px;
}

.campo-filtro {
  flex: 1;
  min-width: 200px;
}

.campo-filtro.fecha {
  display: flex;
  gap: 1rem;
}

.campo-filtro.fecha > div {
  flex: 1;
}

.campo-filtro label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.campo-filtro input,
.campo-filtro select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.tarjetas-resumen {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.tarjeta {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  text-align: center;
}

.tarjeta-titulo {
  font-size: 1rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.tarjeta-valor {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
}

.graficos {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.grafico-contenedor {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

.grafico {
  height: 300px;
  background-color: #f9f9f9;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
}

.tabla-contenedor {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  margin-bottom: 2rem;
  overflow-x: auto;
}

.tabla-turnos {
  width: 100%;
  border-collapse: collapse;
}

.tabla-turnos th,
.tabla-turnos td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.tabla-turnos th {
  background-color: #f8f9fa;
  font-weight: 600;
}

.estado {
  display: inline-block;
  padding: 0.3rem 0.6rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.estado-completado {
  background-color: #d4edda;
  color: #155724;
}

.estado-cancelado {
  background-color: #f8d7da;
  color: #721c24;
}

.mensaje-vacio {
  padding: 2rem;
  text-align: center;
  color: #6c757d;
}

@media (max-width: 768px) {
  .filtros {
    flex-direction: column;
  }
  
  .graficos {
    grid-template-columns: 1fr;
  }
}
</style>

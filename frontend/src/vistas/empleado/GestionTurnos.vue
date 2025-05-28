<template>
  <div class="gestion-turnos">
    <h1>Gestión de Turnos</h1>
    
    <div class="filtros">
      <div class="campo-filtro">
        <label for="fecha">Fecha</label>
        <input type="date" id="fecha" v-model="filtros.fecha" @change="cargarTurnos" />
      </div>
      <div class="campo-filtro">
        <label for="estado">Estado</label>
        <select id="estado" v-model="filtros.estado" @change="cargarTurnos">
          <option value="">Todos</option>
          <option value="pendiente">Pendiente</option>
          <option value="en_proceso">En Proceso</option>
          <option value="completado">Completado</option>
          <option value="cancelado">Cancelado</option>
        </select>
      </div>
      <div class="campo-filtro">
        <label for="servicio">Servicio</label>
        <select id="servicio" v-model="filtros.servicio" @change="cargarTurnos">
          <option value="">Todos</option>
          <option v-for="servicio in servicios" :key="servicio.id" :value="servicio.id">
            {{ servicio.nombre }}
          </option>
        </select>
      </div>
    </div>
    
    <div class="tabla-contenedor">
      <table v-if="turnos.length > 0" class="tabla-turnos">
        <thead>
          <tr>
            <th>Número</th>
            <th>Cliente</th>
            <th>Servicio</th>
            <th>Hora</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="turno in turnos" :key="turno.id" :class="{ 'turno-actual': turno.esActual }">
            <td><strong>{{ turno.numero }}</strong></td>
            <td>{{ turno.cliente.nombre }} {{ turno.cliente.apellido }}</td>
            <td>{{ turno.servicio.nombre }}</td>
            <td>{{ formatearHora(turno.hora) }}</td>
            <td>
              <span class="estado" :class="'estado-' + turno.estado">
                {{ traducirEstado(turno.estado) }}
              </span>
            </td>
            <td class="acciones">
              <button 
                v-if="turno.estado === 'pendiente'" 
                @click="llamarTurno(turno)" 
                class="boton boton-llamar"
              >
                Llamar
              </button>
              <button 
                v-if="turno.estado === 'en_proceso'" 
                @click="completarTurno(turno)" 
                class="boton boton-completar"
              >
                Completar
              </button>
              <button 
                v-if="['pendiente', 'en_proceso'].includes(turno.estado)" 
                @click="cancelarTurno(turno)" 
                class="boton boton-cancelar"
              >
                Cancelar
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="mensaje-vacio">
        No hay turnos para mostrar con los filtros seleccionados.
      </div>
    </div>
    
    <div class="panel-actual" v-if="turnoActual">
      <h2>Turno Actual</h2>
      <div class="info-turno-actual">
        <div class="numero-turno">{{ turnoActual.numero }}</div>
        <div class="detalles-turno">
          <p><strong>Cliente:</strong> {{ turnoActual.cliente.nombre }} {{ turnoActual.cliente.apellido }}</p>
          <p><strong>Servicio:</strong> {{ turnoActual.servicio.nombre }}</p>
          <p><strong>Tiempo transcurrido:</strong> {{ tiempoTranscurrido }}</p>
        </div>
        <div class="botones-accion">
          <button @click="completarTurno(turnoActual)" class="boton boton-completar">Completar</button>
          <button @click="cancelarTurno(turnoActual)" class="boton boton-cancelar">Cancelar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GestionTurnos',
  data() {
    return {
      turnos: [],
      turnoActual: null,
      tiempoTranscurrido: '00:00',
      cronometro: null,
      filtros: {
        fecha: new Date().toISOString().split('T')[0],
        estado: '',
        servicio: ''
      },
      servicios: []
    };
  },
  mounted() {
    this.cargarServicios();
    this.cargarTurnos();
  },
  beforeUnmount() {
    this.detenerCronometro();
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
    
    // Cargar turnos según filtros
    cargarTurnos() {
      // Aquí se implementaría la lógica para cargar los turnos
      // desde el servidor según los filtros aplicados
      
      // Simulación de carga de turnos
      setTimeout(() => {
        this.turnos = [
          {
            id: 1,
            numero: 'A001',
            cliente: { nombre: 'Juan', apellido: 'Pérez' },
            servicio: { id: 1, nombre: 'Atención al Cliente' },
            hora: new Date().setHours(9, 30),
            estado: 'pendiente',
            esActual: false
          },
          {
            id: 2,
            numero: 'A002',
            cliente: { nombre: 'María', apellido: 'González' },
            servicio: { id: 2, nombre: 'Pagos' },
            hora: new Date().setHours(10, 0),
            estado: 'en_proceso',
            esActual: true
          },
          {
            id: 3,
            numero: 'A003',
            cliente: { nombre: 'Carlos', apellido: 'Rodríguez' },
            servicio: { id: 1, nombre: 'Atención al Cliente' },
            hora: new Date().setHours(10, 15),
            estado: 'pendiente',
            esActual: false
          },
          {
            id: 4,
            numero: 'A004',
            cliente: { nombre: 'Ana', apellido: 'Martínez' },
            servicio: { id: 3, nombre: 'Reclamos' },
            hora: new Date().setHours(10, 30),
            estado: 'pendiente',
            esActual: false
          }
        ];
        
        // Establecer turno actual si existe alguno en proceso
        this.turnoActual = this.turnos.find(t => t.estado === 'en_proceso');
        
        if (this.turnoActual) {
          this.iniciarCronometro();
        }
      }, 500);
    },
    
    // Formatear hora para mostrar en la tabla
    formatearHora(timestamp) {
      const fecha = new Date(timestamp);
      return fecha.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
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
    },
    
    // Llamar al siguiente turno
    llamarTurno(turno) {
      // Detener cronómetro anterior si existe
      this.detenerCronometro();
      
      // Actualizar estado del turno
      turno.estado = 'en_proceso';
      turno.esActual = true;
      
      // Si había un turno actual, ya no lo es
      if (this.turnoActual) {
        this.turnoActual.esActual = false;
      }
      
      // Establecer nuevo turno actual
      this.turnoActual = turno;
      
      // Iniciar cronómetro
      this.iniciarCronometro();
      
      // Aquí se implementaría la lógica para llamar al turno en el sistema
      // y actualizar en el servidor
      
      // Notificar al usuario
      this.$toast.success(`Turno ${turno.numero} llamado correctamente`);
    },
    
    // Completar un turno
    completarTurno(turno) {
      // Actualizar estado del turno
      turno.estado = 'completado';
      turno.esActual = false;
      
      // Si era el turno actual, detener cronómetro
      if (this.turnoActual && this.turnoActual.id === turno.id) {
        this.detenerCronometro();
        this.turnoActual = null;
      }
      
      // Aquí se implementaría la lógica para completar el turno en el servidor
      
      // Notificar al usuario
      this.$toast.success(`Turno ${turno.numero} completado correctamente`);
    },
    
    // Cancelar un turno
    cancelarTurno(turno) {
      // Confirmar cancelación
      if (!confirm(`¿Está seguro de cancelar el turno ${turno.numero}?`)) {
        return;
      }
      
      // Actualizar estado del turno
      turno.estado = 'cancelado';
      turno.esActual = false;
      
      // Si era el turno actual, detener cronómetro
      if (this.turnoActual && this.turnoActual.id === turno.id) {
        this.detenerCronometro();
        this.turnoActual = null;
      }
      
      // Aquí se implementaría la lógica para cancelar el turno en el servidor
      
      // Notificar al usuario
      this.$toast.info(`Turno ${turno.numero} cancelado`);
    },
    
    // Iniciar cronómetro para el turno actual
    iniciarCronometro() {
      let segundos = 0;
      
      this.cronometro = setInterval(() => {
        segundos++;
        const minutos = Math.floor(segundos / 60);
        const segsRestantes = segundos % 60;
        
        this.tiempoTranscurrido = 
          `${minutos.toString().padStart(2, '0')}:${segsRestantes.toString().padStart(2, '0')}`;
      }, 1000);
    },
    
    // Detener cronómetro
    detenerCronometro() {
      if (this.cronometro) {
        clearInterval(this.cronometro);
        this.cronometro = null;
      }
    }
  }
};
</script>

<style scoped>
.gestion-turnos {
  padding: 2rem;
}

h1 {
  margin-bottom: 2rem;
  color: #333;
}

.filtros {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  background-color: #f5f5f5;
  padding: 1rem;
  border-radius: 8px;
}

.campo-filtro {
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

.tabla-contenedor {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
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

.turno-actual {
  background-color: #e8f4fd;
}

.estado {
  display: inline-block;
  padding: 0.3rem 0.6rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.estado-pendiente {
  background-color: #fff3cd;
  color: #856404;
}

.estado-en_proceso {
  background-color: #d1ecf1;
  color: #0c5460;
}

.estado-completado {
  background-color: #d4edda;
  color: #155724;
}

.estado-cancelado {
  background-color: #f8d7da;
  color: #721c24;
}

.acciones {
  display: flex;
  gap: 0.5rem;
}

.boton {
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.boton-llamar {
  background-color: #4a90e2;
  color: white;
}

.boton-llamar:hover {
  background-color: #3a7bc8;
}

.boton-completar {
  background-color: #28a745;
  color: white;
}

.boton-completar:hover {
  background-color: #218838;
}

.boton-cancelar {
  background-color: #dc3545;
  color: white;
}

.boton-cancelar:hover {
  background-color: #c82333;
}

.mensaje-vacio {
  padding: 2rem;
  text-align: center;
  color: #6c757d;
}

.panel-actual {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

.panel-actual h2 {
  margin-bottom: 1rem;
  color: #333;
}

.info-turno-actual {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.numero-turno {
  font-size: 3rem;
  font-weight: bold;
  color: #4a90e2;
  background-color: #e8f4fd;
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.detalles-turno {
  flex: 1;
}

.detalles-turno p {
  margin: 0.5rem 0;
}

.botones-accion {
  display: flex;
  gap: 1rem;
}

@media (max-width: 768px) {
  .filtros {
    flex-direction: column;
  }
  
  .info-turno-actual {
    flex-direction: column;
    gap: 1rem;
  }
  
  .botones-accion {
    margin-top: 1rem;
  }
}
</style>

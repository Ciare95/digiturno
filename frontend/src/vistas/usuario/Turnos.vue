<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6">Mis Turnos</h1>
    
    <!-- Sección para solicitar nuevo turno -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 class="text-xl font-semibold mb-4">Solicitar Nuevo Turno</h2>
      <form @submit.prevent="solicitarTurno">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Sucursal</label>
            <select 
              v-model="nuevoTurno.sucursalId" 
              class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            >
              <option value="" disabled>Selecciona una sucursal</option>
              <option v-for="sucursal in sucursales" :key="sucursal.id" :value="sucursal.id">
                {{ sucursal.nombre }}
              </option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Servicio</label>
            <select 
              v-model="nuevoTurno.servicioId" 
              class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            >
              <option value="" disabled>Selecciona un servicio</option>
              <option v-for="servicio in servicios" :key="servicio.id" :value="servicio.id">
                {{ servicio.nombre }}
              </option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Fecha</label>
            <input 
              type="date" 
              v-model="nuevoTurno.fecha" 
              class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            >
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Hora</label>
            <select 
              v-model="nuevoTurno.hora" 
              class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            >
              <option value="" disabled>Selecciona una hora</option>
              <option v-for="hora in horasDisponibles" :key="hora" :value="hora">
                {{ hora }}
              </option>
            </select>
          </div>
        </div>
        
        <div class="mt-6">
          <button 
            type="submit" 
            class="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            :disabled="cargando"
          >
            <span v-if="cargando">Procesando...</span>
            <span v-else>Solicitar Turno</span>
          </button>
        </div>
      </form>
    </div>
    
    <!-- Lista de turnos activos -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 class="text-xl font-semibold mb-4">Turnos Activos</h2>
      
      <div v-if="cargando" class="flex justify-center py-8">
        <div class="spinner"></div>
      </div>
      
      <div v-else-if="turnosActivos.length === 0" class="py-8 text-center text-gray-500">
        No tienes turnos activos en este momento.
      </div>
      
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead>
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Código</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Sucursal</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Servicio</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha y Hora</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="turno in turnosActivos" :key="turno.id">
              <td class="px-6 py-4 whitespace-nowrap font-medium">{{ turno.codigo }}</td>
              <td class="px-6 py-4 whitespace-nowrap">{{ turno.sucursal }}</td>
              <td class="px-6 py-4 whitespace-nowrap">{{ turno.servicio }}</td>
              <td class="px-6 py-4 whitespace-nowrap">{{ formatearFechaHora(turno.fechaHora) }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span 
                  :class="{
                    'px-2 py-1 text-xs font-semibold rounded-full': true,
                    'bg-yellow-100 text-yellow-800': turno.estado === 'pendiente',
                    'bg-blue-100 text-blue-800': turno.estado === 'en_espera',
                    'bg-green-100 text-green-800': turno.estado === 'en_atencion'
                  }"
                >
                  {{ traducirEstado(turno.estado) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <button 
                  @click="cancelarTurno(turno.id)" 
                  class="text-red-600 hover:text-red-900 mr-4"
                >
                  Cancelar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- Historial de turnos -->
    <div class="bg-white rounded-lg shadow-md p-6">
      <h2 class="text-xl font-semibold mb-4">Historial de Turnos</h2>
      
      <div v-if="cargando" class="flex justify-center py-8">
        <div class="spinner"></div>
      </div>
      
      <div v-else-if="historialTurnos.length === 0" class="py-8 text-center text-gray-500">
        No tienes turnos en tu historial.
      </div>
      
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead>
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Código</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Sucursal</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Servicio</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha y Hora</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="turno in historialTurnos" :key="turno.id">
              <td class="px-6 py-4 whitespace-nowrap font-medium">{{ turno.codigo }}</td>
              <td class="px-6 py-4 whitespace-nowrap">{{ turno.sucursal }}</td>
              <td class="px-6 py-4 whitespace-nowrap">{{ turno.servicio }}</td>
              <td class="px-6 py-4 whitespace-nowrap">{{ formatearFechaHora(turno.fechaHora) }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span 
                  :class="{
                    'px-2 py-1 text-xs font-semibold rounded-full': true,
                    'bg-gray-100 text-gray-800': turno.estado === 'cancelado',
                    'bg-green-100 text-green-800': turno.estado === 'completado'
                  }"
                >
                  {{ traducirEstado(turno.estado) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TurnosUsuario',
  data() {
    return {
      // Datos para el formulario de nuevo turno
      nuevoTurno: {
        sucursalId: '',
        servicioId: '',
        fecha: '',
        hora: ''
      },
      // Datos para las listas desplegables
      sucursales: [],
      servicios: [],
      horasDisponibles: [
        '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
        '12:00', '12:30', '13:00', '13:30', '14:00', '14:30',
        '15:00', '15:30', '16:00', '16:30', '17:00', '17:30'
      ],
      // Datos de turnos
      turnosActivos: [],
      historialTurnos: [],
      // Estado de la interfaz
      cargando: false,
      error: null
    }
  },
  created() {
    this.cargarDatos()
  },
  methods: {
    /**
     * Carga los datos iniciales necesarios para la vista
     */
    async cargarDatos() {
      this.cargando = true
      try {
        // Aquí se cargarían los datos desde la API
        // Por ahora usamos datos de ejemplo
        await this.cargarSucursales()
        await this.cargarServicios()
        await this.cargarTurnos()
      } catch (error) {
        this.error = 'Error al cargar los datos: ' + error.message
        console.error('Error al cargar datos:', error)
      } finally {
        this.cargando = false
      }
    },
    
    /**
     * Carga la lista de sucursales disponibles
     */
    async cargarSucursales() {
      // Simulación de carga desde API
      this.sucursales = [
        { id: 1, nombre: 'Sucursal Centro' },
        { id: 2, nombre: 'Sucursal Norte' },
        { id: 3, nombre: 'Sucursal Sur' }
      ]
    },
    
    /**
     * Carga la lista de servicios disponibles
     */
    async cargarServicios() {
      // Simulación de carga desde API
      this.servicios = [
        { id: 1, nombre: 'Atención al Cliente' },
        { id: 2, nombre: 'Pagos' },
        { id: 3, nombre: 'Reclamos' },
        { id: 4, nombre: 'Información' }
      ]
    },
    
    /**
     * Carga los turnos del usuario (activos e historial)
     */
    async cargarTurnos() {
      // Simulación de carga desde API
      this.turnosActivos = [
        {
          id: 101,
          codigo: 'A123',
          sucursal: 'Sucursal Centro',
          servicio: 'Atención al Cliente',
          fechaHora: '2025-05-28T10:30:00',
          estado: 'pendiente'
        },
        {
          id: 102,
          codigo: 'B456',
          sucursal: 'Sucursal Norte',
          servicio: 'Pagos',
          fechaHora: '2025-05-29T11:00:00',
          estado: 'en_espera'
        }
      ]
      
      this.historialTurnos = [
        {
          id: 95,
          codigo: 'C789',
          sucursal: 'Sucursal Sur',
          servicio: 'Reclamos',
          fechaHora: '2025-05-20T14:30:00',
          estado: 'completado'
        },
        {
          id: 82,
          codigo: 'D012',
          sucursal: 'Sucursal Centro',
          servicio: 'Información',
          fechaHora: '2025-05-15T09:00:00',
          estado: 'cancelado'
        }
      ]
    },
    
    /**
     * Solicita un nuevo turno
     */
    async solicitarTurno() {
      this.cargando = true
      try {
        // Aquí se enviaría la solicitud a la API
        console.log('Solicitando turno:', this.nuevoTurno)
        
        // Simulamos una respuesta exitosa
        setTimeout(() => {
          // Agregamos el nuevo turno a la lista de activos
          const nuevoTurnoCreado = {
            id: 103,
            codigo: 'E345',
            sucursal: this.sucursales.find(s => s.id === this.nuevoTurno.sucursalId)?.nombre,
            servicio: this.servicios.find(s => s.id === this.nuevoTurno.servicioId)?.nombre,
            fechaHora: `${this.nuevoTurno.fecha}T${this.nuevoTurno.hora}:00`,
            estado: 'pendiente'
          }
          
          this.turnosActivos.unshift(nuevoTurnoCreado)
          
          // Limpiamos el formulario
          this.nuevoTurno = {
            sucursalId: '',
            servicioId: '',
            fecha: '',
            hora: ''
          }
          
          // Mostramos mensaje de éxito
          this.$store.dispatch('notificaciones/agregarNotificacion', {
            tipo: 'exito',
            mensaje: `Turno ${nuevoTurnoCreado.codigo} creado exitosamente`
          })
          
          this.cargando = false
        }, 1000)
      } catch (error) {
        this.error = 'Error al solicitar turno: ' + error.message
        console.error('Error al solicitar turno:', error)
        this.cargando = false
      }
    },
    
    /**
     * Cancela un turno existente
     */
    async cancelarTurno(id) {
      if (!confirm('¿Estás seguro de que deseas cancelar este turno?')) {
        return
      }
      
      this.cargando = true
      try {
        // Aquí se enviaría la solicitud a la API
        console.log('Cancelando turno:', id)
        
        // Simulamos una respuesta exitosa
        setTimeout(() => {
          // Encontramos el turno a cancelar
          const turnoIndex = this.turnosActivos.findIndex(t => t.id === id)
          if (turnoIndex !== -1) {
            const turnoCancelado = {...this.turnosActivos[turnoIndex], estado: 'cancelado'}
            
            // Eliminamos de activos y agregamos al historial
            this.turnosActivos.splice(turnoIndex, 1)
            this.historialTurnos.unshift(turnoCancelado)
            
            // Mostramos mensaje de éxito
            this.$store.dispatch('notificaciones/agregarNotificacion', {
              tipo: 'info',
              mensaje: `Turno ${turnoCancelado.codigo} cancelado exitosamente`
            })
          }
          
          this.cargando = false
        }, 1000)
      } catch (error) {
        this.error = 'Error al cancelar turno: ' + error.message
        console.error('Error al cancelar turno:', error)
        this.cargando = false
      }
    },
    
    /**
     * Formatea una fecha y hora para mostrarla al usuario
     */
    formatearFechaHora(fechaHora) {
      const fecha = new Date(fechaHora)
      return fecha.toLocaleString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    
    /**
     * Traduce los códigos de estado a texto legible
     */
    traducirEstado(estado) {
      const traducciones = {
        'pendiente': 'Pendiente',
        'en_espera': 'En Espera',
        'en_atencion': 'En Atención',
        'completado': 'Completado',
        'cancelado': 'Cancelado'
      }
      return traducciones[estado] || estado
    }
  }
}
</script>

<style scoped>
@reference "../../assets/css/main.css";
.spinner {
  @apply w-[2rem] h-[2rem] border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin;
}
</style>

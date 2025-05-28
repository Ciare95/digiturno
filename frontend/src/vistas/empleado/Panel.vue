<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-800 mb-6">Panel de Empleado</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
      <!-- Tarjeta de Bienvenida -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-3">Bienvenido, {{ nombreEmpleado }}</h2>
        <p class="text-gray-600 mb-4">
          Desde este panel podrás gestionar los turnos asignados y ver tus estadísticas.
        </p>
        <div class="flex items-center space-x-2 text-sm">
          <span :class="estadoConexionClase" class="px-2 py-1 rounded-full text-xs font-medium">
            {{ estadoConexionTexto }}
          </span>
          <span>Ventanilla: {{ ventanillaAsignada || 'No asignada' }}</span>
        </div>
      </div>
      
      <!-- Tarjeta de Turno Actual -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-3">Turno Actual</h2>
        
        <div v-if="cargando" class="flex justify-center py-4">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
        
        <div v-else-if="!turnoActual" class="text-center py-6">
          <div class="text-gray-500 mb-4">No tienes un turno en atención</div>
          <button @click="llamarSiguienteTurno" class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition-colors">
            Llamar Siguiente Turno
          </button>
        </div>
        
        <div v-else class="border border-blue-200 rounded-lg p-4 bg-blue-50">
          <div class="text-center mb-3">
            <span class="text-3xl font-bold text-blue-700">{{ turnoActual.numero_turno }}</span>
          </div>
          
          <div class="space-y-2 mb-4">
            <div class="flex justify-between">
              <span class="text-gray-600">Servicio:</span>
              <span class="font-medium">{{ turnoActual.servicio.nombre }}</span>
            </div>
            
            <div class="flex justify-between">
              <span class="text-gray-600">Cliente:</span>
              <span class="font-medium">{{ nombreCliente }}</span>
            </div>
            
            <div class="flex justify-between">
              <span class="text-gray-600">Tiempo en atención:</span>
              <span class="font-medium">{{ tiempoEnAtencion }}</span>
            </div>
          </div>
          
          <div class="flex space-x-2">
            <button @click="finalizarTurno" class="flex-1 bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-3 rounded-md transition-colors text-sm">
              Finalizar
            </button>
            
            <button @click="transferirTurno" class="flex-1 bg-purple-600 hover:bg-purple-700 text-white font-medium py-2 px-3 rounded-md transition-colors text-sm">
              Transferir
            </button>
            
            <button @click="marcarAusente" class="flex-1 bg-orange-600 hover:bg-orange-700 text-white font-medium py-2 px-3 rounded-md transition-colors text-sm">
              Ausente
            </button>
          </div>
        </div>
      </div>
      
      <!-- Tarjeta de Estadísticas -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-3">Estadísticas de Hoy</h2>
        
        <div v-if="cargando" class="flex justify-center py-4">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
        
        <div v-else class="space-y-4">
          <div class="flex items-center justify-between">
            <span class="text-gray-600">Turnos atendidos:</span>
            <span class="bg-blue-100 text-blue-800 font-medium px-3 py-1 rounded-full text-sm">
              {{ estadisticasHoy.turnosAtendidos || 0 }}
            </span>
          </div>
          
          <div class="flex items-center justify-between">
            <span class="text-gray-600">Tiempo promedio:</span>
            <span class="bg-green-100 text-green-800 font-medium px-3 py-1 rounded-full text-sm">
              {{ estadisticasHoy.tiempoPromedio || '0 min' }}
            </span>
          </div>
          
          <div class="flex items-center justify-between">
            <span class="text-gray-600">Calificación promedio:</span>
            <span class="bg-yellow-100 text-yellow-800 font-medium px-3 py-1 rounded-full text-sm flex items-center">
              <span>{{ estadisticasHoy.calificacionPromedio || '0' }}</span>
              <span class="ml-1 text-yellow-500">★</span>
            </span>
          </div>
          
          <div class="mt-4 text-center">
            <router-link to="/empleado/estadisticas" class="text-blue-600 hover:text-blue-800 text-sm font-medium">
              Ver estadísticas completas
            </router-link>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Cola de Turnos -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">Cola de Turnos</h2>
        <div class="flex space-x-2">
          <button @click="actualizarCola" class="bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-1 px-3 rounded-md transition-colors text-sm flex items-center">
            <i class="fas fa-sync-alt mr-1"></i> Actualizar
          </button>
          
          <button @click="llamarSiguienteTurno" class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-1 px-3 rounded-md transition-colors text-sm">
            Llamar Siguiente
          </button>
        </div>
      </div>
      
      <div v-if="cargando" class="flex justify-center py-4">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
      
      <div v-else-if="colaTurnos.length === 0" class="text-center py-6 text-gray-500">
        No hay turnos en espera
      </div>
      
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Posición</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Turno</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Servicio</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cliente</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tiempo Espera</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="(turno, index) in colaTurnos" :key="turno.id" :class="index === 0 ? 'bg-blue-50' : ''">
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="index === 0 ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'" class="px-2 py-1 rounded-full text-xs font-medium">
                  {{ turno.posicion_cola }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap font-medium">
                {{ turno.turno.numero_turno }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                {{ turno.servicio.nombre }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                {{ obtenerNombreCliente(turno.turno.usuario) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                {{ formatearTiempoEspera(turno.turno.fecha_creacion) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <button @click="llamarTurno(turno.turno)" class="text-blue-600 hover:text-blue-800 font-medium text-sm">
                  Llamar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- Modal de Transferir Turno (simplificado) -->
    <div v-if="mostrarModalTransferir" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full">
        <div class="p-4 border-b border-gray-200">
          <h3 class="text-lg font-semibold">Transferir Turno</h3>
        </div>
        
        <div class="p-6">
          <form @submit.prevent="confirmarTransferencia">
            <div class="mb-4">
              <label class="block text-gray-700 font-medium mb-2">Servicio Destino</label>
              <select v-model="transferencia.servicio_id" class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                <option value="" disabled>Selecciona un servicio</option>
                <option v-for="servicio in servicios" :key="servicio.id" :value="servicio.id">
                  {{ servicio.nombre }}
                </option>
              </select>
            </div>
            
            <div class="mb-4">
              <label class="block text-gray-700 font-medium mb-2">Motivo de Transferencia</label>
              <textarea v-model="transferencia.motivo" class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" rows="3" required></textarea>
            </div>
          </form>
        </div>
        
        <div class="p-4 border-t border-gray-200 flex justify-end space-x-3">
          <button @click="mostrarModalTransferir = false" class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition-colors">
            Cancelar
          </button>
          <button @click="confirmarTransferencia" class="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 transition-colors" :disabled="cargando">
            Transferir
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useStore } from 'vuex';

export default {
  name: 'PanelEmpleado',
  setup() {
    const tienda = useStore();
    
    // Estado
    const mostrarModalTransferir = ref(false);
    const transferencia = ref({
      servicio_id: '',
      motivo: ''
    });
    const intervaloActualizacion = ref(null);
    
    // Computadas
    const usuario = computed(() => tienda.state.usuario);
    const nombreEmpleado = computed(() => {
      return usuario.value ? `${usuario.value.first_name} ${usuario.value.last_name}` : '';
    });
    const cargando = computed(() => tienda.state.cargando);
    const error = computed(() => tienda.state.error);
    const turnos = computed(() => tienda.state.turnos);
    const servicios = computed(() => tienda.state.servicios);
    
    const turnoActual = computed(() => {
      return turnos.value.find(turno => 
        turno.estado === 'en_atencion' && 
        turno.empleado?.id === usuario.value?.perfil_empleado?.id
      );
    });
    
    const colaTurnos = computed(() => {
      // Simulamos la cola de turnos (en una implementación real, esto vendría del backend)
      return turnos.value
        .filter(turno => turno.estado === 'en_espera')
        .map((turno, index) => ({
          id: `cola-${turno.id}`,
          turno: turno,
          servicio: turno.servicio,
          posicion_cola: index + 1,
          tiempo_espera_estimado: 5 * (index + 1)
        }))
        .sort((a, b) => a.posicion_cola - b.posicion_cola);
    });
    
    const nombreCliente = computed(() => {
      if (!turnoActual.value || !turnoActual.value.usuario) return 'Cliente sin registrar';
      const cliente = turnoActual.value.usuario;
      return `${cliente.first_name} ${cliente.last_name}`;
    });
    
    const tiempoEnAtencion = computed(() => {
      if (!turnoActual.value || !turnoActual.value.fecha_inicio_atencion) return '0 min';
      
      const inicio = new Date(turnoActual.value.fecha_inicio_atencion);
      const ahora = new Date();
      const minutos = Math.floor((ahora - inicio) / 60000);
      
      if (minutos < 1) return 'Menos de 1 min';
      return `${minutos} min`;
    });
    
    const estadoConexionClase = computed(() => {
      const estado = usuario.value?.perfil_empleado?.estado_conexion || 'desconectado';
      return estado === 'conectado' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800';
    });
    
    const estadoConexionTexto = computed(() => {
      const estado = usuario.value?.perfil_empleado?.estado_conexion || 'desconectado';
      return estado === 'conectado' ? 'Conectado' : 'Desconectado';
    });
    
    const ventanillaAsignada = computed(() => {
      return usuario.value?.perfil_empleado?.ventanilla_asignada || '';
    });
    
    const estadisticasHoy = computed(() => {
      // Simulamos estadísticas (en una implementación real, esto vendría del backend)
      return {
        turnosAtendidos: 12,
        tiempoPromedio: '8 min',
        calificacionPromedio: '4.5'
      };
    });
    
    // Métodos
    const cargarDatos = async () => {
      try {
        // Cargar datos iniciales
        await tienda.dispatch('cargarTurnosEmpleado');
        
        // Cargar servicios de la sucursal del empleado
        const sucursalId = usuario.value?.perfil_empleado?.sucursal?.id;
        if (sucursalId) {
          await tienda.dispatch('cargarServicios', sucursalId);
        }
      } catch (error) {
        console.error('Error al cargar datos:', error);
      }
    };
    
    const actualizarCola = async () => {
      try {
        await tienda.dispatch('cargarTurnosEmpleado');
      } catch (error) {
        console.error('Error al actualizar cola:', error);
      }
    };
    
    const llamarSiguienteTurno = async () => {
      if (colaTurnos.value.length === 0) return;
      
      const siguienteTurno = colaTurnos.value[0].turno;
      await llamarTurno(siguienteTurno);
    };
    
    const llamarTurno = async (turno) => {
      try {
        await tienda.dispatch('cambiarEstadoTurno', {
          turnoId: turno.id,
          estado: 'llamado'
        });
        
        // Simular que después de 10 segundos, si no se cancela, pasa a estado "en_atencion"
        setTimeout(async () => {
          await tienda.dispatch('cambiarEstadoTurno', {
            turnoId: turno.id,
            estado: 'en_atencion'
          });
          
          await actualizarCola();
        }, 10000);
        
        await actualizarCola();
      } catch (error) {
        console.error('Error al llamar turno:', error);
      }
    };
    
    const finalizarTurno = async () => {
      if (!turnoActual.value) return;
      
      try {
        await tienda.dispatch('cambiarEstadoTurno', {
          turnoId: turnoActual.value.id,
          estado: 'finalizado'
        });
        
        await actualizarCola();
      } catch (error) {
        console.error('Error al finalizar turno:', error);
      }
    };
    
    const transferirTurno = () => {
      if (!turnoActual.value) return;
      mostrarModalTransferir.value = true;
    };
    
    const confirmarTransferencia = async () => {
      if (!turnoActual.value) return;
      
      try {
        // En una implementación real, aquí se enviaría la información de transferencia al backend
        await tienda.dispatch('cambiarEstadoTurno', {
          turnoId: turnoActual.value.id,
          estado: 'transferido',
          servicio_destino: transferencia.value.servicio_id,
          motivo: transferencia.value.motivo
        });
        
        mostrarModalTransferir.value = false;
        transferencia.value = {
          servicio_id: '',
          motivo: ''
        };
        
        await actualizarCola();
      } catch (error) {
        console.error('Error al transferir turno:', error);
      }
    };
    
    const marcarAusente = async () => {
      if (!turnoActual.value) return;
      
      try {
        await tienda.dispatch('cambiarEstadoTurno', {
          turnoId: turnoActual.value.id,
          estado: 'ausente'
        });
        
        await actualizarCola();
      } catch (error) {
        console.error('Error al marcar ausente:', error);
      }
    };
    
    const obtenerNombreCliente = (cliente) => {
      if (!cliente) return 'Cliente sin registrar';
      return `${cliente.first_name} ${cliente.last_name}`;
    };
    
    const formatearTiempoEspera = (fechaCreacion) => {
      if (!fechaCreacion) return '0 min';
      
      const inicio = new Date(fechaCreacion);
      const ahora = new Date();
      const minutos = Math.floor((ahora - inicio) / 60000);
      
      if (minutos < 1) return 'Menos de 1 min';
      return `${minutos} min`;
    };
    
    // Ciclo de vida
    onMounted(() => {
      cargarDatos();
      
      // Actualizar la cola cada 30 segundos
      intervaloActualizacion.value = setInterval(actualizarCola, 30000);
    });
    
    onUnmounted(() => {
      if (intervaloActualizacion.value) {
        clearInterval(intervaloActualizacion.value);
      }
    });
    
    return {
      usuario,
      nombreEmpleado,
      cargando,
      error,
      turnos,
      servicios,
      turnoActual,
      colaTurnos,
      nombreCliente,
      tiempoEnAtencion,
      estadoConexionClase,
      estadoConexionTexto,
      ventanillaAsignada,
      estadisticasHoy,
      mostrarModalTransferir,
      transferencia,
      actualizarCola,
      llamarSiguienteTurno,
      llamarTurno,
      finalizarTurno,
      transferirTurno,
      confirmarTransferencia,
      marcarAusente,
      obtenerNombreCliente,
      formatearTiempoEspera
    };
  }
}
</script>

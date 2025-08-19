<template>
    <div class="min-h-screen bg-gray-100">
    <!-- Barra de navegación -->
    <nav class="bg-white shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex items-center">
                    <div class="flex-shrink-0 flex items-center">
                        <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                            <ClockIcon class="h-5 w-5 text-white" />
                        </div>
                        <span class="ml-2 text-xl font-bold text-gray-800">DigiTurno</span>
                    </div>
                </div>
                <div class="hidden sm:ml-6 sm:flex sm:items-center">
                </div>
            </div>
        </div>
    </nav>

    <!-- Contenido principal -->
    <div class="py-6">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Encabezado -->
        <div class="md:flex md:items-center md:justify-between mb-6">
    </div>
        <!-- Sección de turnos -->
        <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <!-- Cola de turnos -->
          <div class="lg:col-span-2">
            <div class="bg-white shadow overflow-hidden sm:rounded-lg">
              <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                  Cola de Turnos
                </h3>
                <p class="mt-1 text-sm text-gray-500">
                  Turnos pendientes por atender
                </p>
              </div>
              <div class="bg-white overflow-hidden">
                <ul class="divide-y divide-gray-200">
                  <li v-for="turno in turnosPendientes" :key="turno.id" class="px-6 py-4 hover:bg-gray-50">
                    <div class="flex items-center">
                      <div class="flex-shrink-0 h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                        <span class="text-blue-600 font-medium">{{ turno.numero }}</span>
                      </div>
                      <div class="ml-4">
                        <div class="text-sm font-medium text-gray-900">{{ turno.servicio }}</div>
                        <div class="text-sm text-gray-500">{{ turno.cliente }}</div>
                      </div>
                      <div class="ml-auto">
                        <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="{
                          'bg-yellow-100 text-yellow-800': turno.estado === 'Pendiente',
                          'bg-green-100 text-green-800': turno.estado === 'En Atención',
                          'bg-gray-100 text-gray-800': turno.estado === 'Atendido'
                        }">
                          {{ turno.estado }}
                        </span>
                      </div>
                      <div class="ml-4">
                        <button @click="atenderSiguiente(turno)" class="text-sm font-medium text-blue-600 hover:text-blue-500" :disabled="turnoEnProgreso">
                          Atender
                        </button>
                      </div>
                    </div>
                  </li>
                  <li v-if="turnosPendientes.length === 0" class="px-6 py-4 text-center text-gray-500">
                    No hay turnos pendientes
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Panel de control -->
          <div>
            <div class="bg-white shadow overflow-hidden sm:rounded-lg mb-6">
              <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                  Turno Actual
                </h3>
              </div>
              <div class="px-4 py-5 sm:p-6 text-center">
                <div v-if="turnoActual" class="space-y-4">
                  <div class="text-6xl font-bold text-gray-900">
                    {{ turnoActual.numero }}
                  </div>
                  <div class="text-lg font-medium text-gray-900">
                    {{ turnoActual.servicio }}
                  </div>
                  <div class="text-sm text-gray-500">
                    {{ turnoActual.cliente }}
                  </div>
                  <div class="mt-6">
                    <div class="text-4xl font-bold text-blue-600">
                      {{ tiempoTranscurrido }}
                    </div>
                    <div class="text-sm text-gray-500 mt-1">
                      Tiempo de atención
                    </div>
                  </div>
                </div>
                <div v-else class="text-center py-8">
                  <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-gray-100">
                    <ClockIcon class="h-6 w-6 text-gray-400" />
                  </div>
                  <h3 class="mt-2 text-sm font-medium text-gray-900">Sin turno activo</h3>
                  <div class="mt-6">
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { 
  ClockIcon, 
  CheckCircleIcon, 
  UserGroupIcon, 
  UserCircleIcon,
  CalendarIcon
} from '@heroicons/vue/24/outline';
import EmpleadoService from '@/Services/EmpleadoService';

export default {
  name: 'EmpleadoDashboard',
  components: {
    ClockIcon,
    CheckCircleIcon,
    UserGroupIcon,
    UserCircleIcon,
    CalendarIcon
  },
  setup() {
    const router = useRouter();
    const fechaSeleccionada = ref(new Date().toISOString().split('T')[0]);
    const estadisticasServidor = ref({ turnos_atendidos_hoy: 0 });
    const tiempoInicio = ref(null);
    const tiempoTranscurrido = ref('00:00');
    let intervalo = null;

    // Datos reales
    const turnos = ref([]);
    const historial = ref([]);
    const isLoading = ref(true);
    const empleadoInfo = ref({
      nombre: '',
      codigo: '',
      ventanilla: '',
      estado: 'Desconectado',
      sucursal_nombre: ''
    });

    // Función para actualizar datos de turnos
    const actualizarTurnos = async () => {
      try {
        console.log('Actualizando datos de turnos...');
        const [stats, pendientes, actual] = await Promise.all([
          EmpleadoService.obtenerEstadisticas(),
          EmpleadoService.obtenerTurnosPendientes(),
          EmpleadoService.obtenerTurnoActual()
        ]);
        
        estadisticasServidor.value = stats;
        turnos.value = Array.isArray(pendientes) ? pendientes : [];
        
        // Solo actualizar turno actual si hay cambios
        if (actual && (!turnoActual.value || actual.id !== turnoActual.value.id)) {
          turnoActual.value = actual;
          iniciarTemporizador();
        } else if (!actual && turnoActual.value) {
          turnoActual.value = null;
          clearInterval(intervalo);
          tiempoTranscurrido.value = '00:00';
        }
      } catch (error) {
        console.error('Error actualizando turnos:', error);
      }
    };

    // Cargar datos iniciales y configurar polling
    onMounted(async () => {
      try {
        await actualizarTurnos();
        
        const [infoEmpleado, initialHistorial] = await Promise.all([
          EmpleadoService.obtenerInfoEmpleado(),
          EmpleadoService.obtenerHistorial()
        ]);
        
        if (infoEmpleado) {
          empleadoInfo.value = {
            nombre: infoEmpleado.nombre || '',
            codigo: infoEmpleado.codigo_empleado || '',
            ventanilla: infoEmpleado.ventanilla_asignada || '',
            estado: infoEmpleado.estado_conexion ? 'Conectado' : 'Desconectado',
            sucursal_nombre: infoEmpleado.sucursal_nombre || '',
            servicios: infoEmpleado.servicios || []
          };
        }
        
        historial.value = Array.isArray(initialHistorial) ? initialHistorial : [];
      } catch (error) {
        console.error('Error cargando datos:', error);
      } finally {
        isLoading.value = false;
      }

      // Configurar polling cada 5 segundos
      const pollingInterval = setInterval(actualizarTurnos, 5000);
      
      // Limpiar intervalo al desmontar
      onUnmounted(() => {
        clearInterval(pollingInterval);
        clearInterval(intervalo);
      });
    });

    // Turno actual en atención
    const turnoActual = ref(null);
    const turnoEnProgreso = computed(() => turnoActual.value !== null);

    // Filtrar turnos pendientes
    const turnosPendientes = computed(() => {
      console.log('All turnos:', turnos.value); // Debugging
      const pendientes = turnos.value.filter(t => 
        t.estado === 'Pendiente' || 
        t.estado === 'En Espera' ||
        t.estado === 'EN_ESPERA'
      );
      console.log('Turnos pendientes filtrados:', pendientes); // Debugging
      return pendientes;
    });

    // Historial reciente (últimos 5 turnos)
    const historialReciente = computed(() => {
      const sorted = [...historial.value]
        .sort((a, b) => new Date(`1970/01/01 ${b.hora}`) - new Date(`1970/01/01 ${a.hora}`))
        .slice(0, 5);
      
      console.log('Historial reciente calculado:', sorted);
      console.log('Datos completos del historial:', historial.value);
      
      return sorted;
    });

    // Estadísticas
    const estadisticas = computed(() => {
      const atendidos = estadisticasServidor.value?.turnos_atendidos_hoy || 0;
      const enEspera = turnosPendientes.value.length;
      return {
        turnosHoy: atendidos + enEspera,
        atendidosHoy: atendidos,
        enEspera: enEspera,
        enAtencion: turnoActual.value ? 1 : 0
      };
    });

   
    // Atender siguiente turno
    const atenderSiguiente = async (turno) => {
      try {
        if (turnoActual.value) {
          alert('Ya hay un turno en atención. Finalícelo antes de atender otro.');
          return;
        }

        // Actualizar lista de turnos primero
        turnos.value = await EmpleadoService.obtenerTurnosPendientes();
        
        const turnoId = turno?.id;
        if (!turnoId) {
          alert('No se ha seleccionado un turno válido.');
          return;
        }

        console.log('Attempting to attend turn ID:', turnoId, 'Number:', turno.numero);
        console.log('Current turn list:', turnos.value.map(t => ({id: t.id, numero: t.numero})));

        // Verificar que el turno sigue disponible
        const turnoActualizado = turnos.value.find(t => t.id === turnoId);
        if (!turnoActualizado) {
          throw new Error('El turno seleccionado ya no está disponible. Actualizando lista...');
        }
        if (turnoActualizado.estado !== 'Pendiente' && turnoActualizado.estado !== 'En Espera' && turnoActualizado.estado !== 'EN_ESPERA') {
          throw new Error('El turno seleccionado no está disponible para atención.');
        }

        const response = await EmpleadoService.iniciarAtencion(turnoId);
        turnoActual.value = response;
        iniciarTemporizador();

        // Guardar turno actualizado en localStorage para que el cliente lo vea
        localStorage.setItem('ultimoTurno', JSON.stringify({
          ...response,
          estado_display: 'En Atención',
          ventanilla: empleadoInfo.value.ventanilla
        }));

        // Actualizar lista nuevamente después de atender
        turnos.value = await EmpleadoService.obtenerTurnosPendientes();

      } catch (error) {
        console.error('Error al atender turno:', error);
        alert(error.message || 'Error al atender el turno');
        // Forzar actualización de lista
        try {
          turnos.value = await EmpleadoService.obtenerTurnosPendientes();
        } catch (refreshError) {
          console.error('Error actualizando lista de turnos:', refreshError);
        }
      }
    };

    // Llamar siguiente turno
    const llamarSiguiente = async () => {
      if (turnoActual.value) {
        alert('Ya hay un turno en atención. Finalícelo antes de llamar a otro.');
        return;
      }
      
      try {
        // Actualizar lista de turnos primero
        turnos.value = await EmpleadoService.obtenerTurnosPendientes();
        
        if (turnos.value.length === 0) {
          throw new Error('No hay turnos disponibles en la cola');
        }

        const response = await EmpleadoService.iniciarAtencion(null);
        turnoActual.value = response;
        iniciarTemporizador();

        // Guardar turno actualizado en localStorage para que el cliente lo vea
        localStorage.setItem('ultimoTurno', JSON.stringify({
          ...response,
          estado_display: 'En Atención',
          ventanilla: empleadoInfo.value.ventanilla
        }));
        
        // Actualizar lista nuevamente después de atender
        turnos.value = await EmpleadoService.obtenerTurnosPendientes();
      } catch (error) {
        console.error('Error al llamar al siguiente turno:', error);
        alert(error.message || 'No se pudo llamar al siguiente turno.');
        // Forzar actualización de lista
        turnos.value = await EmpleadoService.obtenerTurnosPendientes();
      }
    };

    // Finalizar turno actual
    const finalizarTurno = async () => {
      if (turnoActual.value) {
        try {
          console.log('Iniciando finalizarTurno con turnoActual:', turnoActual.value);
          
          // Finalizar el turno actual y obtener datos completos
          const turnoFinalizado = await EmpleadoService.finalizarAtencion(turnoActual.value.id);
          console.log('Turno finalizado recibido:', turnoFinalizado);
          console.log('Estado del turno finalizado:', turnoFinalizado.estado, 'Estado display:', turnoFinalizado.estado_display);
          
          // Crear entrada para historial
          const historialEntry = {
            id: turnoFinalizado.id,
            numero: turnoFinalizado.numero,
            servicio: turnoFinalizado.servicio,
            cliente: turnoFinalizado.cliente,
            estado: turnoFinalizado.estado,
            estado_display: turnoFinalizado.estado_display || 'Atendido',
            fecha_creacion: turnoFinalizado.fecha_creacion,
            hora: turnoFinalizado.hora
          };
          console.log('Nueva entrada de historial:', historialEntry);
          
          // Agregar al historial
          historial.value.unshift(historialEntry);
          console.log('Historial actualizado:', historial.value);

          // Mantener solo los últimos 5 turnos
          if (historial.value.length > 5) {
            historial.value = historial.value.slice(0, 5);
          }

          // Actualizar solo las estadísticas y lista de pendientes
          const [stats, updatedTurnos] = await Promise.all([
            EmpleadoService.obtenerEstadisticas(),
            EmpleadoService.obtenerTurnosPendientes()
          ]);

          estadisticasServidor.value = stats;
          turnos.value = Array.isArray(updatedTurnos) ? updatedTurnos : [];
          
          turnoActual.value = null;
          clearInterval(intervalo);
          tiempoTranscurrido.value = '00:00';
        } catch (error) {
          console.error('Error al finalizar turno:', error);
          alert('Error al finalizar el turno.');
        }
      }
    };

    // Marcar como ausente
    const ausenteTurno = () => {
      if (turnoActual.value) {
        // Mover a historial como ausente
        const turnoAusente = {
          ...turnoActual.value,
          estado: 'Ausente',
          hora: new Date().toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' }),
          duracion: '--:--'
        };
        
        historial.value.unshift(turnoAusente);
        
        // Eliminar de la lista de turnos
        turnos.value = turnos.value.filter(t => t.id !== turnoActual.value.id);
        
        // Limpiar turno actual
        turnoActual.value = null;
        clearInterval(intervalo);
        tiempoTranscurrido.value = '00:00';
      }
    };

    // Cerrar sesión
    const cerrarSesion = () => {
      // Detener temporizador si está activo
      if (turnoActual.value) {
        finalizarTurno();
      }
      
      // Eliminar datos de sesión (simulado)
      localStorage.removeItem('token');
      localStorage.removeItem('userRole');
      
      // Redirigir al login
      router.push('/login');
    };

    // Limpiar intervalo al desmontar el componente
    onUnmounted(() => {
      clearInterval(intervalo);
    });

    return {
      // Datos
      turnoActual,
      turnoEnProgreso,
      turnosPendientes,
      historialReciente,
      estadisticas,
      fechaSeleccionada,
      tiempoTranscurrido,
      
      // Datos
      empleadoInfo,
      
      // Métodos
      atenderSiguiente,
      llamarSiguiente,
      finalizarTurno,
      ausenteTurno,
      cerrarSesion
    };
  }
};
</script>

<style scoped>
/* Estilos específicos del panel de empleado */

/* Transiciones suaves */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* Estilos para las tarjetas de estadísticas */
.stat-card {
  transition: all 0.2s ease-in-out;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
</style>

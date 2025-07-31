<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Barra de navegación -->
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center
          ">
            <div class="flex-shrink-0 flex items-center">
              <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <ClockIcon class="h-5 w-5 text-white" />
              </div>
              <span class="ml-2 text-xl font-bold text-gray-800">DigiTurno</span>
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <router-link to="/empleado" class="border-b-2 border-blue-500 text-gray-900 inline-flex items-center px-1 pt-1 text-sm font-medium">
                Panel de Turnos
              </router-link>
            </div>
          </div>
          <div class="hidden sm:ml-6 sm:flex sm:items-center">
            <span v-if="sucursalActual?.nombre" class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800 mr-4">
              {{ sucursalActual.nombre }}
            </span>
            <span v-else class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-800 mr-4">
              Sucursal no disponible
            </span>
            <button @click="cerrarSesion" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
              Cerrar Sesión
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Contenido principal -->
    <div class="py-6">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Encabezado -->
        <div class="md:flex md:items-center md:justify-between mb-6">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Panel de Turnos</h1>
            <p class="mt-1 text-sm text-gray-600">Gestiona los turnos de la sucursal</p>
          </div>
          <div class="mt-4 flex md:mt-0 md:ml-4
          ">
            <div class="relative rounded-md shadow-sm">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <CalendarIcon class="h-5 w-5 text-gray-400" />
              </div>
              <input type="date" v-model="fechaSeleccionada" class="focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 sm:text-sm border-gray-300 rounded-md py-2">
            </div>
          </div>
        </div>

        <!-- Estadísticas rápidas -->
        <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-6">
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0 bg-blue-500 rounded-md p-3">
                  <UserGroupIcon class="h-6 w-6 text-white" />
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">
                      Turnos Hoy
                    </dt>
                    <dd class="flex items-baseline">
                      <div class="text-2xl font-semibold text-gray-900">
                        {{ estadisticas.turnosHoy }}
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0 bg-green-500 rounded-md p-3">
                  <CheckCircleIcon class="h-6 w-6 text-white" />
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">
                      Atendidos Hoy
                    </dt>
                    <dd class="flex items-baseline">
                      <div class="text-2xl font-semibold text-gray-900">
                        {{ estadisticas.atendidosHoy }}
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0 bg-yellow-500 rounded-md p-3">
                  <ClockIcon class="h-6 w-6 text-white" />
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">
                      En Espera
                    </dt>
                    <dd class="flex items-baseline">
                      <div class="text-2xl font-semibold text-gray-900">
                        {{ estadisticas.enEspera }}
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0 bg-purple-500 rounded-md p-3">
                  <UserCircleIcon class="h-6 w-6 text-white" />
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">
                      En Atención
                    </dt>
                    <dd class="flex items-baseline">
                      <div class="text-2xl font-semibold text-gray-900">
                        {{ estadisticas.enAtencion }}
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
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
                  <div class="mt-6 space-y-3">
                    <button @click="finalizarTurno" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
                      Finalizar Atención
                    </button>
                    <button @click="llamarSiguiente" :disabled="turnosPendientes.length === 0" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed">
                      Llamar Siguiente
                    </button>
                    <button @click="ausenteTurno" class="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                      Marcar como Ausente
                    </button>
                  </div>
                </div>
                <div v-else class="text-center py-8">
                  <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-gray-100">
                    <ClockIcon class="h-6 w-6 text-gray-400" />
                  </div>
                  <h3 class="mt-2 text-sm font-medium text-gray-900">Sin turno activo</h3>
                  <p class="mt-1 text-sm text-gray-500">
                    Selecciona un turno para comenzar
                  </p>
                  <div class="mt-6">
                    <button @click="llamarSiguiente" :disabled="turnosPendientes.length === 0" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed">
                      Llamar Siguiente Turno
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Historial reciente -->
            <div class="bg-white shadow overflow-hidden sm:rounded-lg">
              <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                  Historial Reciente
                </h3>
              </div>
              <div class="divide-y divide-gray-200">
                <div v-for="turno in historialReciente" :key="turno.id" class="px-6 py-4">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-100 flex items-center justify-center">
                      <span class="text-gray-600 font-medium">{{ turno.numero }}</span>
                    </div>
                    <div class="ml-4">
                      <div class="text-sm font-medium text-gray-900">{{ turno.servicio }}</div>
                      <div class="text-sm text-gray-500">{{ turno.cliente }}</div>
                    </div>
                    <div class="ml-auto">
                      <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="{
                        'bg-green-100 text-green-800': turno.estado === 'Atendido',
                        'bg-red-100 text-red-800': turno.estado === 'Ausente',
                        'bg-gray-100 text-gray-800': turno.estado === 'Cancelado'
                      }">
                        {{ turno.estado }}
                      </span>
                    </div>
                  </div>
                </div>
                <div v-if="historialReciente.length === 0" class="px-6 py-4 text-center text-gray-500">
                  No hay historial reciente
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
    const tiempoInicio = ref(null);
    const tiempoTranscurrido = ref('00:00');
    let intervalo = null;

    // Datos reales
    const sucursalActual = ref({});
    const turnos = ref([]);
    const historial = ref([]);
    const isLoading = ref(true);

    // Cargar datos iniciales
    onMounted(async () => {
      try {
        const [estadisticas, pendientes, actual] = await Promise.all([
          EmpleadoService.obtenerEstadisticas(),
          EmpleadoService.obtenerTurnosPendientes(),
          EmpleadoService.obtenerTurnoActual()
        ]);
        
        console.log('Datos cargados:', { estadisticas, pendientes, actual }); // Debugging
        sucursalActual.value = estadisticas.sucursal || {};
        turnos.value = Array.isArray(pendientes) ? pendientes : [];
        if (actual) {
          turnoActual.value = actual;
          iniciarTemporizador();
        }
      } catch (error) {
        console.error('Error cargando datos:', error);
      } finally {
        isLoading.value = false;
      }
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
      return [...historial.value]
        .sort((a, b) => new Date(`1970/01/01 ${b.hora}`) - new Date(`1970/01/01 ${a.hora}`))
        .slice(0, 5);
    });

    // Estadísticas
    const estadisticas = computed(() => {
      const hoy = new Date().toISOString().split('T')[0];
      return {
        turnosHoy: turnos.value.length,
        atendidosHoy: historial.value.filter(t => 
          t.estado === 'Atendido' || 
          t.estado === 'ATENDIDO'
        ).length,
        enEspera: turnosPendientes.value.length,
        enAtencion: turnoActual.value ? 1 : 0
      };
    });

    // Iniciar temporizador
    const iniciarTemporizador = () => {
      tiempoInicio.value = new Date();
      clearInterval(intervalo);
      
      intervalo = setInterval(() => {
        if (tiempoInicio.value) {
          const ahora = new Date();
          const diff = Math.floor((ahora - tiempoInicio.value) / 1000);
          const minutos = Math.floor(diff / 60).toString().padStart(2, '0');
          const segundos = (diff % 60).toString().padStart(2, '0');
          tiempoTranscurrido.value = `${minutos}:${segundos}`;
        }
      }, 1000);
    };

    // Atender siguiente turno
    const atenderSiguiente = async (turno) => {
      try {
        if (turnoActual.value) {
          await finalizarTurno();
        }

        // Refetch turns before attempting to start attention
        const updatedTurnos = await EmpleadoService.obtenerTurnosPendientes();
        turnos.value = updatedTurnos;

        // Find the turn in the updated list
        const turnoToAttend = turnos.value.find(t => t.id === turno.id);
        if (!turnoToAttend) {
          throw new Error('El turno especificado no está disponible.');
        }

        const response = await EmpleadoService.iniciarAtencion(turnoToAttend.id);
        turnoActual.value = response;
        iniciarTemporizador();

        // Refresh turn list again after successful attention start
        turnos.value = await EmpleadoService.obtenerTurnosPendientes();
      } catch (error) {
        console.error('Error al atender turno:', error);
        alert(error.message || 'Error al atender el turno');
        // Refresh turn list in case the error was due to stale data
        turnos.value = await EmpleadoService.obtenerTurnosPendientes();
      }
    };

    // Llamar siguiente turno
    const llamarSiguiente = () => {
      if (turnosPendientes.value.length > 0) {
        atenderSiguiente(turnosPendientes.value[0]);
      }
    };

    // Finalizar turno actual
    const finalizarTurno = async () => {
      if (turnoActual.value) {
        try {
          await EmpleadoService.finalizarAtencion(turnoActual.value.id);
          
          // Actualizar historial y turnos
          const [updatedHistorial, updatedTurnos] = await Promise.all([
            EmpleadoService.obtenerHistorial(),
            EmpleadoService.obtenerTurnosPendientes()
          ]);
          
          historial.value = updatedHistorial;
          turnos.value = updatedTurnos;
          
          // Limpiar turno actual
          turnoActual.value = null;
          clearInterval(intervalo);
          tiempoTranscurrido.value = '00:00';
        } catch (error) {
          console.error('Error al finalizar turno:', error);
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
      sucursalActual,
      turnoActual,
      turnoEnProgreso,
      turnosPendientes,
      historialReciente,
      estadisticas,
      fechaSeleccionada,
      tiempoTranscurrido,
      
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

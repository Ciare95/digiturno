<template>
  <div class="min-h-screen flex flex-col bg-gradient-to-br from-gray-50 to-blue-50">
    <!-- Header -->
    <AppHeader />

    <!-- Contenido Principal -->
    <main class="flex-grow py-12 px-4">
      <div class="max-w-4xl mx-auto">
        <!-- Encabezado -->
        <div class="text-center mb-12">
          <h1 class="text-4xl font-bold text-gray-900 mb-2">Turno Generado</h1>
          <p class="text-xl text-gray-600">Tu turno ha sido registrado exitosamente</p>
        </div>

        <!-- Tarjeta del turno -->
        <div v-if="turno" class="bg-white rounded-2xl shadow-xl overflow-hidden">
          <div class="bg-gradient-to-r from-green-600 to-green-700 px-8 py-6">
            <h2 class="text-2xl font-bold text-white">Tu Turno</h2>
            <p class="text-green-100 mt-1">Información completa de tu turno</p>
          </div>
          
          <div class="p-8">
            <!-- Número de turno destacado -->
            <div class="text-center mb-8">
              <p class="text-sm font-medium text-gray-500 mb-2">Número de turno</p>
              <div class="bg-green-50 rounded-lg p-6">
                <span class="text-6xl font-bold text-green-600">{{ turno.numero_turno }}</span>
              </div>
            </div>
            
            <!-- Información del turno -->
            <div class="grid md:grid-cols-2 gap-8">
              <!-- Columna izquierda -->
              <div class="space-y-6">
                <div class="bg-gray-50 rounded-lg p-6">
                  <h3 class="text-lg font-semibold text-gray-900 mb-4">Información del Servicio</h3>
                  <div class="space-y-3">
                    <div>
                      <p class="text-sm font-medium text-gray-500">Servicio</p>
                      <p class="font-medium text-gray-900">{{ turno.servicio_nombre }}</p>
                    </div>
                    <div>
                      <p class="text-sm font-medium text-gray-500">Sucursal</p>
                      <p class="font-medium text-gray-900">{{ turno.sucursal_nombre }}</p>
                    </div>
                    <div>
                      <p class="text-sm font-medium text-gray-500">Estado</p>
                      <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                        {{ turno.estado_display }}
                      </span>
                    </div>
                  </div>
                </div>

                <div class="bg-gray-50 rounded-lg p-6">
                  <h3 class="text-lg font-semibold text-gray-900 mb-4">Información Personal</h3>
                  <div class="space-y-3">
                    <div>
                      <p class="text-sm font-medium text-gray-500">Nombre</p>
                      <p class="font-medium text-gray-900">{{ turno.nombre_cliente }}</p>
                    </div>
                    <div>
                      <p class="text-sm font-medium text-gray-500">Número de Cédula</p>
                      <p class="font-medium text-gray-900">{{ turno.numero_cedula }}</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Columna derecha -->
              <div class="space-y-6">
                <div class="bg-gray-50 rounded-lg p-6">
                  <h3 class="text-lg font-semibold text-gray-900 mb-4">Tiempos</h3>
                  <div class="space-y-3">
                    <div>
                      <p class="text-sm font-medium text-gray-500">Fecha de Solicitud</p>
                      <p class="font-medium text-gray-900">
                        {{ new Date(turno.fecha_creacion).toLocaleDateString() }}
                      </p>
                      <p class="text-sm text-gray-500">
                        {{ new Date(turno.fecha_creacion).toLocaleTimeString() }}
                      </p>
                    </div>
                    <div v-if="turno.fecha_inicio_atencion">
                      <p class="text-sm font-medium text-gray-500">Inicio de Atención</p>
                      <p class="font-medium text-gray-900">
                        {{ new Date(turno.fecha_inicio_atencion).toLocaleDateString() }}
                      </p>
                      <p class="text-sm text-gray-500">
                        {{ new Date(turno.fecha_inicio_atencion).toLocaleTimeString() }}
                      </p>
                    </div>
                    <div v-if="turno.fecha_finalizacion">
                      <p class="text-sm font-medium text-gray-500">Finalización</p>
                      <p class="font-medium text-gray-900">
                        {{ new Date(turno.fecha_finalizacion).toLocaleDateString() }}
                      </p>
                      <p class="text-sm text-gray-500">
                        {{ new Date(turno.fecha_finalizacion).toLocaleTimeString() }}
                      </p>
                    </div>
                  </div>
                </div>

                <div class="bg-blue-50 rounded-lg p-6">
                  <h3 class="text-lg font-semibold text-blue-900 mb-4">Información de Cola</h3>
                  <div class="space-y-4">
                    <div class="text-center">
                      <div class="text-3xl font-bold text-blue-600 mb-2">
                        {{ calcularTiempoEspera() }} minutos
                      </div>
                      <p class="text-sm text-blue-700">
                        Tiempo aproximado de espera
                      </p>
                    </div>
                    <div class="text-center pt-4 border-t border-blue-200">
                      <div class="text-2xl font-bold text-blue-600 mb-2">
                        Posición {{ turno.posicion_cola || 1 }}
                      </div>
                      <p class="text-sm text-blue-700">
                        En la cola de espera
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Botones de acción -->
            <div class="mt-8 pt-6 border-t border-gray-200">
              <div class="flex flex-col sm:flex-row gap-4 justify-center">
                <button 
                  @click="volverASolicitar"
                  class="px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Solicitar Otro Turno
                </button>
                <button 
                  @click="verMisTurnos"
                  class="px-6 py-3 bg-gray-600 text-white font-medium rounded-lg hover:bg-gray-700 transition-colors"
                >
                  Ver Mis Turnos
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Mensaje de error si no hay turno -->
        <div v-else class="text-center">
          <div class="bg-red-50 border border-red-200 rounded-lg p-6">
            <svg class="h-12 w-12 text-red-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
            </svg>
            <h3 class="text-lg font-medium text-red-800 mb-2">No se encontró información del turno</h3>
            <p class="text-red-700">Por favor, solicita un nuevo turno.</p>
            <button 
              @click="volverASolicitar"
              class="mt-4 px-4 py-2 bg-red-600 text-white font-medium rounded-lg hover:bg-red-700 transition-colors"
            >
              Solicitar Turno
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <AppFooter />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import AppHeader from '@/components/layout/AppHeader.vue';
import AppFooter from '@/components/layout/AppFooter.vue';

const route = useRoute();
const router = useRouter();
const turno = ref(null);

onMounted(() => {
  // Obtener el turno desde los parámetros de la ruta o localStorage
  if (route.params.turno) {
    try {
      turno.value = JSON.parse(route.params.turno);
    } catch (error) {
      console.error('Error al parsear el turno:', error);
    }
  }
  
  // Si no hay turno en los parámetros, intentar obtener desde localStorage
  if (!turno.value) {
    const turnoGuardado = localStorage.getItem('ultimoTurno');
    if (turnoGuardado) {
      try {
        turno.value = JSON.parse(turnoGuardado);
      } catch (error) {
        console.error('Error al parsear el turno del localStorage:', error);
      }
    }
  }
});

const calcularTiempoEspera = () => {
  if (!turno.value) return 0;
  
  // Usar el tiempo de espera que viene del backend
  return turno.value.tiempo_espera_estimado || 0;
};

const volverASolicitar = () => {
  router.push('/solicitar-turno');
};

const verMisTurnos = () => {
  router.push('/mis-turnos');
};
</script>

<style scoped>
/* Transiciones suaves */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style> 
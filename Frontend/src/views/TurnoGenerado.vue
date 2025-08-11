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
              
              <!-- Mensaje de ventanilla cuando está en atención -->
              <div v-if="turno.estado_display === 'En Atención' && turno.ventanilla" 
                   class="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div class="flex items-center justify-center gap-3">
                  <svg class="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
                  </svg>
                  <p class="text-lg font-medium text-blue-800">
                    Puede pasar a la ventanilla <span class="font-bold">{{ turno.ventanilla }}</span>
                  </p>
                </div>
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
                  @click="cancelarTurno"
                  class="px-6 py-3 bg-red-600 text-white font-medium rounded-lg hover:bg-red-700 transition-colors"
                  v-if="turno && turno.estado_display === 'En Espera'"
                >
                  Cancelar Turno
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

  <!-- Modal de calificación -->
  <div v-if="showRatingModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 max-w-md w-full">
      <h3 class="text-xl font-bold text-gray-900 mb-4">Califica tu experiencia</h3>
      <p class="text-gray-600 mb-4">¿Cómo calificarías el servicio recibido?</p>
      
      <div class="flex justify-center mb-6">
        <div v-for="star in 5" :key="star" 
             @click="rating = star" 
             class="text-3xl cursor-pointer"
             :class="star <= rating ? 'text-yellow-400' : 'text-gray-300'">
          ★
        </div>
      </div>
      
      <textarea v-model="comentario" 
                class="w-full border border-gray-300 rounded-md p-2 mb-4" 
                placeholder="Opcional: Deja un comentario sobre tu experiencia"
                rows="3"></textarea>
      
      <div class="flex justify-end gap-3">
        <button @click="showRatingModal = false" 
                class="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400">
          Cancelar
        </button>
        <button @click="enviarCalificacion" 
                class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
          Enviar Calificación
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import AppHeader from '@/components/layout/AppHeader.vue';
import AppFooter from '@/components/layout/AppFooter.vue';

const route = useRoute();
const router = useRouter();
const turno = ref(null);
const showRatingModal = ref(false);
const rating = ref(0);
const comentario = ref('');

onMounted(() => {
  let pollingInterval = null;

  const preguntarPorCalificacion = (turnoId) => {
    const calificacionKey = `calificacionMostrada_${turnoId}`;
    if (localStorage.getItem(calificacionKey)) {
      console.log(`La pregunta de calificación para el turno ${turnoId} ya fue mostrada.`);
      return;
    }

    console.log(`Mostrando pregunta de calificación para el turno ${turnoId}.`);
    if (confirm('¿Desea calificar el servicio recibido?')) {
      showRatingModal.value = true;
    } else {
      router.push('/solicitar-turno');
    }
    localStorage.setItem(calificacionKey, 'true');
  };

  const procesarDatosTurno = (data) => {
    const estadoFinalizado = data.estado_display === 'Atendido' || data.estado_display === 'Finalizado';
    
    if (estadoFinalizado) {
      preguntarPorCalificacion(data.id);
    }
  };

  const cargarTurno = () => {
    console.log('Cargando turno...');
    const turnoId = route.params.id;
    const turnoGuardado = localStorage.getItem('ultimoTurno');

    if (turnoGuardado) {
      try {
        const parsedTurno = JSON.parse(turnoGuardado);
        // Si el turno en localStorage corresponde al de la URL, lo usamos
        if (parsedTurno.id == turnoId) {
          turno.value = parsedTurno;
          console.log('Turno cargado desde localStorage:', parsedTurno);
          procesarDatosTurno(parsedTurno);
        }
      } catch (e) {
        console.error('Error parseando turno desde localStorage', e);
      }
    }
    
    // Si no hay turno cargado (o no coincide), establecemos el ID para el polling
    if (!turno.value && turnoId) {
      turno.value = { id: turnoId };
      console.log(`ID de turno ${turnoId} establecido desde la URL. Esperando polling...`);
    }

    if (!turno.value) {
      console.warn('No se encontró información del turno');
    }
  };

  const actualizarTurnoDesdeServidor = async () => {
    if (!turno.value?.id) {
      console.log('Polling: No hay ID de turno, deteniendo.');
      clearInterval(pollingInterval);
      return;
    }

    console.log(`Polling: Verificando estado para turno ID: ${turno.value.id}`);
    try {
      const response = await fetch(`/api/turns/public/turno/${turno.value.id}/status/`);
      if (!response.ok) {
        console.warn(`Polling: Respuesta no OK (${response.status})`);
        return;
      }
      const data = await response.json();
      console.log('Polling: Datos recibidos:', data);

      const estadoAnterior = turno.value.estado_display;
      const estadoNuevo = data.estado_display;

      if (estadoAnterior !== estadoNuevo || data.ventanilla !== turno.value.ventanilla) {
        console.log(`Actualizando turno. Estado: ${estadoAnterior} -> ${estadoNuevo}.`);
        turno.value = { ...turno.value, ...data };
        localStorage.setItem('ultimoTurno', JSON.stringify(turno.value));
        procesarDatosTurno(data);
      }
    } catch (error) {
      console.error('Polling: Error al actualizar turno:', error);
    }
  };

  cargarTurno();

  window.addEventListener('storage', (event) => {
    if (event.key === 'ultimoTurno') {
      console.log('Detectado cambio en localStorage, recargando turno.');
      cargarTurno();
    }
  });

  pollingInterval = setInterval(actualizarTurnoDesdeServidor, 5000);

  onUnmounted(() => {
    console.log('Componente desmontado, limpiando intervalo de polling.');
    clearInterval(pollingInterval);
  });
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

const cancelarTurno = async () => {
  if (!turno.value || !turno.value.id) return;

  if (confirm('¿Estás seguro de que deseas cancelar este turno?')) {
    try {
      const response = await fetch(`/api/turns/public/turno/${turno.value.id}/cancelar/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Error al cancelar el turno');
      }

      alert('Turno cancelado exitosamente.');
      router.push('/solicitar-turno');
    } catch (error) {
      console.error('Error al cancelar turno:', error);
      alert(`Ocurrió un error: ${error.message}`);
    }
  }
};

    const enviarCalificacion = async () => {
      try {
        console.log('Iniciando envío de calificación...');
        console.log('Datos a enviar:', {
          turno_id: turno.value.id,
          calificacion: rating.value,
          comentario: comentario.value
        });

        const token = localStorage.getItem('token');
        if (!token) {
          console.warn('No se encontró token - intentando enviar calificación sin autenticación');
          // Permitir enviar calificación sin token como invitado
          // El backend validará si se permite calificación anónima
        }

        const headers = {
          'Content-Type': 'application/json'
        };
        if (token) {
          headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch('/api/turns/calificaciones/crear/', {
          method: 'POST',
          headers: headers,
          body: JSON.stringify({
            turno_id: turno.value.id,
            calificacion: rating.value,
            comentario: comentario.value
          })
        });

        console.log('Respuesta del servidor:', {
          status: response.status,
          ok: response.ok
        });

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          console.error('Error en la respuesta:', errorData);
          throw new Error(errorData.detail || 'Error al enviar calificación');
        }

        const responseData = await response.json();
        console.log('Calificación enviada exitosamente:', responseData);

        showRatingModal.value = false;
        alert('¡Gracias por calificar nuestro servicio!');
        router.push('/solicitar-turno');
      } catch (error) {
        console.error('Error al calificar:', error);
        alert(`Ocurrió un error al enviar tu calificación: ${error.message}`);
      }
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

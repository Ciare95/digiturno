<template>
  <div class="bg-white rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-xl">
    <div class="bg-gradient-to-r from-blue-600 to-indigo-700 px-6 py-4">
      <div class="flex justify-between items-center">
        <div>
          <h2 class="text-xl font-bold text-white">Turnos en Espera</h2>
          <p class="text-blue-100 text-sm">Lista de turnos pendientes por atender</p>
        </div>
        <div class="flex items-center space-x-2">
          <div class="bg-white/20 rounded-full px-3 py-1 text-sm font-medium text-white">
            <span class="inline-flex items-center">
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Tiempo estimado: {{ tiempoTotal }} min
            </span>
          </div>
          <div class="bg-white/20 rounded-full px-3 py-1 text-sm font-medium text-white">
            {{ turnosEnEspera.length }} {{ turnosEnEspera.length === 1 ? 'turno' : 'turnos' }}
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="turnosEnEspera.length === 0" class="p-6 text-center">
      <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-blue-50 text-blue-500 mb-3">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <h3 class="text-lg font-medium text-gray-700 mb-1">No hay turnos en espera</h3>
      <p class="text-gray-500">Los turnos solicitados aparecerán aquí</p>
    </div>
    
    <ul v-else class="divide-y divide-gray-100">
      <li v-for="(turno, index) in turnosEnEspera" :key="turno.id" 
          class="p-4 hover:bg-gray-50 transition-colors duration-150 group"
          :class="{ 'bg-blue-50': index % 2 === 0 }">
        <div class="flex justify-between items-start">
          <!-- Información del turno -->
          <div class="flex-1 min-w-0">
            <div class="flex items-start space-x-3">
              <div class="flex-shrink-0">
                <div class="w-12 h-12 rounded-lg flex items-center justify-center" 
                     :class="getServicioInfo(turno.servicio).color + ' bg-opacity-10'">
                  <component :is="getServicioInfo(turno.servicio).icono" 
                           class="h-6 w-6" 
                           :class="getServicioInfo(turno.servicio).color" />
                </div>
              </div>
              <div class="min-w-0 flex-1">
                <div class="flex items-center">
                  <p class="text-base font-semibold text-gray-900 truncate">
                    {{ turno.nombre }}
                  </p>
                  <span class="ml-2 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium"
                        :class="getServicioClase(turno.servicio)">
                    {{ turno.servicio | formatoServicio }}
                  </span>
                </div>
                <p class="mt-1 text-sm text-gray-500">
                  <span class="font-medium">Documento:</span> {{ turno.documento }}
                </p>
                <p class="mt-1 text-sm text-gray-500">
                  <span class="font-medium">Solicitado:</span> {{ turno.horaSolicitud | formatoHora }}
                </p>
                <div class="mt-2 flex items-center text-sm text-gray-500">
                  <svg class="h-4 w-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span>Tiempo estimado: {{ tiemposServicio[turno.servicio] || 5 }} min</span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Código del turno -->
          <div class="ml-4 flex-shrink-0 text-center">
            <div class="bg-gray-50 group-hover:bg-white rounded-lg p-2 transition-colors">
              <span class="text-xs font-medium text-gray-500 block">Tu turno es</span>
              <span class="text-2xl font-bold text-blue-600 block">{{ turno.codigo }}</span>
              <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium mt-1"
                    :class="getServicioClase(turno.servicio) + ' bg-opacity-20'"
                    :style="{ color: getServicioInfo(turno.servicio).color }">
                #{{ index + 1 }} en cola
              </span>
            </div>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useTurnosStore } from '@/store/turnos';

// Tiempos estimados por servicio (en minutos)
const tiemposServicio = {
  'caja': 5,
  'asesoria': 20,
  'pagos': 8,
  'informacion': 5
};

const props = defineProps({
  servicios: {
    type: Array,
    required: true
  }
});

const turnosStore = useTurnosStore();

const turnosEnEspera = computed(() => {
  return [...turnosStore.turnosEnEspera].sort((a, b) => 
    new Date(a.horaSolicitud) - new Date(b.horaSolicitud)
  );
});

// Calcular el tiempo total de espera estimado
const tiempoTotal = computed(() => {
  return turnosEnEspera.value.reduce((total, turno) => {
    return total + (tiemposServicio[turno.servicio] || 5); // 5 minutos por defecto
  }, 0);
});

// Obtener la información del servicio para un turno
const getServicioInfo = (servicioId) => {
  return props.servicios.find(s => s.id === servicioId) || { nombre: servicioId, color: 'bg-gray-500' };
};

const getServicioClase = (servicio) => {
  const clases = {
    'caja': 'bg-green-100 text-green-800',
    'asesoria': 'bg-purple-100 text-purple-800',
    'pagos': 'bg-amber-100 text-amber-800'
  };
  return clases[servicio] || 'bg-gray-100 text-gray-800';
};

// Filtros
const filters = {
  formatoServicio(servicioId) {
    const servicios = {
      'caja': 'Caja',
      'asesoria': 'Asesoría',
      'pagos': 'Pagos'
    };
    return servicios[servicioId] || servicioId;
  },
  
  formatoHora(fechaString) {
    const fecha = new Date(fechaString);
    return fecha.toLocaleTimeString('es-ES', { 
      hour: '2-digit', 
      minute: '2-digit',
      hour12: true 
    });
  }
};

// Aplicar filtros
defineExpose({
  filters
});
</script>

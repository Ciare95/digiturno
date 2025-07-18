<template>
  <div class="bg-white rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-xl">
    <form @submit.prevent="solicitarTurno" class="space-y-6">
      <!-- Selector de Sucursal -->
      <div class="px-6 pt-6">
        <label class="block text-sm font-medium text-gray-700 mb-1">Selecciona una sucursal</label>
        <div class="relative">
          <select 
            v-model="turnoData.sucursalId" 
            @change="seleccionarSucursal"
            required
            class="block w-full pl-4 pr-10 py-3 text-base border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-lg appearance-none bg-white"
            :class="{ 'text-gray-500': !turnoData.sucursalId }"
          >
            <option value="" disabled selected>Selecciona una sucursal</option>
            <option 
              v-for="sucursal in sucursales" 
              :key="sucursal.id" 
              :value="sucursal.id"
              class="text-gray-900"
            >
              {{ sucursal.nombre }}
            </option>
          </select>
          <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
          </div>
        </div>
      </div>

      <!-- Selector de Servicio -->
      <div class="px-6" :class="{ 'opacity-50': !turnoData.sucursalId }">
        <label class="block text-sm font-medium text-gray-700 mb-1">Selecciona un servicio</label>
        <div class="relative">
          <select 
            v-model="turnoData.servicio" 
            :disabled="!turnoData.sucursalId"
            required
            class="block w-full pl-4 pr-10 py-3 text-base border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-lg appearance-none bg-white"
            :class="{ 'text-gray-500': !turnoData.servicio }"
          >
            <option value="" disabled selected>Selecciona un servicio</option>
            <option 
              v-for="servicio in serviciosDisponibles" 
              :key="servicio.id" 
              :value="servicio.id"
              class="text-gray-900"
            >
              {{ servicio.nombre }}
            </option>
          </select>
          <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
          </div>
        </div>
      </div>

      <!-- Información del Servicio Seleccionado -->
      <div v-if="servicioSeleccionado" class="px-6">
        <div class="bg-blue-50 border-l-4 border-blue-500 p-4 rounded-r-lg">
          <div class="flex">
            <div class="flex-shrink-0">
              <div class="p-2 rounded-lg" :class="servicioSeleccionado.color + ' bg-opacity-20'">
                <component :is="servicioSeleccionado.icono" class="h-5 w-5" :class="servicioSeleccionado.color" />
              </div>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-blue-800">
                {{ servicioSeleccionado.nombre }}
              </h3>
              <div class="mt-1 text-sm text-blue-700">
                <p>{{ servicioSeleccionado.descripcion }}</p>
                <p class="mt-1">
                  <span class="font-medium">Tiempo estimado:</span> {{ servicioSeleccionado.tiempo }}
                  <span class="mx-2">•</span>
                  <span class="font-medium">Documentos:</span> {{ servicioSeleccionado.documentos }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Campos del formulario -->
      <div class="px-6 space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Nombre Completo</label>
          <input 
            v-model="turnoData.nombre" 
            type="text" 
            required
            class="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            placeholder="Ingrese su nombre completo"
          >
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Número de Documento</label>
          <input 
            v-model="turnoData.documento" 
            type="text" 
            required
            class="block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            placeholder="Ingrese su número de documento"
          >
        </div>
      </div>
      
      <!-- Botón de envío -->
      <div class="px-6 pb-6">
        <button 
          type="submit" 
          class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="!turnoData.nombre || !turnoData.documento || !turnoData.servicio || !turnoData.sucursalId"
        >
          Solicitar Turno
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, watch, defineProps, defineEmits } from 'vue';
import { useTurnosStore } from '@/store/turnos';

const props = defineProps({
  sucursales: {
    type: Array,
    required: true
  },
  servicios: {
    type: Array,
    required: true
  }
});

const emit = defineEmits(['update:sucursal', 'update:servicio', 'turno-solicitado']);

const turnosStore = useTurnosStore();

const turnoData = ref({
  sucursalId: '',
  servicio: '',
  nombre: '',
  documento: ''
});

// Filtrar servicios disponibles según la sucursal seleccionada
const serviciosDisponibles = computed(() => {
  if (!turnoData.value.sucursalId) return [];
  const sucursalSeleccionada = props.sucursales.find(s => s.id === turnoData.value.sucursalId);
  if (!sucursalSeleccionada) return [];
  return props.servicios.filter(servicio => 
    sucursalSeleccionada.servicios.includes(servicio.id)
  );
});

// Obtener el objeto completo del servicio seleccionado
const servicioSeleccionado = computed(() => {
  return props.servicios.find(s => s.id === turnoData.value.servicio) || null;
});

// Manejar selección de sucursal
const seleccionarSucursal = () => {
  // Limpiar servicio cuando cambia la sucursal
  turnoData.value.servicio = '';
  emit('update:sucursal', turnoData.value.sucursalId);
};

// Observar cambios en el servicio seleccionado
watch(() => turnoData.value.servicio, (nuevoValor) => {
  if (nuevoValor) {
    emit('update:servicio', nuevoValor);
  }
});

// Solicitar turno
const solicitarTurno = async () => {
  try {
    if (!turnoData.value.sucursalId || !turnoData.value.servicio || !turnoData.value.nombre || !turnoData.value.documento) {
      throw new Error('Por favor complete todos los campos requeridos');
    }

    // Obtener la sucursal seleccionada
    const sucursal = props.sucursales.find(s => s.id === turnoData.value.sucursalId);
    
    // Crear el objeto de turno
    const nuevoTurno = {
      ...turnoData.value,
      sucursal: sucursal.nombre,
      horaSolicitud: new Date().toISOString(),
      estado: 'pendiente',
      codigo: generarCodigoTurno()
    };

    // Enviar al store
    await turnosStore.agregarTurno(nuevoTurno);
    
    // Emitir evento con los datos del turno generado
    emit('turno-solicitado', nuevoTurno);
    
    // Limpiar el formulario
    turnoData.value.servicio = '';
    turnoData.value.nombre = '';
    turnoData.value.documento = '';
  } catch (error) {
    console.error('Error al solicitar turno:', error);
    alert(error.message || 'Ocurrió un error al solicitar el turno. Por favor, intente nuevamente.');
  }
};

// Generar un código de turno único (ej: C-001)
const generarCodigoTurno = () => {
  const letraServicio = turnoData.value.sucursalId.charAt(0).toUpperCase();
  const numero = Math.floor(Math.random() * 1000).toString().padStart(3, '0');
  return `${letraServicio}-${numero}`;
};
</script>

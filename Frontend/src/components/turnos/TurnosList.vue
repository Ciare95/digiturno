<template>
  <div class="bg-white p-6 rounded-lg shadow-md">
    <h2 class="text-xl font-semibold mb-4">Turnos en Espera</h2>
    <div v-if="turnosEnEspera.length === 0" class="text-gray-500 text-center py-4">
      No hay turnos en espera
    </div>
    <ul class="space-y-3">
      <li v-for="turno in turnosEnEspera" :key="turno.id" 
          class="border-b pb-2 last:border-b-0">
        <div class="flex justify-between items-center">
          <div>
            <span class="font-medium">{{ turno.servicio | formatoServicio }}</span>
            <p class="text-sm text-gray-600">{{ turno.nombre }} - {{ turno.documento }}</p>
          </div>
          <span class="text-2xl font-bold text-blue-600">{{ turno.codigo }}</span>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useTurnosStore } from '@/store/turnos';

const turnosStore = useTurnosStore();

const turnosEnEspera = computed(() => turnosStore.turnosEnEspera);

// Filtros
const filters = {
  formatoServicio(servicioId) {
    const servicios = {
      'caja': 'Caja',
      'asesoria': 'Asesoría',
      'pagos': 'Pagos'
    };
    return servicios[servicioId] || servicioId;
  }
};

// Aplicar filtros
defineExpose({
  filters
});
</script>

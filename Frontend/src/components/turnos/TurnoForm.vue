<template>
  <div class="bg-white p-6 rounded-lg shadow-md">
    <h2 class="text-xl font-semibold mb-4">Solicitar Turno</h2>
    <form @submit.prevent="solicitarTurno" class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700">Tipo de Servicio</label>
        <select v-model="turnoData.servicio" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
          <option value="">Seleccione un servicio</option>
          <option v-for="servicio in servicios" :key="servicio.id" :value="servicio.id">
            {{ servicio.nombre }}
          </option>
        </select>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700">Nombre</label>
        <input v-model="turnoData.nombre" type="text" required
               class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700">Documento de Identidad</label>
        <input v-model="turnoData.documento" type="text" required
               class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
      </div>
      <button type="submit"
              class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors">
        Solicitar Turno
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useTurnosStore } from '@/store/turnos';

const turnosStore = useTurnosStore();

const turnoData = ref({
  servicio: '',
  nombre: '',
  documento: ''
});

const servicios = [
  { id: 'caja', nombre: 'Caja' },
  { id: 'asesoria', nombre: 'Asesoría' },
  { id: 'pagos', nombre: 'Pagos' }
];

const solicitarTurno = async () => {
  try {
    await turnosStore.solicitarTurno(turnoData.value);
    turnoData.value = { servicio: '', nombre: '', documento: '' };
    alert('Turno solicitado exitosamente');
  } catch (error) {
    console.error('Error al solicitar turno:', error);
    alert('Ocurrió un error al solicitar el turno');
  }
};
</script>

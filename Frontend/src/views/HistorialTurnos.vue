<template>
    <div class="max-w-5xl mx-auto px-4 py-6">
        <h1 class="text-2xl font-bold mb-6 text-blue-700">Historial de Turnos</h1>

        <div v-if="loading" class="text-gray-500">Cargando historial...</div>
        <div v-else-if="turnos.length === 0" class="text-gray-500">No hay turnos registrados.</div>

        <div v-else class="space-y-4">
            <div v-for="turno in turnos" :key="turno.id" class="bg-white shadow rounded-lg p-4 border border-gray-200">
                <div class="flex flex-col sm:flex-row sm:justify-between">
                    <div>
                        <p class="text-lg font-semibold text-gray-800">{{ turno.nombre_cliente }}</p>
                        <p class="text-sm text-gray-600">Cédula: {{ turno.numero_cedula }}</p>
                    </div>
                    <div class="text-right">
                        <p class="text-sm text-gray-600">Fecha: {{ formatFecha(turno.fecha_creacion) }}</p>
                        <p class="text-sm font-medium text-green-600">{{ turno.estado }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'

const turnos = ref([])
const loading = ref(true)

const formatFecha = (fechaIso) => {
    const fecha = new Date(fechaIso)
    return fecha.toLocaleDateString() + ' ' + fecha.toLocaleTimeString()
}

const fetchTurnos = async () => {
    try {
        const response = await axios.get('/api/turnos/historial/')
        turnos.value = response.data
    } catch (error) {
        console.error('Error al cargar turnos:', error)
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    fetchTurnos()
})
</script>

<style scoped>
/* Puedes agregar estilos personalizados si deseas */
</style>
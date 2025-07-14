<template>
  <div class="min-h-screen flex flex-col bg-gradient-to-br from-gray-50 to-blue-50">
    <!-- Header -->
    <AppHeader />

    <!-- Contenido Principal -->
    <main class="flex-grow flex items-center justify-center py-12 px-4">
      <div class="w-full max-w-4xl">
        <!-- Tarjeta Principal -->
        <div class="bg-white rounded-2xl shadow-xl overflow-hidden">
          <!-- Encabezado -->
          <div class="bg-gradient-to-r from-blue-600 to-indigo-700 px-8 py-6 text-center">
            <h1 class="text-3xl font-bold text-white">Solicita tu Turno</h1>
            <p class="text-blue-100 mt-2">Selecciona tu sucursal y servicio</p>
          </div>
          
          <!-- Contenido -->
          <div class="p-8">
            <!-- Selector de Sucursal y Servicio -->
            <TurnoForm 
              :sucursales="sucursales" 
              :servicios="servicios" 
              class="max-w-2xl mx-auto"
              @update:sucursal="seleccionarSucursal"
              @update:servicio="seleccionarServicio"
            />
            
            <!-- Información de la Sucursal -->
            <div v-if="sucursalSeleccionada" class="mt-8 bg-blue-50 rounded-xl p-6">
              <h3 class="text-lg font-semibold text-gray-800 mb-3">Información de la Sucursal</h3>
              <div class="grid md:grid-cols-2 gap-6">
                <div>
                  <h4 class="font-medium text-gray-700">Dirección</h4>
                  <p class="text-gray-600 mt-1">{{ sucursalSeleccionada.direccion }}</p>
                  <div class="mt-3 flex items-start">
                    <svg class="h-5 w-5 text-blue-500 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    </svg>
                    <div>
                      <p class="text-sm text-gray-500">{{ sucursalSeleccionada.ubicacion }}</p>
                      <a :href="'https://maps.google.com/?q=' + encodeURIComponent(sucursalSeleccionada.direccion)" 
                         target="_blank" 
                         class="text-blue-600 hover:text-blue-800 text-sm font-medium mt-1 inline-flex items-center">
                        Ver en mapa
                        <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
                        </svg>
                      </a>
                    </div>
                  </div>
                </div>
                <div>
                  <h4 class="font-medium text-gray-700">Horario de Atención</h4>
                  <ul class="mt-1 space-y-1">
                    <li v-for="(horario, dia) in sucursalSeleccionada.horario" :key="dia" class="flex justify-between">
                      <span class="text-gray-600">{{ dia }}:</span>
                      <span class="font-medium">{{ horario }}</span>
                    </li>
                  </ul>
                  <div class="mt-3 flex items-start">
                    <svg class="h-5 w-5 text-blue-500 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <div>
                      <p class="text-sm text-gray-500">Tiempo de espera estimado: {{ tiempoEsperaEstimado }} min</p>
                      <p class="text-sm text-gray-500">Personas en espera: {{ personasEnEspera }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Información del Servicio -->
            <div v-if="servicioSeleccionado" class="mt-6 bg-blue-50 rounded-xl p-6">
              <h3 class="text-lg font-semibold text-gray-800 mb-3">Detalles del Servicio</h3>
              <div class="flex items-start">
                <div class="p-3 rounded-lg mr-4" :class="servicioSeleccionado.color + ' bg-opacity-10'">
                  <component :is="servicioSeleccionado.icono" class="h-6 w-6" :class="servicioSeleccionado.color" />
                </div>
                <div>
                  <h4 class="text-lg font-medium text-gray-900">{{ servicioSeleccionado.nombre }}</h4>
                  <p class="text-gray-600 mt-1">{{ servicioSeleccionado.descripcion }}</p>
                  <div class="mt-3 grid grid-cols-2 gap-4">
                    <div>
                      <p class="text-sm text-gray-500">Tiempo estimado</p>
                      <p class="font-medium">{{ servicioSeleccionado.tiempo }}</p>
                    </div>
                    <div>
                      <p class="text-sm text-gray-500">Documentos requeridos</p>
                      <p class="font-medium">{{ servicioSeleccionado.documentos }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Turnos en Espera -->
        <div v-if="sucursalSeleccionada" class="mt-8">
          <h2 class="text-2xl font-bold text-gray-800 mb-4">Turnos en Espera</h2>
          <TurnosList :servicios="servicios" class="max-w-2xl mx-auto" />
        </div>
      </div>
    </main>

    <!-- Footer -->
    <AppFooter />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useTurnosStore } from '@/store/turnos';
import AppHeader from '@/components/layout/AppHeader.vue';
import AppFooter from '@/components/layout/AppFooter.vue';
import TurnoForm from '@/components/turnos/TurnoForm.vue';
import TurnosList from '@/components/turnos/TurnosList.vue';

// Datos de las sucursales
const sucursales = [
  {
    id: 'centro',
    nombre: 'Sucursal Centro',
    direccion: 'Av. Principal #123, Colonia Centro',
    ubicacion: 'Entre Calle Juárez y Calle Hidalgo',
    horario: {
      'Lunes a Viernes': '9:00 AM - 6:00 PM',
      'Sábado': '9:00 AM - 2:00 PM',
      'Domingo': 'Cerrado'
    },
    telefono: '555-123-4567',
    servicios: ['caja', 'asesoria', 'pagos', 'informacion']
  },
  {
    id: 'norte',
    nombre: 'Sucursal Norte',
    direccion: 'Blvd. Las Américas #456, Col. Del Valle',
    ubicacion: 'Cerca del Parque Central',
    horario: {
      'Lunes a Viernes': '8:30 AM - 5:30 PM',
      'Sábado': '9:00 AM - 1:00 PM',
      'Domingo': 'Cerrado'
    },
    telefono: '555-987-6543',
    servicios: ['caja', 'pagos', 'informacion']
  },
  {
    id: 'sur',
    nombre: 'Sucursal Sur',
    direccion: 'Calle Revolución #789, Col. Moderna',
    ubicacion: 'Frente a Plaza Galerías',
    horario: {
      'Lunes a Sábado': '10:00 AM - 7:00 PM',
      'Domingo': '10:00 AM - 2:00 PM'
    },
    telefono: '555-456-7890',
    servicios: ['caja', 'asesoria', 'pagos', 'informacion']
  }
];

const turnosStore = useTurnosStore();

// Estado reactivo
const sucursalSeleccionada = ref(null);
const servicioSeleccionado = ref(null);

// Datos de los servicios
const servicios = [
  {
    id: 'caja',
    nombre: 'Atención en Caja',
    descripcion: 'Realiza pagos, depósitos y consulta de saldos',
    tiempo: '5-10 min',
    documentos: 'INE y comprobante de pago',
    color: 'bg-green-500',
    icono: {
      template: `
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
        </svg>
      `
    }
  },
  {
    id: 'asesoria',
    nombre: 'Asesoría Personalizada',
    descripcion: 'Atención personalizada para resolver dudas sobre nuestros servicios',
    tiempo: '15-20 min',
    documentos: 'INE y documentación relacionada',
    color: 'bg-purple-500',
    icono: {
      template: `
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      `
    }
  },
  {
    id: 'pagos',
    nombre: 'Pagos de Servicios',
    descripcion: 'Realiza el pago de servicios como luz, agua, teléfono, etc.',
    tiempo: '5-8 min',
    documentos: 'Recibo del servicio a pagar',
    color: 'bg-amber-500',
    icono: {
      template: `
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
        </svg>
      `
    }
  },
  {
    id: 'informacion',
    nombre: 'Información General',
    descripcion: 'Solicita información sobre trámites y requisitos',
    tiempo: '3-5 min',
    documentos: 'Ninguno',
    color: 'bg-blue-500',
    icono: {
      template: `
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      `
    }
  }
];

// Filtra los servicios disponibles según la sucursal seleccionada
const serviciosDisponibles = computed(() => {
  if (!sucursalSeleccionada.value) return [];
  return servicios.filter(servicio => 
    sucursalSeleccionada.value.servicios.includes(servicio.id)
  );
});

// Actualiza el servicio seleccionado cuando cambia la sucursal
watch(sucursalSeleccionada, (nuevaSucursal) => {
  if (nuevaSucursal) {
    // Si el servicio actual no está disponible en la nueva sucursal, lo limpiamos
    if (servicioSeleccionado.value && !nuevaSucursal.servicios.includes(servicioSeleccionado.value.id)) {
      servicioSeleccionado.value = null;
    }
  } else {
    servicioSeleccionado.value = null;
  }
});

// Métodos para manejar la selección
const seleccionarSucursal = (sucursalId) => {
  sucursalSeleccionada.value = sucursales.find(s => s.id === sucursalId) || null;
};

const seleccionarServicio = (servicioId) => {
  servicioSeleccionado.value = servicios.find(s => s.id === servicioId) || null;
};

// Datos simulados para el tiempo de espera
const tiempoEsperaEstimado = computed(() => {
  if (!sucursalSeleccionada.value) return 0;
  // Simulamos un tiempo de espera basado en la cantidad de turnos
  const turnosSucursal = turnosStore.turnosEnEspera.filter(t => t.sucursalId === sucursalSeleccionada.value.id);
  return turnosSucursal.length * 5; // 5 minutos por turno
});

const personasEnEspera = computed(() => {
  if (!sucursalSeleccionada.value) return 0;
  return turnosStore.turnosEnEspera.filter(t => t.sucursalId === sucursalSeleccionada.value.id).length;
});

// Íconos para las estadísticas
const ClockIcon = {
  template: `
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  `
};

const UserGroupIcon = {
  template: `
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
    </svg>
  `
};

const CheckCircleIcon = {
  template: `
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  `
};

// Estadísticas
const estadisticas = computed(() => [
  {
    label: 'Turnos en Espera',
    value: turnosStore.turnosEnEspera.length,
    icon: ClockIcon,
    bgColor: 'bg-blue-500',
    trend: 'up'
  },
  {
    label: 'Turnos Atendidos Hoy',
    value: turnosStore.turnosAtendidos.length,
    icon: CheckCircleIcon,
    bgColor: 'bg-green-500',
    trend: 'up'
  },
  {
    label: 'Clientes en Espera',
    value: new Set(turnosStore.turnosEnEspera.map(t => t.documento)).size,
    icon: UserGroupIcon,
    bgColor: 'bg-purple-500',
    trend: 'up'
  }
]);
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
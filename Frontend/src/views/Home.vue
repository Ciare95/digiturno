<template>
  <div class="min-h-screen flex flex-col bg-gradient-to-br from-gray-50 to-blue-50">
    <!-- Header -->
    <AppHeader />

    <!-- Contenido Principal -->
    <main class="flex-grow py-12 px-4">
      <div class="max-w-7xl mx-auto">
        <!-- Encabezado -->
        <div class="text-center mb-12">
          <h1 class="text-4xl font-bold text-gray-900 mb-2">Sistema de Turnos</h1>
          <p class="text-xl text-gray-600">Solicita tu turno de forma rápida y sencilla</p>
        </div>

        <div class="grid lg:grid-cols-3 gap-8">
          <!-- Columna del formulario -->
          <div class="lg:col-span-2">
            <div class="flex flex-col lg:flex-row gap-6">
              <!-- Formulario de turno -->  
              <div class="flex-1 bg-white rounded-2xl shadow-xl overflow-hidden">
                <div class="bg-gradient-to-r from-blue-600 to-indigo-700 px-8 py-6">
                  <h2 class="text-2xl font-bold text-white">Solicita tu Turno</h2>
                  <p class="text-blue-100 mt-1">Completa el formulario para reservar tu turno</p>
                </div>
                
                <div class="p-6">
                  <TurnoForm 
                    :sucursales="sucursales" 
                    :servicios="servicios" 
                    @update:sucursal="seleccionarSucursal"
                    @update:servicio="seleccionarServicio"
                    @turno-solicitado="mostrarAlertaTurno"
                  />
                </div>
              </div>

              <!-- Tarjeta de turno generado -->
              <div v-if="ultimoTurno" class="lg:w-80 flex-shrink-0">
                <div class="bg-white rounded-2xl shadow-xl overflow-hidden h-full">
                  <div class="bg-gradient-to-r from-green-600 to-green-700 px-6 py-4">
                    <h2 class="text-xl font-bold text-white">Tu Turno</h2>
                  </div>
                  
                  <div class="p-6 text-center">
                    <div class="mb-6">
                      <p class="text-sm font-medium text-gray-500">Número de turno</p>
                      <div class="mt-2 bg-green-50 rounded-lg p-4">
                        <span class="text-4xl font-bold text-green-600">{{ ultimoTurno.codigo }}</span>
                      </div>
                    </div>
                    
                    <div class="space-y-4 text-left">
                      <div>
                        <p class="text-sm font-medium text-gray-500">Servicio</p>
                        <p class="font-medium">
                          {{ servicios.find(s => s.id === ultimoTurno.servicio)?.nombre || ultimoTurno.servicio }}
                        </p>
                      </div>
                      
                      <div>
                        <p class="text-sm font-medium text-gray-500">Sucursal</p>
                        <p class="font-medium">{{ ultimoTurno.sucursal }}</p>
                      </div>
                      
                      <div>
                        <p class="text-sm font-medium text-gray-500">Tiempo de espera</p>
                        <p class="font-medium">
                          <span class="text-blue-600">{{ calcularTiempoEspera(ultimoTurno) }} minutos</span>
                        </p>
                      </div>
                      
                      <div class="pt-4 mt-4 border-t border-gray-100">
                        <p class="text-sm text-gray-500">
                          <svg class="h-5 w-5 inline-block mr-1 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                          </svg>
                          Hora de solicitud: {{ new Date(ultimoTurno.horaSolicitud).toLocaleTimeString() }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Sección de turnos en espera -->
            <div v-if="sucursalSeleccionada" class="mt-8 bg-white rounded-2xl shadow-xl overflow-hidden">
              <div class="bg-gray-50 px-6 py-4 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-800">Turnos en Espera</h3>
              </div>
              <div class="p-6">
                <TurnosList :servicios="servicios" />
              </div>
            </div>
          </div>

          <!-- Columna de información -->
          <div class="space-y-6">
            <!-- Mensaje de confirmación -->
            <div v-if="ultimoTurno" class="mt-4">
              <div class="bg-blue-50 border-l-4 border-blue-500 p-4 rounded-lg">
                <div class="flex">
                  <div class="flex-shrink-0">
                    <svg class="h-5 w-5 text-blue-500" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                    </svg>
                  </div>
                  <div class="ml-3">
                    <p class="text-sm font-medium text-blue-800">¡Turno generado con éxito!</p>
                    <p class="text-sm text-blue-700 mt-1">Tu turno ha sido registrado correctamente.</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Información de la Sucursal -->
            <div v-if="sucursalSeleccionada" class="bg-white rounded-2xl shadow-xl overflow-hidden">
              <div class="bg-gray-50 px-6 py-4 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-800">Información de la Sucursal</h3>
              </div>
              <div class="p-6 space-y-4">
                <div>
                  <h4 class="text-sm font-medium text-gray-500">Sucursal</h4>
                  <p class="mt-1 text-gray-900 font-medium">{{ sucursalSeleccionada.nombre }}</p>
                </div>
                
                <div>
                  <h4 class="text-sm font-medium text-gray-500">Dirección</h4>
                  <p class="mt-1 text-gray-900">{{ sucursalSeleccionada.direccion }}</p>
                  <p class="text-sm text-gray-500">{{ sucursalSeleccionada.ubicacion }}</p>
                  <a :href="'https://maps.google.com/?q=' + encodeURIComponent(sucursalSeleccionada.direccion)" 
                     target="_blank" 
                     class="mt-2 inline-flex items-center text-sm font-medium text-blue-600 hover:text-blue-800">
                    Ver en mapa
                    <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
                    </svg>
                  </a>
                </div>
                
                <div>
                  <h4 class="text-sm font-medium text-gray-500">Horario de Atención</h4>
                  <ul class="mt-1 space-y-1">
                    <li v-for="(horario, dia) in sucursalSeleccionada.horario" :key="dia" class="flex justify-between">
                      <span class="text-gray-600">{{ dia }}:</span>
                      <span class="font-medium text-gray-900">{{ horario }}</span>
                    </li>
                  </ul>
                </div>
                
                <div class="pt-4 border-t border-gray-200">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 bg-blue-100 p-2 rounded-lg">
                      <svg class="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                    </div>
                    <div class="ml-3">
                      <p class="text-sm font-medium text-gray-900">Tiempo de espera estimado</p>
                      <p class="text-2xl font-bold text-blue-600">{{ tiempoEsperaEstimado }} min</p>
                      <p class="text-sm text-gray-500">{{ personasEnEspera }} personas en espera</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Información del Servicio -->
            <div v-if="servicioSeleccionado" class="bg-white rounded-2xl shadow-xl overflow-hidden">
              <div class="bg-gray-50 px-6 py-4 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-800">Detalles del Servicio</h3>
              </div>
              <div class="p-6">
                <div class="flex items-start">
                  <div class="p-3 rounded-lg mr-4" :class="servicioSeleccionado.color + ' bg-opacity-10'">
                    <component :is="servicioSeleccionado.icono" class="h-6 w-6" :class="servicioSeleccionado.color" />
                  </div>
                  <div class="flex-1">
                    <h4 class="text-lg font-semibold text-gray-900">{{ servicioSeleccionado.nombre }}</h4>
                    <p class="mt-1 text-gray-600">{{ servicioSeleccionado.descripcion }}</p>
                    
                    <div class="mt-4 space-y-3">
                      <div class="flex items-start">
                        <svg class="h-5 w-5 text-gray-400 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                        <div>
                          <p class="text-sm font-medium text-gray-500">Tiempo estimado</p>
                          <p class="text-gray-900">{{ servicioSeleccionado.tiempo }}</p>
                        </div>
                      </div>
                      
                      <div class="flex items-start">
                        <svg class="h-5 w-5 text-gray-400 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                        </svg>
                        <div>
                          <p class="text-sm font-medium text-gray-500">Documentos requeridos</p>
                          <p class="text-gray-900">{{ servicioSeleccionado.documentos }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
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
const ultimoTurno = ref(null);

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

// Mostrar alerta cuando se genera un nuevo turno
const mostrarAlertaTurno = (nuevoTurno) => {
  ultimoTurno.value = nuevoTurno;
  
  // Ocultar la alerta después de 10 segundos
  setTimeout(() => {
    ultimoTurno.value = null;
  }, 10000);
};

// Calcular tiempo de espera estimado para el turno
const calcularTiempoEspera = (turno) => {
  if (!turno || !sucursalSeleccionada.value) return 0;
  
  const turnosEnEspera = turnosStore.turnosEnEspera.filter(t => 
    t.sucursalId === sucursalSeleccionada.value.id && 
    t.servicio === turno.servicio
  );
  
  // Encontrar la posición del turno actual
  const posicion = turnosEnEspera.findIndex(t => t.id === turno.id);
  
  if (posicion === -1) return 0;
  
  // Calcular tiempo estimado (5 minutos por turno por delante)
  return (posicion + 1) * 5;
};

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
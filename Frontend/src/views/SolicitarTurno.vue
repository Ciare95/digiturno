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
            <div class="lg:col-span-3">
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
  import { obtenerSucursales } from '@/services/Sucursales';


  const sucursales = ref([]);
  
  async function obtenerData() {
    try {
        sucursales.value = await obtenerSucursales();
    } catch (error) {
        sucursales.value = [];
        console.error('Error al obtener sucursales:', error);
    }
  }

  obtenerData();
  
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
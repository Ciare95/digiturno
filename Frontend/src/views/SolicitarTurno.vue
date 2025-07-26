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
  
          <div class="max-w-4xl mx-auto">
            <!-- Formulario de turno -->  
            <div class="bg-white rounded-2xl shadow-xl overflow-hidden">
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
            </div>
        </div>
      </main>
  
      <!-- Footer -->
      <AppFooter />
    </div>
  </template>
  
  <script setup>
  import { ref, computed, watch } from 'vue';
  import { useRouter } from 'vue-router';
  import { useTurnosStore } from '@/store/turnos';
  import AppHeader from '@/components/layout/AppHeader.vue';
  import AppFooter from '@/components/layout/AppFooter.vue';
  import TurnoForm from '@/components/turnos/TurnoForm.vue';
  import { obtenerSucursales } from '@/services/Sucursales';
  import { obtenerServicios } from '@/services/Servicios';


  const sucursales = ref([]);
  const servicios = ref([]);
  
  async function obtenerData() {
    try {
        sucursales.value = await obtenerSucursales();
        servicios.value = await obtenerServicios();
    } catch (error) {
        sucursales.value = [];
        servicios.value = [];
        console.error('Error al obtener sucursales:', error);
    }
  }

  obtenerData();
  
  const router = useRouter();
  const turnosStore = useTurnosStore();
  
  // Estado reactivo
  const sucursalSeleccionada = ref(null);
  const servicioSeleccionado = ref(null);
  
  // Filtra los servicios disponibles según la sucursal seleccionada
  const serviciosDisponibles = computed(() => {
    if (!sucursalSeleccionada.value) return [];
    return servicios.value.filter(servicio => 
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
    sucursalSeleccionada.value = sucursales.value.find(s => s.id === sucursalId) || null;
  };
  
  const seleccionarServicio = (servicioId) => {
    servicioSeleccionado.value = servicios.value.find(s => s.id === servicioId) || null;
  };
  

  
  // Redirigir a la vista del turno generado
  const mostrarAlertaTurno = (nuevoTurno) => {
    // Guardar el turno en localStorage como respaldo
    localStorage.setItem('ultimoTurno', JSON.stringify(nuevoTurno));
    
    // Redirigir a la vista del turno generado
    router.push({
      name: 'turno-generado',
      params: { turno: JSON.stringify(nuevoTurno) }
    });
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
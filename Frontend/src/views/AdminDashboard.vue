<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Barra de navegación -->
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <div class="flex-shrink-0 flex items-center">
              <div class="flex items-center
              ">
                <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <span class="ml-2 text-xl font-bold text-gray-800">DigiTurno</span>
              </div>
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <router-link to="/" class="border-b-2 border-b border-blue-500 text-gray-900 inline-flex items-center px-1 pt-1 text-sm font-medium">
                Panel Principal
              </router-link>
            </div>
          </div>
          <div class="hidden sm:ml-6 sm:flex sm:items-center">
            <button @click="cerrarSesion" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
              Cerrar Sesión
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Contenido principal -->
    <div class="py-10">
      <header>
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 class="text-3xl font-bold text-gray-900">Panel de Administración</h1>
        </div>
      </header>
      <main>
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
          <!-- Pestañas -->
          <div class="border-b border-gray-200">
            <nav class="-mb-px flex space-x-8">
              <button 
                v-for="tab in tabs" 
                :key="tab.name"
                @click="currentTab = tab.name"
                :class="[
                  currentTab === tab.name
                    ? 'border-b border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                  'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm'
                ]"
              >
                {{ tab.label }}
              </button>
            </nav>
          </div>

          <!-- Contenido de las pestañas -->
          <div class="mt-6">
            <!-- Gestión de Servicios -->
            <div v-if="currentTab === 'servicios'" class="bg-white shadow overflow-hidden sm:rounded-lg">
              <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
                <div>
                  <h3 class="text-lg leading-6 font-medium text-gray-900">Servicios</h3>
                  <p class="mt-1 max-w-2xl text-sm text-gray-500">Gestiona los servicios ofrecidos</p>
                </div>
                <button @click="abrirModalNuevoServicio" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                  Nuevo Servicio
                </button>
              </div>
              <div class="border-t border-gray-200">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                    <tr>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Nombre
                      </th>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Descripción
                      </th>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Duración
                      </th>
                      <th scope="col" class="relative px-6 py-3">
                        <span class="sr-only">Acciones</span>
                      </th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="servicio in servicios" :key="servicio.id">
                      <td class="px-6 py-4 whitespace-nowrap">
                        <div class="flex items-center">
                          <div class="flex-shrink-0 h-10 w-10 bg-blue-100 rounded-md flex items-center justify-center">
                            <component :is="servicio.icono" class="h-5 w-5 text-blue-600" />
                          </div>
                          <div class="ml-4">
                            <div class="text-sm font-medium text-gray-900">{{ servicio.nombre }}</div>
                          </div>
                        </div>
                      </td>
                      <td class="px-6 py-4">
                        <div class="text-sm text-gray-500">{{ servicio.descripcion }}</div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                          {{ servicio.duracion }} min
                        </span>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <button @click="editarServicio(servicio)" class="text-blue-600 hover:text-blue-900 mr-3">Editar</button>
                        <button @click="eliminarServicio(servicio.id)" class="text-red-600 hover:text-red-900">Eliminar</button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Gestión de Sucursales -->
            <div v-else-if="currentTab === 'sucursales'" class="bg-white shadow overflow-hidden sm:rounded-lg">
              <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
                <div>
                  <h3 class="text-lg leading-6 font-medium text-gray-900">Sucursales</h3>
                  <p class="mt-1 max-w-2xl text-sm text-gray-500">Gestiona las sucursales disponibles</p>
                </div>
                <button @click="abrirModalNuevaSucursal" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                  Nueva Sucursal
                </button>
              </div>
              <div class="border-t border-gray-200">
                <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 p-6">
                  <div v-for="sucursal in sucursales" :key="sucursal.id" class="bg-white overflow-hidden shadow rounded-lg border border-gray-200">
                    <div class="p-5">
                      <div class="flex items-center">
                        <div class="flex-shrink-0 bg-blue-500 rounded-md p-3">
                          <svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                          </svg>
                        </div>
                        <div class="ml-5 w-0 flex-1">
                          <dl>
                            <dt class="text-sm font-medium text-gray-500 truncate">
                              {{ sucursal.nombre }}
                            </dt>
                            <dd class="flex items-baseline">
                              <div class="text-2xl font-semibold text-gray-900">
                                {{ sucursal.direccion }}
                              </div>
                            </dd>
                          </dl>
                        </div>
                      </div>
                      <div class="mt-4 flex space-x-3">
                        <button @click="editarSucursal(sucursal)" class="inline-flex items-center px-3 py-1.5 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                          Editar
                        </button>
                        <button @click="eliminarSucursal(sucursal.id)" class="inline-flex items-center px-3 py-1.5 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
                          Eliminar
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- Modal de Servicio -->
    <div v-if="mostrarModalServicio" class="fixed z-10 inset-0 overflow-y-auto">
      <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 transition-opacity" aria-hidden="true">
          <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
        </div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                  {{ esNuevoServicio ? 'Nuevo Servicio' : 'Editar Servicio' }}
                </h3>
                <div class="mt-5">
                  <div class="mb-4">
                    <label for="nombreServicio" class="block text-sm font-medium text-gray-700">Nombre</label>
                    <input type="text" v-model="servicioActual.nombre" id="nombreServicio" class="mt-1 focus:ring-blue-500 focus:border focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                  </div>
                  <div class="mb-4">
                    <label for="descripcionServicio" class="block text-sm font-medium text-gray-700">Descripción</label>
                    <textarea v-model="servicioActual.descripcion" id="descripcionServicio" rows="3" class="shadow-sm focus:ring-blue-500 focus:border focus:border-blue-500 mt-1 block w-full sm:text-sm border border-gray-300 rounded-md"></textarea>
                  </div>
                  <div class="mb-4">
                    <label for="duracionServicio" class="block text-sm font-medium text-gray-700">Duración (minutos)</label>
                    <input type="number" v-model.number="servicioActual.duracion" id="duracionServicio" class="mt-1 focus:ring-blue-500 focus:border focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button @click="guardarServicio" type="button" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm">
              Guardar
            </button>
            <button @click="cerrarModalServicio" type="button" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
              Cancelar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ClockIcon, UserIcon, DocumentTextIcon, ShoppingBagIcon } from '@heroicons/vue/24/outline';

export default {
  name: 'AdminDashboard',
  components: {
    ClockIcon,
    UserIcon,
    DocumentTextIcon,
    ShoppingBagIcon
  },
  setup() {
    const router = useRouter();
    const currentTab = ref('servicios');
    const mostrarModalServicio = ref(false);
    const esNuevoServicio = ref(true);
    const servicioActual = ref({
      id: null,
      nombre: '',
      descripcion: '',
      duracion: 30,
      icono: 'DocumentTextIcon'
    });

    const tabs = [
      { name: 'servicios', label: 'Servicios' },
      { name: 'sucursales', label: 'Sucursales' }
    ];

    // Datos de ejemplo
    const servicios = ref([
      {
        id: 1,
        nombre: 'Atención al Cliente',
        descripcion: 'Atención personalizada para consultas generales',
        duracion: 15,
        icono: 'UserIcon'
      },
      {
        id: 2,
        nombre: 'Pagos',
        descripcion: 'Pago de facturas y servicios',
        duracion: 10,
        icono: 'ShoppingBagIcon'
      },
      {
        id: 3,
        nombre: 'Asesoría Legal',
        descripcion: 'Asesoría legal especializada',
        duracion: 30,
        icono: 'DocumentTextIcon'
      }
    ]);

    const sucursales = ref([
      {
        id: 1,
        nombre: 'Sucursal Centro',
        direccion: 'Av. Principal #123',
        horario: 'Lun-Vie 9:00 - 18:00'
      },
      {
        id: 2,
        nombre: 'Sucursal Norte',
        direccion: 'Calle Norte #456',
        horario: 'Lun-Vie 8:00 - 17:00'
      }
    ]);

    const abrirModalNuevoServicio = () => {
      servicioActual.value = {
        id: null,
        nombre: '',
        descripcion: '',
        duracion: 30,
        icono: 'DocumentTextIcon'
      };
      esNuevoServicio.value = true;
      mostrarModalServicio.value = true;
    };

    const abrirModalNuevaSucursal = () => {
      // Implementar lógica para nueva sucursal
      alert('Función de nueva sucursal se implementará aquí');
    };

    const editarServicio = (servicio) => {
      servicioActual.value = { ...servicio };
      esNuevoServicio.value = false;
      mostrarModalServicio.value = true;
    };

    const editarSucursal = (sucursal) => {
      // Implementar lógica para editar sucursal
      alert(`Editando sucursal: ${sucursal.nombre}`);
    };

    const eliminarServicio = (id) => {
      if (confirm('¿Estás seguro de eliminar este servicio?')) {
        servicios.value = servicios.value.filter(s => s.id !== id);
      }
    };

    const eliminarSucursal = (id) => {
      if (confirm('¿Estás seguro de eliminar esta sucursal?')) {
        sucursales.value = sucursales.value.filter(s => s.id !== id);
      }
    };

    const guardarServicio = () => {
      if (esNuevoServicio.value) {
        // Agregar nuevo servicio
        const nuevoId = Math.max(...servicios.value.map(s => s.id), 0) + 1;
        servicios.value.push({
          ...servicioActual.value,
          id: nuevoId
        });
      } else {
        // Actualizar servicio existente
        const index = servicios.value.findIndex(s => s.id === servicioActual.value.id);
        if (index !== -1) {
          servicios.value[index] = { ...servicioActual.value };
        }
      }
      cerrarModalServicio();
    };

    const cerrarModalServicio = () => {
      mostrarModalServicio.value = false;
    };

    const cerrarSesion = () => {
      // Eliminar token de autenticación (simulado)
      localStorage.removeItem('token');
      // Redirigir al login
      router.push('/login');
    };

    return {
      currentTab,
      tabs,
      servicios,
      sucursales,
      mostrarModalServicio,
      servicioActual,
      esNuevoServicio,
      abrirModalNuevoServicio,
      abrirModalNuevaSucursal,
      editarServicio,
      editarSucursal,
      eliminarServicio,
      eliminarSucursal,
      guardarServicio,
      cerrarModalServicio,
      cerrarSesion
    };
  }
};
</script>

<style>
/* Estilos específicos del panel de administración */
/* Transiciones suaves para los modales */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

/* Estilos para las tarjetas de sucursales */
.sucursal-card {
  transition: all 0.2s ease-in-out;
}

.sucursal-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
</style>

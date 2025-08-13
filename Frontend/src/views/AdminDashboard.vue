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
              <router-link to="/" class="border-b-2 border-blue-500 text-gray-900 inline-flex items-center px-1 pt-1 text-sm font-medium">
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
                          <div class="ml-4">
                            <div class="text-sm font-medium text-gray-900">{{ servicio.nombre }}</div>
                          </div>
                        </div>
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

    <!-- Modal simplificado para nuevo servicio -->
    <div v-if="showModalServicio" class="fixed z-50 top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-full max-w-md">
      <div class="bg-white rounded-lg shadow-xl p-6">
          <div>
            <div class="mt-3 text-center sm:mt-5">
              <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                Nuevo Servicio
              </h3>
              <div class="mt-2">
                <div class="space-y-4">
                  <div>
                    <label for="nombre" class="block text-sm font-medium text-gray-700 text-left">Nombre del servicio</label>
                    <input type="text" v-model="nuevoServicio.nombre" id="nombre" class="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                  </div>
                  <div>
                    <label for="codigo" class="block text-sm font-medium text-gray-700 text-left">Código del servicio</label>
                    <input type="text" v-model="nuevoServicio.codigo_servicio" id="codigo" class="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                  </div>
                  <div>
                    <label for="sucursal" class="block text-sm font-medium text-gray-700 text-left">Sucursal</label>
                    <select v-model="nuevoServicio.sucursal" id="sucursal" class="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                      <option v-for="sucursal in sucursales" :key="sucursal.id" :value="sucursal.id">
                        {{ sucursal.nombre }}
                      </option>
                    </select>
                  </div>
                  <div>
                    <label for="duracion" class="block text-sm font-medium text-gray-700 text-left">Duración (minutos)</label>
                    <input type="number" v-model="nuevoServicio.duracion" id="duracion" class="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
            <button type="button" @click="crearServicio" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:col-start-2 sm:text-sm">
              Crear Servicio
            </button>
            <button type="button" @click="cerrarModalServicio" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:col-start-1 sm:text-sm">
              Cancelar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal para editar servicio -->
    <div v-if="showEditModalServicio" class="fixed z-50 top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-full max-w-md">
      <div class="bg-white rounded-lg shadow-xl p-6">
          <div>
            <div class="mt-3 text-center sm:mt-5">
              <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                Editar Servicio
              </h3>
              <div class="mt-2">
                <div class="space-y-4">
                  <div>
                    <label for="edit-nombre" class="block text-sm font-medium text-gray-700 text-left">Nombre del servicio</label>
                    <input type="text" v-model="servicioEditando.nombre" id="edit-nombre" class="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                  </div>
                  <div>
                    <label for="edit-codigo" class="block text-sm font-medium text-gray-700 text-left">Código del servicio</label>
                    <input type="text" v-model="servicioEditando.codigo_servicio" id="edit-codigo" class="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                  </div>
                  <div>
                    <label for="edit-sucursal" class="block text-sm font-medium text-gray-700 text-left">Sucursal</label>
                    <select v-model="servicioEditando.sucursal" id="edit-sucursal" class="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                      <option v-for="sucursal in sucursales" :key="sucursal.id" :value="sucursal.id">
                        {{ sucursal.nombre }}
                      </option>
                    </select>
                  </div>
                  <div>
                    <label for="edit-duracion" class="block text-sm font-medium text-gray-700 text-left">Duración (minutos)</label>
                    <input type="number" v-model="servicioEditando.duracion" id="edit-duracion" class="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
            <button type="button" @click="actualizarServicio" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:col-start-2 sm:text-sm">
              Guardar Cambios
            </button>
            <button type="button" @click="showEditModalServicio = false" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:col-start-1 sm:text-sm">
              Cancelar
            </button>
          </div>
        </div>
      </div>
 
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ClockIcon, UserIcon, DocumentTextIcon, ShoppingBagIcon } from '@heroicons/vue/24/outline';
import axios from 'axios';

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

    const tabs = [
      { name: 'servicios', label: 'Servicios' },
      { name: 'sucursales', label: 'Sucursales' }
    ];

    // Datos de ejemplo
    const servicios = ref([]);

    const sucursales = ref([]);

    const showModalServicio = ref(false);
    const showEditModalServicio = ref(false);
    const nuevoServicio = ref({
      nombre: '',
      codigo_servicio: '',
      sucursal: null,
      duracion: 30
    });
    const servicioEditando = ref({
      id: null,
      nombre: '',
      codigo_servicio: '',
      sucursal: null,
      duracion: 30
    });

    const abrirModalNuevoServicio = () => {
      console.log('Intentando abrir modal...');
      showModalServicio.value = true;
      console.log('Modal abierto:', showModalServicio.value);
    };

    const cerrarModalServicio = () => {
      console.log('Cerrando modal...');
      showModalServicio.value = false;
      nuevoServicio.value = {
        nombre: '',
        duracion: 30
      };
    };

    const crearServicio = async () => {
      try {
        const payload = {
          nombre: nuevoServicio.value.nombre,
          codigo_servicio: nuevoServicio.value.codigo_servicio,
          sucursal: nuevoServicio.value.sucursal,
          tiempo_estimado_atencion: nuevoServicio.value.duracion
        };
        
        console.log('Request payload:', payload);
        
        const response = await axios.post('/api/admin/servicios/', payload, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          }
        });
        
        servicios.value.push({
          id: response.data.id,
          nombre: response.data.nombre,
          duracion: response.data.tiempo_estimado_atencion
        });
        
        cerrarModalServicio();
      } catch (error) {
        console.error('Error creando servicio:', error);
        if (error.response) {
          console.error('Error details:', error.response.data);
          alert(`Error al crear el servicio: ${JSON.stringify(error.response.data)}`);
        } else {
          alert('Error al crear el servicio');
        }
      }
    };

    const abrirModalNuevaSucursal = () => {
      // Implementar lógica para nueva sucursal
      alert('Función de nueva sucursal se implementará aquí');
    };

    const editarServicio = (servicio) => {
      servicioEditando.value = {
        id: servicio.id,
        nombre: servicio.nombre,
        codigo_servicio: servicio.codigo_servicio || '',
        sucursal: servicio.sucursal,
        duracion: servicio.duracion
      };
      showEditModalServicio.value = true;
    };

    const actualizarServicio = async () => {
      try {
        const payload = {
          nombre: servicioEditando.value.nombre,
          codigo_servicio: servicioEditando.value.codigo_servicio,
          sucursal: servicioEditando.value.sucursal,
          tiempo_estimado_atencion: servicioEditando.value.duracion
        };
        
        const response = await axios.put(`/api/admin/servicios/${servicioEditando.value.id}/`, payload, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          }
        });
        
        const index = servicios.value.findIndex(s => s.id === servicioEditando.value.id);
        if (index !== -1) {
          servicios.value[index] = {
            id: servicioEditando.value.id,
            nombre: response.data.nombre,
            duracion: response.data.tiempo_estimado_atencion
          };
        }
        
        showEditModalServicio.value = false;
      } catch (error) {
        console.error('Error actualizando servicio:', error);
        if (error.response) {
          console.error('Error details:', error.response.data);
          alert(`Error al actualizar el servicio: ${JSON.stringify(error.response.data)}`);
        } else {
          alert('Error al actualizar el servicio');
        }
      }
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

    const getServicios = async () => {
      try {
        const response = await axios.get('/api/admin/servicios/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        servicios.value = response.data.results.map(servicio => ({
          id: servicio.id,
          nombre: servicio.nombre,
          duracion: servicio.tiempo_estimado_atencion,
        }));
      } catch (error) {
        console.error('Error fetching services:', error);
      }
    };

    const getSucursales = async () => {
      try {
        const response = await axios.get('/api/admin/sucursales/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        sucursales.value = response.data.results;
      } catch (error) {
        console.error('Error fetching branches:', error);
      }
    };

    onMounted(() => {
      getServicios();
      getSucursales();
    });

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
      abrirModalNuevoServicio,
      abrirModalNuevaSucursal,
      editarServicio,
      editarSucursal,
      eliminarServicio,
      eliminarSucursal,
      cerrarSesion,
      showModalServicio,
      showEditModalServicio,
      nuevoServicio,
      servicioEditando,
      cerrarModalServicio,
      crearServicio,
      actualizarServicio
    };
  }
};
</script>

<style>

</style>

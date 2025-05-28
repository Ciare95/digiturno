<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-800 mb-6">Panel de Usuario</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
      <!-- Tarjeta de Bienvenida -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-3">Bienvenido, {{ nombreUsuario }}</h2>
        <p class="text-gray-600 mb-4">
          Desde este panel podrás gestionar tus turnos y acceder a todas las funcionalidades del sistema.
        </p>
      </div>
      
      <!-- Tarjeta de Turnos Activos -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex justify-between items-center mb-3">
          <h2 class="text-xl font-semibold">Turnos Activos</h2>
          <span class="bg-blue-100 text-blue-800 font-medium px-3 py-1 rounded-full text-sm">
            {{ turnosActivos.length }}
          </span>
        </div>
        
        <div v-if="cargando" class="flex justify-center py-4">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
        
        <div v-else-if="turnosActivos.length === 0" class="text-gray-500 text-center py-4">
          No tienes turnos activos
        </div>
        
        <div v-else class="space-y-3">
          <div v-for="turno in turnosActivos" :key="turno.id" class="border-b border-gray-100 pb-3 last:border-b-0 last:pb-0">
            <div class="font-medium">{{ turno.numero_turno }} - {{ turno.servicio.nombre }}</div>
            <div class="text-sm text-gray-600">{{ turno.sucursal.nombre }}</div>
            <div class="flex justify-between items-center mt-1">
              <span :class="obtenerClaseEstadoTurno(turno.estado)" class="px-2 py-1 rounded-md text-xs font-medium">
                {{ obtenerTextoEstadoTurno(turno.estado) }}
              </span>
              <span class="text-xs text-gray-500">
                {{ formatearFecha(turno.fecha_creacion) }}
              </span>
            </div>
          </div>
        </div>
        
        <div class="mt-4 text-center">
          <router-link to="/usuario/turnos" class="text-blue-600 hover:text-blue-800 text-sm font-medium">
            Ver todos los turnos
          </router-link>
        </div>
      </div>
      
      <!-- Tarjeta de Nuevo Turno -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-3">Solicitar Nuevo Turno</h2>
        <p class="text-gray-600 mb-4">
          Solicita un nuevo turno para cualquiera de nuestros servicios disponibles.
        </p>
        <button @click="mostrarModalNuevoTurno = true" class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition-colors w-full">
          Solicitar Turno
        </button>
      </div>
    </div>
    
    <!-- Sección de Sucursales -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 class="text-xl font-semibold mb-4">Sucursales Disponibles</h2>
      
      <div v-if="cargando" class="flex justify-center py-4">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
      
      <div v-else-if="sucursales.length === 0" class="text-gray-500 text-center py-4">
        No hay sucursales disponibles
      </div>
      
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="sucursal in sucursales" :key="sucursal.id" class="border border-gray-200 rounded-md p-4 hover:border-blue-500 transition-colors cursor-pointer" @click="seleccionarSucursal(sucursal)">
          <h3 class="font-medium text-lg">{{ sucursal.nombre }}</h3>
          <div class="text-sm text-gray-600 mt-1">{{ sucursal.direccion }}</div>
          <div class="text-sm text-gray-600">{{ sucursal.ciudad }}, {{ sucursal.departamento }}</div>
          <div class="mt-2 flex justify-between items-center">
            <span :class="sucursal.activa ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'" class="px-2 py-1 rounded-md text-xs font-medium">
              {{ sucursal.activa ? 'Activa' : 'Inactiva' }}
            </span>
            <button @click.stop="verServicios(sucursal)" class="text-blue-600 hover:text-blue-800 text-sm font-medium">
              Ver servicios
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Modal de Nuevo Turno (simplificado) -->
    <div v-if="mostrarModalNuevoTurno" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full">
        <div class="p-4 border-b border-gray-200">
          <h3 class="text-lg font-semibold">Solicitar Nuevo Turno</h3>
        </div>
        
        <div class="p-6">
          <form @submit.prevent="crearTurno">
            <!-- Campos del formulario -->
            <div class="mb-4">
              <label class="block text-gray-700 font-medium mb-2">Sucursal</label>
              <select v-model="nuevoTurno.sucursal_id" class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                <option value="" disabled>Selecciona una sucursal</option>
                <option v-for="sucursal in sucursales" :key="sucursal.id" :value="sucursal.id">
                  {{ sucursal.nombre }}
                </option>
              </select>
            </div>
            
            <div class="mb-4">
              <label class="block text-gray-700 font-medium mb-2">Servicio</label>
              <select v-model="nuevoTurno.servicio_id" class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                <option value="" disabled>Selecciona un servicio</option>
                <option v-for="servicio in serviciosFiltrados" :key="servicio.id" :value="servicio.id">
                  {{ servicio.nombre }}
                </option>
              </select>
            </div>
            
            <div class="mb-4">
              <label class="block text-gray-700 font-medium mb-2">Observaciones</label>
              <textarea v-model="nuevoTurno.observaciones" class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" rows="3"></textarea>
            </div>
          </form>
        </div>
        
        <div class="p-4 border-t border-gray-200 flex justify-end space-x-3">
          <button @click="mostrarModalNuevoTurno = false" class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition-colors">
            Cancelar
          </button>
          <button @click="crearTurno" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors" :disabled="cargando">
            Solicitar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';

export default {
  name: 'PanelUsuario',
  setup() {
    const tienda = useStore();
    
    // Estado
    const mostrarModalNuevoTurno = ref(false);
    const nuevoTurno = ref({
      sucursal_id: '',
      servicio_id: '',
      observaciones: ''
    });
    
    // Computadas
    const usuario = computed(() => tienda.state.usuario);
    const nombreUsuario = computed(() => {
      return usuario.value ? `${usuario.value.first_name} ${usuario.value.last_name}` : '';
    });
    const cargando = computed(() => tienda.state.cargando);
    const error = computed(() => tienda.state.error);
    const sucursales = computed(() => tienda.state.sucursales);
    const servicios = computed(() => tienda.state.servicios);
    const turnos = computed(() => tienda.state.turnos);
    
    const turnosActivos = computed(() => {
      return turnos.value.filter(turno => 
        ['en_espera', 'llamado', 'en_atencion'].includes(turno.estado)
      );
    });
    
    const serviciosFiltrados = computed(() => {
      if (!nuevoTurno.value.sucursal_id) return [];
      return servicios.value.filter(servicio => 
        servicio.sucursal.id === nuevoTurno.value.sucursal_id
      );
    });
    
    // Métodos
    const cargarDatos = async () => {
      try {
        await tienda.dispatch('cargarSucursales');
        await tienda.dispatch('cargarTurnosUsuario');
      } catch (error) {
        console.error('Error al cargar datos:', error);
      }
    };
    
    const seleccionarSucursal = (sucursal) => {
      nuevoTurno.value.sucursal_id = sucursal.id;
      tienda.dispatch('cargarServicios', sucursal.id);
      mostrarModalNuevoTurno.value = true;
    };
    
    const verServicios = async (sucursal) => {
      try {
        await tienda.dispatch('cargarServicios', sucursal.id);
        // Aquí podrías mostrar un modal con los servicios
      } catch (error) {
        console.error('Error al cargar servicios:', error);
      }
    };
    
    const crearTurno = async () => {
      try {
        await tienda.dispatch('crearTurno', {
          servicio: nuevoTurno.value.servicio_id,
          sucursal: nuevoTurno.value.sucursal_id,
          observaciones: nuevoTurno.value.observaciones
        });
        
        // Limpiar formulario y cerrar modal
        nuevoTurno.value = {
          sucursal_id: '',
          servicio_id: '',
          observaciones: ''
        };
        mostrarModalNuevoTurno.value = false;
        
        // Recargar turnos
        await tienda.dispatch('cargarTurnosUsuario');
      } catch (error) {
        console.error('Error al crear turno:', error);
      }
    };
    
    const obtenerClaseEstadoTurno = (estado) => {
      const clases = {
        'en_espera': 'bg-yellow-100 text-yellow-800',
        'llamado': 'bg-blue-100 text-blue-800',
        'en_atencion': 'bg-green-100 text-green-800',
        'finalizado': 'bg-gray-100 text-gray-800',
        'cancelado': 'bg-red-100 text-red-800',
        'ausente': 'bg-orange-100 text-orange-800',
        'transferido': 'bg-purple-100 text-purple-800'
      };
      
      return clases[estado] || 'bg-gray-100 text-gray-800';
    };
    
    const obtenerTextoEstadoTurno = (estado) => {
      const textos = {
        'en_espera': 'En espera',
        'llamado': 'Llamado',
        'en_atencion': 'En atención',
        'finalizado': 'Finalizado',
        'cancelado': 'Cancelado',
        'ausente': 'Ausente',
        'transferido': 'Transferido'
      };
      
      return textos[estado] || estado;
    };
    
    const formatearFecha = (fecha) => {
      if (!fecha) return '';
      const fechaObj = new Date(fecha);
      return fechaObj.toLocaleString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    };
    
    // Ciclo de vida
    onMounted(() => {
      cargarDatos();
    });
    
    return {
      usuario,
      nombreUsuario,
      cargando,
      error,
      sucursales,
      servicios,
      turnos,
      turnosActivos,
      serviciosFiltrados,
      mostrarModalNuevoTurno,
      nuevoTurno,
      seleccionarSucursal,
      verServicios,
      crearTurno,
      obtenerClaseEstadoTurno,
      obtenerTextoEstadoTurno,
      formatearFecha
    };
  }
}
</script>

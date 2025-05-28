<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-800 mb-6">Panel de Administrador</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
      <!-- Tarjeta de Bienvenida -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-3">Bienvenido, {{ nombreAdministrador }}</h2>
        <p class="text-gray-600 mb-4">
          Desde este panel podrás administrar todos los aspectos del sistema DigiTurno.
        </p>
        <div class="flex items-center space-x-2 text-sm">
          <span class="bg-purple-100 text-purple-800 px-2 py-1 rounded-full text-xs font-medium">
            Administrador
          </span>
          <span>{{ sucursalActual }}</span>
        </div>
      </div>
      
      <!-- Tarjeta de Estadísticas Generales -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-3">Estadísticas Generales</h2>
        
        <div v-if="cargando" class="flex justify-center py-4">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
        
        <div v-else class="space-y-4">
          <div class="flex items-center justify-between">
            <span class="text-gray-600">Turnos hoy:</span>
            <span class="bg-blue-100 text-blue-800 font-medium px-3 py-1 rounded-full text-sm">
              {{ estadisticasGenerales.turnosHoy || 0 }}
            </span>
          </div>
          
          <div class="flex items-center justify-between">
            <span class="text-gray-600">Tiempo promedio:</span>
            <span class="bg-green-100 text-green-800 font-medium px-3 py-1 rounded-full text-sm">
              {{ estadisticasGenerales.tiempoPromedio || '0 min' }}
            </span>
          </div>
          
          <div class="flex items-center justify-between">
            <span class="text-gray-600">Satisfacción:</span>
            <span class="bg-yellow-100 text-yellow-800 font-medium px-3 py-1 rounded-full text-sm flex items-center">
              <span>{{ estadisticasGenerales.satisfaccion || '0%' }}</span>
            </span>
          </div>
          
          <div class="mt-4 text-center">
            <router-link to="/admin/estadisticas" class="text-blue-600 hover:text-blue-800 text-sm font-medium">
              Ver estadísticas detalladas
            </router-link>
          </div>
        </div>
      </div>
      
      <!-- Tarjeta de Alertas -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex justify-between items-center mb-3">
          <h2 class="text-xl font-semibold">Alertas del Sistema</h2>
          <span class="bg-red-100 text-red-800 font-medium px-3 py-1 rounded-full text-sm">
            {{ alertas.length }}
          </span>
        </div>
        
        <div v-if="cargando" class="flex justify-center py-4">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
        
        <div v-else-if="alertas.length === 0" class="text-gray-500 text-center py-4">
          No hay alertas pendientes
        </div>
        
        <div v-else class="space-y-3">
          <div v-for="alerta in alertas" :key="alerta.id" class="border-b border-gray-100 pb-3 last:border-b-0 last:pb-0">
            <div class="font-medium">{{ alerta.titulo }}</div>
            <div class="text-sm text-gray-600">{{ alerta.mensaje }}</div>
            <div class="flex justify-between items-center mt-1">
              <span :class="obtenerClaseAlerta(alerta.tipo)" class="px-2 py-1 rounded-md text-xs font-medium">
                {{ alerta.tipo }}
              </span>
              <span class="text-xs text-gray-500">
                {{ formatearFecha(alerta.fecha) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Sección de Accesos Rápidos -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 class="text-xl font-semibold mb-4">Accesos Rápidos</h2>
      
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <router-link to="/admin/usuarios" class="flex flex-col items-center justify-center p-4 border border-gray-200 rounded-lg hover:bg-blue-50 hover:border-blue-300 transition-colors">
          <div class="text-blue-600 text-3xl mb-2">
            <i class="fas fa-users"></i>
          </div>
          <span class="text-gray-800 font-medium">Usuarios</span>
        </router-link>
        
        <router-link to="/admin/empleados" class="flex flex-col items-center justify-center p-4 border border-gray-200 rounded-lg hover:bg-blue-50 hover:border-blue-300 transition-colors">
          <div class="text-blue-600 text-3xl mb-2">
            <i class="fas fa-user-tie"></i>
          </div>
          <span class="text-gray-800 font-medium">Empleados</span>
        </router-link>
        
        <router-link to="/admin/sucursales" class="flex flex-col items-center justify-center p-4 border border-gray-200 rounded-lg hover:bg-blue-50 hover:border-blue-300 transition-colors">
          <div class="text-blue-600 text-3xl mb-2">
            <i class="fas fa-building"></i>
          </div>
          <span class="text-gray-800 font-medium">Sucursales</span>
        </router-link>
        
        <router-link to="/admin/servicios" class="flex flex-col items-center justify-center p-4 border border-gray-200 rounded-lg hover:bg-blue-50 hover:border-blue-300 transition-colors">
          <div class="text-blue-600 text-3xl mb-2">
            <i class="fas fa-concierge-bell"></i>
          </div>
          <span class="text-gray-800 font-medium">Servicios</span>
        </router-link>
      </div>
    </div>
    
    <!-- Sección de Actividad Reciente -->
    <div class="bg-white rounded-lg shadow-md p-6">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">Actividad Reciente</h2>
        <button @click="cargarActividad" class="text-blue-600 hover:text-blue-800 text-sm font-medium">
          Actualizar
        </button>
      </div>
      
      <div v-if="cargando" class="flex justify-center py-4">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
      
      <div v-else-if="actividades.length === 0" class="text-center py-6 text-gray-500">
        No hay actividades recientes
      </div>
      
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Usuario</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acción</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Detalles</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="actividad in actividades" :key="actividad.id">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatearFecha(actividad.fecha) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="font-medium text-gray-900">{{ actividad.usuario }}</div>
                <div class="text-xs text-gray-500">{{ actividad.rol }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="obtenerClaseActividad(actividad.tipo)" class="px-2 py-1 rounded-md text-xs font-medium">
                  {{ actividad.tipo }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ actividad.detalles }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';

export default {
  name: 'PanelAdmin',
  setup() {
    const tienda = useStore();
    
    // Estado
    const alertas = ref([
      {
        id: 1,
        titulo: 'Tiempo de espera excesivo',
        mensaje: 'La sucursal Central tiene tiempos de espera superiores a 30 minutos',
        tipo: 'advertencia',
        fecha: new Date(new Date().setHours(new Date().getHours() - 2))
      },
      {
        id: 2,
        titulo: 'Empleado desconectado',
        mensaje: 'El empleado Juan Pérez lleva más de 15 minutos desconectado',
        tipo: 'error',
        fecha: new Date(new Date().setHours(new Date().getHours() - 1))
      },
      {
        id: 3,
        titulo: 'Actualización disponible',
        mensaje: 'Hay una nueva actualización del sistema disponible (v2.1.0)',
        tipo: 'info',
        fecha: new Date()
      }
    ]);
    
    const actividades = ref([
      {
        id: 1,
        fecha: new Date(new Date().setMinutes(new Date().getMinutes() - 30)),
        usuario: 'María López',
        rol: 'Administrador',
        tipo: 'creación',
        detalles: 'Creó un nuevo empleado: Carlos Rodríguez'
      },
      {
        id: 2,
        fecha: new Date(new Date().setHours(new Date().getHours() - 1)),
        usuario: 'Juan Pérez',
        rol: 'Empleado',
        tipo: 'modificación',
        detalles: 'Cambió su estado a desconectado'
      },
      {
        id: 3,
        fecha: new Date(new Date().setHours(new Date().getHours() - 2)),
        usuario: 'Ana Gómez',
        rol: 'Administrador',
        tipo: 'eliminación',
        detalles: 'Eliminó el servicio: Consulta Rápida'
      },
      {
        id: 4,
        fecha: new Date(new Date().setHours(new Date().getHours() - 3)),
        usuario: 'Pedro Sánchez',
        rol: 'Empleado',
        tipo: 'transferencia',
        detalles: 'Transfirió el turno A001 al servicio: Atención Prioritaria'
      },
      {
        id: 5,
        fecha: new Date(new Date().setHours(new Date().getHours() - 4)),
        usuario: 'Laura Martínez',
        rol: 'Usuario',
        tipo: 'creación',
        detalles: 'Solicitó un nuevo turno: B023'
      }
    ]);
    
    // Computadas
    const usuario = computed(() => tienda.state.usuario);
    const nombreAdministrador = computed(() => {
      return usuario.value ? `${usuario.value.first_name} ${usuario.value.last_name}` : '';
    });
    const cargando = computed(() => tienda.state.cargando);
    const error = computed(() => tienda.state.error);
    
    const sucursalActual = computed(() => {
      return usuario.value?.perfil_administrador?.sucursal?.nombre || 'Todas las sucursales';
    });
    
    const estadisticasGenerales = computed(() => {
      // Simulamos estadísticas (en una implementación real, esto vendría del backend)
      return {
        turnosHoy: 145,
        tiempoPromedio: '12 min',
        satisfaccion: '87%'
      };
    });
    
    // Métodos
    const cargarDatos = async () => {
      try {
        // Aquí cargaríamos datos reales del backend
        console.log('Cargando datos del panel de administrador...');
      } catch (error) {
        console.error('Error al cargar datos:', error);
      }
    };
    
    const cargarActividad = async () => {
      try {
        // Aquí cargaríamos la actividad reciente del backend
        console.log('Cargando actividad reciente...');
      } catch (error) {
        console.error('Error al cargar actividad:', error);
      }
    };
    
    const obtenerClaseAlerta = (tipo) => {
      const clases = {
        'error': 'bg-red-100 text-red-800',
        'advertencia': 'bg-yellow-100 text-yellow-800',
        'info': 'bg-blue-100 text-blue-800',
        'éxito': 'bg-green-100 text-green-800'
      };
      
      return clases[tipo] || 'bg-gray-100 text-gray-800';
    };
    
    const obtenerClaseActividad = (tipo) => {
      const clases = {
        'creación': 'bg-green-100 text-green-800',
        'modificación': 'bg-blue-100 text-blue-800',
        'eliminación': 'bg-red-100 text-red-800',
        'transferencia': 'bg-purple-100 text-purple-800'
      };
      
      return clases[tipo] || 'bg-gray-100 text-gray-800';
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
      nombreAdministrador,
      cargando,
      error,
      alertas,
      actividades,
      sucursalActual,
      estadisticasGenerales,
      cargarActividad,
      obtenerClaseAlerta,
      obtenerClaseActividad,
      formatearFecha
    };
  }
}
</script>

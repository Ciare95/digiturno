<template>
  <div class="min-h-screen flex flex-col">
    <!-- Barra de navegación superior -->
    <header class="bg-blue-600 text-white shadow-md">
      <nav class="container mx-auto px-4 py-3 flex justify-between items-center">
        <router-link :to="rutaInicio" class="text-xl font-bold">DigiTurno</router-link>
        
        <div class="flex items-center space-x-4">
          <div class="relative" ref="notificacionesMenu">
            <button @click="toggleNotificaciones" class="hover:text-blue-200 transition-colors">
              <span class="sr-only">Notificaciones</span>
              <i class="fas fa-bell"></i>
              <span v-if="notificaciones.length" class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-4 w-4 flex items-center justify-center">
                {{ notificaciones.length }}
              </span>
            </button>
            
            <div v-if="mostrarNotificaciones" class="absolute right-0 mt-2 w-80 bg-white rounded-md shadow-lg z-10 text-gray-800">
              <div class="p-3 border-b border-gray-200">
                <h3 class="font-medium">Notificaciones</h3>
              </div>
              
              <div class="max-h-64 overflow-y-auto">
                <div v-if="notificaciones.length === 0" class="p-4 text-center text-gray-500">
                  No tienes notificaciones
                </div>
                
                <div v-for="notificacion in notificaciones" :key="notificacion.id" class="p-3 border-b border-gray-100 hover:bg-gray-50">
                  <div class="font-medium">{{ notificacion.titulo }}</div>
                  <div class="text-sm text-gray-600">{{ notificacion.mensaje }}</div>
                  <div class="text-xs text-gray-400 mt-1">{{ formatearFecha(notificacion.fecha_envio) }}</div>
                </div>
              </div>
              
              <div v-if="notificaciones.length > 0" class="p-2 text-center">
                <button @click="marcarTodasLeidas" class="text-sm text-blue-600 hover:text-blue-800">
                  Marcar todas como leídas
                </button>
              </div>
            </div>
          </div>
          
          <div class="relative" ref="perfilMenu">
            <button @click="togglePerfilMenu" class="flex items-center space-x-2 hover:text-blue-200 transition-colors">
              <span>{{ nombreUsuario }}</span>
              <i class="fas fa-chevron-down text-xs"></i>
            </button>
            
            <div v-if="mostrarPerfilMenu" class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg z-10 text-gray-800">
              <router-link :to="rutaPerfil" class="block px-4 py-2 hover:bg-gray-100">
                Mi Perfil
              </router-link>
              
              <button @click="cerrarSesion" class="w-full text-left px-4 py-2 hover:bg-gray-100 text-red-600">
                Cerrar Sesión
              </button>
            </div>
          </div>
        </div>
      </nav>
    </header>
    
    <div class="flex-grow flex">
      <!-- Menú lateral -->
      <aside class="w-64 bg-gray-800 text-white">
        <div class="p-4 border-b border-gray-700">
          <div class="font-medium">{{ rolUsuario }}</div>
          <div class="text-sm text-gray-400">{{ usuario.email }}</div>
        </div>
        
        <!-- Menú para Usuario -->
        <nav v-if="esUsuario" class="p-4">
          <router-link to="/usuario" class="block py-2 px-4 rounded hover:bg-gray-700 transition-colors mb-1">
            <i class="fas fa-home mr-2"></i> Panel Principal
          </router-link>
          
          <router-link to="/usuario/turnos" class="block py-2 px-4 rounded hover:bg-gray-700 transition-colors mb-1">
            <i class="fas fa-ticket mr-2"></i> Mis Turnos
          </router-link>
          
          <router-link to="/usuario/perfil" class="block py-2 px-4 rounded hover:bg-gray-700 transition-colors mb-1">
            <i class="fas fa-user mr-2"></i> Mi Perfil
          </router-link>
        </nav>
        
        <!-- Menú para Empleado -->
        <nav v-if="esEmpleado" class="p-4">
          <router-link to="/empleado" class="block py-2 px-4 rounded hover:bg-gray-700 transition-colors mb-1">
            <i class="fas fa-home mr-2"></i> Panel Principal
          </router-link>
          
          <router-link to="/empleado/gestion-turnos" class="block py-2 px-4 rounded hover:bg-gray-700 transition-colors mb-1">
            <i class="fas fa-tasks mr-2"></i> Gestión de Turnos
          </router-link>
          
          <router-link to="/empleado/estadisticas" class="block py-2 px-4 rounded hover:bg-gray-700 transition-colors mb-1">
            <i class="fas fa-chart-bar mr-2"></i> Estadísticas
          </router-link>
        </nav>
        
        <!-- Menú para Administrador -->
        <nav v-if="esAdministrador" class="p-4">
          <router-link to="/admin" class="block py-2 px-4 rounded hover:bg-gray-700 transition-colors mb-1">
            <i class="fas fa-home mr-2"></i> Panel Principal
          </router-link>
          
          <router-link to="/admin/usuarios" class="block py-2 px-4 rounded hover:bg-gray-700 transition-colors mb-1">
            <i class="fas fa-users mr-2"></i> Gestión de Usuarios
          </router-link>
          
          <router-link to="/admin/empleados" class="block py-2 px-4 rounded hover:bg-gray-700 transition-colors mb-1">
            <i class="fas fa-user-tie mr-2"></i> Gestión de Empleados
          </router-link>
          
          <router-link to="/admin/sucursales" class="block py-2 px-4 rounded hover:bg-gray-700 transition-colors mb-1">
            <i class="fas fa-building mr-2"></i> Gestión de Sucursales
          </router-link>
          
          <router-link to="/admin/servicios" class="block py-2 px-4 rounded hover:bg-gray-700 transition-colors mb-1">
            <i class="fas fa-concierge-bell mr-2"></i> Gestión de Servicios
          </router-link>
          
          <router-link to="/admin/estadisticas" class="block py-2 px-4 rounded hover:bg-gray-700 transition-colors mb-1">
            <i class="fas fa-chart-line mr-2"></i> Estadísticas
          </router-link>
          
          <router-link to="/admin/configuracion" class="block py-2 px-4 rounded hover:bg-gray-700 transition-colors mb-1">
            <i class="fas fa-cog mr-2"></i> Configuración
          </router-link>
        </nav>
      </aside>
      
      <!-- Contenido principal -->
      <main class="flex-grow p-6 bg-gray-100">
        <router-view></router-view>
      </main>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapState, mapActions } from 'vuex';
import { onMounted, onUnmounted, ref } from 'vue';


export default {
  name: 'LayoutAutenticado',
  setup() {
    // No usamos router por ahora, pero podríamos necesitarlo en el futuro
    const notificacionesMenu = ref(null);
    const perfilMenu = ref(null);
    const mostrarNotificaciones = ref(false);
    const mostrarPerfilMenu = ref(false);
    
    const toggleNotificaciones = () => {
      mostrarNotificaciones.value = !mostrarNotificaciones.value;
      if (mostrarNotificaciones.value) {
        mostrarPerfilMenu.value = false;
      }
    };
    
    const togglePerfilMenu = () => {
      mostrarPerfilMenu.value = !mostrarPerfilMenu.value;
      if (mostrarPerfilMenu.value) {
        mostrarNotificaciones.value = false;
      }
    };
    
    const cerrarMenusAlHacerClickFuera = (event) => {
      if (notificacionesMenu.value && !notificacionesMenu.value.contains(event.target)) {
        mostrarNotificaciones.value = false;
      }
      
      if (perfilMenu.value && !perfilMenu.value.contains(event.target)) {
        mostrarPerfilMenu.value = false;
      }
    };
    
    onMounted(() => {
      document.addEventListener('click', cerrarMenusAlHacerClickFuera);
    });
    
    onUnmounted(() => {
      document.removeEventListener('click', cerrarMenusAlHacerClickFuera);
    });
    
    return {
      notificacionesMenu,
      perfilMenu,
      mostrarNotificaciones,
      mostrarPerfilMenu,
      toggleNotificaciones,
      togglePerfilMenu
    };
  },
  computed: {
    ...mapState({
      usuario: state => state.usuario,
      notificaciones: state => state.notificaciones
    }),
    ...mapGetters([
      'esUsuario',
      'esEmpleado',
      'esAdministrador'
    ]),
    nombreUsuario() {
      return this.usuario ? `${this.usuario.first_name} ${this.usuario.last_name}` : '';
    },
    rolUsuario() {
      if (this.esAdministrador) return 'Administrador';
      if (this.esEmpleado) return 'Empleado';
      return 'Usuario';
    },
    rutaInicio() {
      if (this.esAdministrador) return '/admin';
      if (this.esEmpleado) return '/empleado';
      return '/usuario';
    },
    rutaPerfil() {
      if (this.esAdministrador) return '/admin/perfil';
      if (this.esEmpleado) return '/empleado/perfil';
      return '/usuario/perfil';
    }
  },
  methods: {
    ...mapActions(['cerrarSesion']),
    formatearFecha(fecha) {
      if (!fecha) return '';
      const fechaObj = new Date(fecha);
      return fechaObj.toLocaleString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    marcarTodasLeidas() {
      // Implementar lógica para marcar todas las notificaciones como leídas
      console.log('Marcar todas como leídas');
    },
    async cerrarSesion() {
      await this.$store.dispatch('cerrarSesion');
      this.$router.push('/iniciar-sesion');
    }
  }
}
</script>

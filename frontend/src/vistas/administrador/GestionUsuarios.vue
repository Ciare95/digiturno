<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6">Gestión de Usuarios</h1>
    
    <!-- Tabla de usuarios -->
    <div class="bg-white rounded-lg shadow-md p-6">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-semibold">Listado de Usuarios</h2>
        <button 
          @click="mostrarFormulario = true" 
          class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          Nuevo Usuario
        </button>
      </div>
      
      <div v-if="cargando" class="flex justify-center py-8">
        <div class="spinner"></div>
      </div>
      
      <div v-else-if="usuarios.length === 0" class="py-8 text-center text-gray-500">
        No hay usuarios registrados.
      </div>
      
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead>
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nombre</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Rol</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="usuario in usuarios" :key="usuario.id">
              <td class="px-6 py-4 whitespace-nowrap">{{ usuario.id }}</td>
              <td class="px-6 py-4 whitespace-nowrap">{{ usuario.nombre }}</td>
              <td class="px-6 py-4 whitespace-nowrap">{{ usuario.email }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span 
                  :class="{
                    'px-2 py-1 text-xs font-semibold rounded-full': true,
                    'bg-gray-100 text-gray-800': usuario.rol === 'usuario',
                    'bg-blue-100 text-blue-800': usuario.rol === 'empleado',
                    'bg-purple-100 text-purple-800': usuario.rol === 'administrador'
                  }"
                >
                  {{ usuario.rol }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span 
                  :class="{
                    'px-2 py-1 text-xs font-semibold rounded-full': true,
                    'bg-green-100 text-green-800': usuario.activo,
                    'bg-red-100 text-red-800': !usuario.activo
                  }"
                >
                  {{ usuario.activo ? 'Activo' : 'Inactivo' }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <button 
                  @click="editarUsuario(usuario)" 
                  class="text-blue-600 hover:text-blue-900 mr-4"
                >
                  Editar
                </button>
                <button 
                  @click="cambiarEstado(usuario)" 
                  class="text-orange-600 hover:text-orange-900 mr-4"
                >
                  {{ usuario.activo ? 'Desactivar' : 'Activar' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GestionUsuarios',
  data() {
    return {
      usuarios: [
        {
          id: 1,
          nombre: 'Juan Pérez',
          email: 'juan@ejemplo.com',
          rol: 'usuario',
          activo: true
        },
        {
          id: 2,
          nombre: 'María García',
          email: 'maria@ejemplo.com',
          rol: 'empleado',
          activo: true
        },
        {
          id: 3,
          nombre: 'Carlos López',
          email: 'carlos@ejemplo.com',
          rol: 'administrador',
          activo: true
        },
        {
          id: 4,
          nombre: 'Ana Martínez',
          email: 'ana@ejemplo.com',
          rol: 'usuario',
          activo: false
        }
      ],
      mostrarFormulario: false,
      usuarioEditando: null,
      cargando: false,
      error: null
    }
  },
  methods: {
    /**
     * Prepara la edición de un usuario
     */
    editarUsuario(usuario) {
      this.usuarioEditando = {...usuario}
      this.mostrarFormulario = true
      console.log('Editando usuario:', usuario)
    },
    
    /**
     * Cambia el estado de un usuario (activo/inactivo)
     */
    cambiarEstado(usuario) {
      // En una aplicación real, aquí se enviaría una petición a la API
      console.log(`Cambiando estado del usuario ${usuario.id} a ${!usuario.activo ? 'activo' : 'inactivo'}`)
      
      // Simulamos el cambio de estado
      const index = this.usuarios.findIndex(u => u.id === usuario.id)
      if (index !== -1) {
        this.usuarios[index] = {
          ...usuario,
          activo: !usuario.activo
        }
      }
    }
  }
}
</script>

<style scoped>
@reference "../../assets/css/main.css";
.spinner {
  @apply w-[2rem] h-[2rem] border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin;
}
</style>

<template>
  <div class="max-w-md mx-auto bg-white rounded-lg shadow-md overflow-hidden">
    <div class="py-4 px-6 bg-blue-600 text-white text-center">
      <h2 class="text-2xl font-bold">Registro de Usuario</h2>
    </div>
    
    <form @submit.prevent="registrarUsuario" class="py-6 px-8">
      <div v-if="error" class="mb-4 p-3 bg-red-100 text-red-700 rounded-md">
        {{ error }}
      </div>
      
      <div class="mb-4">
        <label for="first_name" class="block text-gray-700 font-medium mb-2">Nombre</label>
        <input 
          type="text" 
          id="first_name" 
          v-model="datosUsuario.first_name" 
          class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        >
      </div>
      
      <div class="mb-4">
        <label for="last_name" class="block text-gray-700 font-medium mb-2">Apellido</label>
        <input 
          type="text" 
          id="last_name" 
          v-model="datosUsuario.last_name" 
          class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        >
      </div>
      
      <div class="mb-4">
        <label for="cedula" class="block text-gray-700 font-medium mb-2">Cédula</label>
        <input 
          type="text" 
          id="cedula" 
          v-model="datosUsuario.cedula" 
          class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        >
      </div>
      
      <div class="mb-4">
        <label for="telefono" class="block text-gray-700 font-medium mb-2">Teléfono</label>
        <input 
          type="tel" 
          id="telefono" 
          v-model="datosUsuario.telefono" 
          class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
      </div>
      
      <div class="mb-4">
        <label for="email" class="block text-gray-700 font-medium mb-2">Correo Electrónico</label>
        <input 
          type="email" 
          id="email" 
          v-model="datosUsuario.email" 
          class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        >
      </div>
      
      <div class="mb-4">
        <label for="username" class="block text-gray-700 font-medium mb-2">Nombre de Usuario</label>
        <input 
          type="text" 
          id="username" 
          v-model="datosUsuario.username" 
          class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        >
      </div>
      
      <div class="mb-4">
        <label for="password" class="block text-gray-700 font-medium mb-2">Contraseña</label>
        <input 
          type="password" 
          id="password" 
          v-model="datosUsuario.password" 
          class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        >
      </div>
      
      <div class="mb-6">
        <label for="password_confirmation" class="block text-gray-700 font-medium mb-2">Confirmar Contraseña</label>
        <input 
          type="password" 
          id="password_confirmation" 
          v-model="datosUsuario.password_confirmation" 
          class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        >
      </div>
      
      <div class="mb-6">
        <button 
          type="submit" 
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition-colors"
          :disabled="cargando"
        >
          <span v-if="cargando">Registrando...</span>
          <span v-else>Registrarse</span>
        </button>
      </div>
      
      <div class="text-center text-gray-600">
        ¿Ya tienes una cuenta? 
        <router-link to="/iniciar-sesion" class="text-blue-600 hover:underline">Iniciar Sesión</router-link>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

export default {
  name: 'PaginaRegistro',
  setup() {
    const tienda = useStore();
    const router = useRouter();
    
    const datosUsuario = ref({
      first_name: '',
      last_name: '',
      cedula: '',
      telefono: '',
      email: '',
      username: '',
      password: '',
      password_confirmation: ''
    });
    
    const error = computed(() => tienda.state.error);
    const cargando = computed(() => tienda.state.cargando);
    
    const registrarUsuario = async () => {
      // Validar que las contraseñas coincidan
      if (datosUsuario.value.password !== datosUsuario.value.password_confirmation) {
        tienda.commit('establecerError', 'Las contraseñas no coinciden');
        return;
      }
      
      try {
        await tienda.dispatch('registrarUsuario', datosUsuario.value);
        // Redirigir a la página de inicio de sesión con un mensaje de éxito
        router.push({ 
          name: 'iniciar-sesion',
          params: { 
            mensaje: 'Registro exitoso. Por favor, inicia sesión con tus credenciales.'
          }
        });
      } catch (error) {
        // El error ya se maneja en la acción de Vuex
        console.error('Error al registrar usuario:', error);
      }
    };
    
    return {
      datosUsuario,
      error,
      cargando,
      registrarUsuario
    };
  }
}
</script>

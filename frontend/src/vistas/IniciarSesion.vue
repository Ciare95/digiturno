<template>
  <div class="max-w-md mx-auto bg-white rounded-lg shadow-md overflow-hidden">
    <div class="py-4 px-6 bg-blue-600 text-white text-center">
      <h2 class="text-2xl font-bold">Iniciar Sesión</h2>
    </div>
    
    <form @submit.prevent="iniciarSesion" class="py-6 px-8">
      <div v-if="error" class="mb-4 p-3 bg-red-100 text-red-700 rounded-md">
        {{ error }}
      </div>
      
      <div class="mb-4">
        <label for="email" class="block text-gray-700 font-medium mb-2">Correo Electrónico</label>
        <input 
          type="email" 
          id="email" 
          v-model="credenciales.email" 
          class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        >
      </div>
      
      <div class="mb-6">
        <label for="password" class="block text-gray-700 font-medium mb-2">Contraseña</label>
        <input 
          type="password" 
          id="password" 
          v-model="credenciales.password" 
          class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        >
        <div class="mt-1 text-right">
          <a href="#" class="text-sm text-blue-600 hover:underline">¿Olvidaste tu contraseña?</a>
        </div>
      </div>
      
      <div class="mb-6">
        <button 
          type="submit" 
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition-colors"
          :disabled="cargando"
        >
          <span v-if="cargando">Iniciando sesión...</span>
          <span v-else>Iniciar Sesión</span>
        </button>
      </div>
      
      <div class="text-center text-gray-600">
        ¿No tienes una cuenta? 
        <router-link to="/registro" class="text-blue-600 hover:underline">Regístrate</router-link>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { useStore } from 'vuex';
import { useRouter, useRoute } from 'vue-router';

export default {
  name: 'IniciarSesion',
  setup() {
    const tienda = useStore();
    const router = useRouter();
    const route = useRoute();
    
    const credenciales = ref({
      email: '',
      password: ''
    });
    
    const error = computed(() => tienda.state.error);
    const cargando = computed(() => tienda.state.cargando);
    
    const iniciarSesion = async () => {
      try {
        const usuario = await tienda.dispatch('iniciarSesion', credenciales.value);
        
        // Redirigir según el rol del usuario
        if (usuario.rol === 'administrador') {
          router.push('/admin');
        } else if (usuario.rol === 'empleado') {
          router.push('/empleado');
        } else {
          // Redirigir a la página de usuario o a la página de redirección si existe
          const redirectPath = route.query.redirect || '/usuario';
          router.push(redirectPath);
        }
      } catch (error) {
        // El error ya se maneja en la acción de Vuex
        console.error('Error al iniciar sesión:', error);
      }
    };
    
    return {
      credenciales,
      error,
      cargando,
      iniciarSesion
    };
  }
}
</script>

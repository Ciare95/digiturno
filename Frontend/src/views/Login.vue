<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md text-center">
      <div class="flex justify-center mb-4">
        <div class="w-16 h-16 bg-blue-600 rounded-2xl flex items-center justify-center shadow-lg">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
      </div>
      <h1 class="text-4xl font-bold text-gray-800 mb-2">DigiTurno</h1>
      <p class="text-gray-600 mb-10">Inicia sesión para continuar</p>
    </div>

    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-6 shadow-xl rounded-2xl sm:px-10 border border-gray-100">
        <form class="space-y-6" @submit.prevent="handleLogin">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700">
              Nombre de usuario
            </label>
            <div class="mt-1">
              <input
                id="username"
                v-model="username"
                name="username"
                type="text"
                autocomplete="username"
                required
                class="appearance-none block w-full px-4 py-3 border border-gray-200 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-200 sm:text-sm"
                placeholder="tu_usuario"
              >
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              Contraseña
            </label>
            <div class="mt-1">
              <input
                id="password"
                v-model="password"
                name="password"
                type="password"
                autocomplete="current-password"
                required
                class="appearance-none block w-full px-4 py-3 border border-gray-200 rounded-xl shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-200 sm:text-sm"
                placeholder="••••••••"
              >
            </div>
          </div>

          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <div class="relative flex items-center">
                <input
                  id="remember-me"
                  v-model="rememberMe"
                  name="remember-me"
                  type="checkbox"
                  class="h-5 w-5 text-blue-600 focus:ring-blue-500 border-gray-300 rounded-md focus:ring-2 focus:ring-offset-2 transition"
                >
                <label for="remember-me" class="ml-2 block text-sm text-gray-700">
                  Recordar sesión
                </label>
              </div>
            </div>

            <div class="text-sm">
              <a href="#" class="font-medium text-blue-600 hover:text-blue-500 transition-colors duration-200">
                ¿Olvidaste tu contraseña?
              </a>
            </div>
          </div>

          <div>
            <button
              type="submit"
              class="w-full flex justify-center py-3 px-4 border border-transparent rounded-xl shadow-sm text-base font-medium text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200 transform hover:-translate-y-0.5">
              Iniciar Sesión
            </button>
          </div>
        </form>

        <div v-if="inicioexitoso" class="mt-6 p-4 bg-green-50 border-l-4 border-green-500 rounded-lg">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.707a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 10-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-sm text-green-700">
                {{ inicioexitoso }}
              </p>
            </div>
          </div>
        </div>

        <div v-if="error" class="mt-6 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-sm text-red-700">
                {{ error }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import AuthService from '@/services/AuthService';

export default {
  name: 'LoginView',
  data() {
    return {
      username: '',
      password: '',
      rememberMe: false,
      error: '',
      inicioexitoso: ''
    }
  },
  methods: {
    async handleLogin() {
      try {
        const response = await AuthService.login(this.username, this.password)
        console.log('Login response:', response)
        const token = response['access']
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`

        // Guardar token
        if (this.rememberMe) {
          localStorage.setItem('access', token)
        } else {
          sessionStorage.setItem('access', token)
        }

        this.inicioexitoso = 'Inicio de sesión exitoso.'
        
        // Redirigir según tipo de usuario
        if (response.es_admin) {
          this.$router.push('/admin')
        } else if (response.es_empleado) {
          this.$router.push('/empleado')
        } else {
          this.$router.push('/')
        }
      } catch (error) {
        console.error('Error al iniciar sesión:', error)
        this.error = 'Credenciales incorrectas o error de servidor.'
      }
    }
  }
}
</script>

<style scoped>
/* Efecto de elevación al hacer hover en el formulario */
.form-container {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.form-container:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* Efecto de entrada en los campos */
input[type="email"],
input[type="password"] {
  transition: all 0.2s ease;
}

input[type="email"]:focus,
input[type="password"]:focus {
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

/* Estilo personalizado para el checkbox */
input[type="checkbox"]:checked {
  background-image: url("data:image/svg+xml,%3csvg viewBox='0 0 16 16' fill='white' xmlns='http://www.w3.org/2000/svg'%3e%3cpath d='M5.707 7.293a1 1 0 0 0-1.414 1.414l2 2a1 1 0 0 0 1.414 0l4-4a1 1 0 0 0-1.414-1.414L7 8.586 5.707 7.293z'/%3e%3c/svg%3e");
  background-color: currentColor;
  background-size: 100% 100%;
  background-position: center;
  background-repeat: no-repeat;
}
</style>

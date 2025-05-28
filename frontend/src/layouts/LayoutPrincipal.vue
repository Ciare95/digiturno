<template>
  <div class="min-h-screen flex flex-col">
    <!-- Barra de navegación principal -->
    <header class="bg-blue-600 text-white shadow-md">
      <nav class="container mx-auto px-4 py-3 flex justify-between items-center">
        <router-link to="/" class="text-xl font-bold">DigiTurno</router-link>
        
        <div class="flex space-x-4">
          <router-link to="/" class="hover:text-blue-200 transition-colors">Inicio</router-link>
          <router-link to="/iniciar-sesion" class="hover:text-blue-200 transition-colors">Iniciar Sesión</router-link>
          <router-link to="/registro" class="hover:text-blue-200 transition-colors">Registro</router-link>
        </div>
      </nav>
    </header>
    
    <!-- Contenido principal -->
    <main class="flex-grow container mx-auto px-4 py-6">
      <router-view></router-view>
    </main>
    
    <!-- Pie de página -->
    <footer class="bg-gray-800 text-white py-6">
      <div class="container mx-auto px-4">
        <div class="flex flex-col md:flex-row justify-between items-center">
          <div class="mb-4 md:mb-0">
            <p class="text-center md:text-left">&copy; {{ anioActual }} DigiTurno. Todos los derechos reservados.</p>
          </div>
          
          <div class="flex space-x-4">
            <a href="#" class="hover:text-blue-400 transition-colors">Términos y Condiciones</a>
            <a href="#" class="hover:text-blue-400 transition-colors">Privacidad</a>
            <a href="#" class="hover:text-blue-400 transition-colors">Contacto</a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'LayoutPrincipal',
  computed: {
    anioActual() {
      return new Date().getFullYear();
    }
  }
}
</script>

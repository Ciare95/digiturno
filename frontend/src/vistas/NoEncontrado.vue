<template>
  <div class="flex flex-col items-center justify-center min-h-[60vh] text-center px-4">
    <h1 class="text-9xl font-bold text-blue-600">404</h1>
    <h2 class="text-3xl font-semibold text-gray-800 mt-6 mb-4">Página No Encontrada</h2>
    <p class="text-lg text-gray-600 max-w-md mb-8">
      Lo sentimos, la página que estás buscando no existe o ha sido movida.
    </p>
    <router-link to="/" class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition-colors">
      Volver al Inicio
    </router-link>
  </div>
</template>

<script>
export default {
  name: 'NoEncontrado'
}
</script>

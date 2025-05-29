<template>
  <div id="app">
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
    
    <!-- Selector de roles para desarrollo -->
    <SelectorDesarrollo />
  </div>
</template>

<script>
import SelectorDesarrollo from './componentes/SelectorDesarrollo.vue';

export default {
  name: 'App',
  components: {
    SelectorDesarrollo
  }
}
</script>

<style>
/* Estilos básicos para la aplicación */
#app {
  font-family: 'Inter', Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  min-height: 100vh;
}
</style>

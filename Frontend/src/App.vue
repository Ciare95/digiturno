<template>
  <div class="app-root">
    <router-view></router-view>
    <!--Añadir el container de notificaion-->
      <!--NotificacionContainer-->
  </div>
</template>

<script>
import NotificationContainer from '@/components/ui/NotificationContainer.vue';

export default {
  name: 'App',
}
</script>
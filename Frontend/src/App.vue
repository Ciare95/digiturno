<template>
  <div id="app">
    <router-view></router-view>
    <NotificationContainer />
  </div>
</template>

<script>
import NotificationContainer from '@/components/ui/NotificationContainer.vue';

export default {
  name: 'App',
}
</script>
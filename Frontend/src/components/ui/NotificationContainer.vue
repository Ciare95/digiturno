<template>
  <div class="fixed top-4 right-4 z-50 space-y-2">
    <Alert
      v-for="notification in notifications"
      :key="notification.id"
      :type="notification.type"
      :title="notification.title"
      :message="notification.message"
      :duration="notification.duration"
      :auto-close="notification.autoClose"
      :show="notification.show"
      @close="removeNotification(notification.id)"
    />
  </div>
</template>

<script setup>
import { useNotifications } from '@/composables/useNotifications';
import Alert from './Alert.vue';

const { notifications, removeNotification } = useNotifications();
</script> 
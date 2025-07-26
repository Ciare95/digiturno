import { ref } from 'vue';

const notifications = ref([]);

export function useNotifications() {
  const addNotification = (notification) => {
    const id = Date.now() + Math.random();
    const newNotification = {
      id,
      ...notification,
      show: true
    };
    
    notifications.value.push(newNotification);
    
    // Auto-remove after duration
    if (notification.autoClose !== false && notification.duration !== 0) {
      setTimeout(() => {
        removeNotification(id);
      }, notification.duration || 5000);
    }
    
    return id;
  };

  const removeNotification = (id) => {
    const index = notifications.value.findIndex(n => n.id === id);
    if (index > -1) {
      notifications.value[index].show = false;
      setTimeout(() => {
        notifications.value.splice(index, 1);
      }, 300); // Wait for transition
    }
  };

  const showError = (title, message = '') => {
    return addNotification({
      type: 'error',
      title,
      message,
      duration: 7000 // Errors stay longer
    });
  };

  const showSuccess = (title, message = '') => {
    return addNotification({
      type: 'success',
      title,
      message,
      duration: 4000
    });
  };

  const showWarning = (title, message = '') => {
    return addNotification({
      type: 'warning',
      title,
      message,
      duration: 5000
    });
  };

  const showInfo = (title, message = '') => {
    return addNotification({
      type: 'info',
      title,
      message,
      duration: 4000
    });
  };

  return {
    notifications,
    addNotification,
    removeNotification,
    showError,
    showSuccess,
    showWarning,
    showInfo
  };
} 
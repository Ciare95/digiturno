<template>
  <div class="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 to-indigo-100">
    <!-- Header -->
    <AppHeader />

    <!-- Contenido Principal -->
    <main class="flex-grow container mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold text-center mb-8 text-gray-800">Sistema de Gestión de Turnos</h1>
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Formulario de Turno -->
        <div class="order-2 lg:order-1">
          <TurnoForm />
        </div>
        
        <!-- Lista de Turnos en Espera -->
        <div class="order-1 lg:order-2">
          <TurnosList />
        </div>
      </div>
    </main>

    <!-- Footer -->
    <AppFooter />
  </div>
</template>

<script setup>
import AppHeader from '@/components/layout/AppHeader.vue';
import AppFooter from '@/components/layout/AppFooter.vue';
import TurnoForm from '@/components/turnos/TurnoForm.vue';
import TurnosList from '@/components/turnos/TurnosList.vue';
</script>
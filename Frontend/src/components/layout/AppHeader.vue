<template>
    <header class="sticky top-0 z-50 bg-white/90 backdrop-blur-sm shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <!-- Logo -->
                <div class="flex-shrink-0">
                    <div class="flex items-center space-x-2">
                        <span
                            class="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-blue-500 bg-clip-text text-transparent">
                            DigiTurno
                        </span>
                    </div>
                </div>

                <!-- Navegación de escritorio-->
                <nav class="hidden md:flex items-center space-x-1">
                    <ul class="flex items-center space-x-1">
                        <li v-for="item in itemsNavegacion" :key="item.path">
                            <a :href="item.path" :class="obtenerClassItemNav(item)">
                                {{ item.name }}
                            </a>
                        </li>
                    </ul>
                </nav>

                <!-- Botón para menú mobile-->
                <div class="flex md:hidden">
                    <button type="button" @click="toggleMobileMenu"
                        class="p-2 rounded-lg text-gray-600 hover:bg-gray-100 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
                        <span class="sr-only">Abrir menú</span>
                        <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M4 6h16M4 12h16M4 18h16" />
                        </svg>
                    </button>
                </div>

                <!-- Mobile menu -->
                <div v-if="isMobileMenuOpen" class="md:hidden">
                    <div class="px-2 pt-2 pb-3 space-y-1">
                        <a v-for="item in navigationItems" :key="item.path" :href="item.path"
                            class="block px-4 py-2 text-base font-medium text-gray-600 hover:text-indigo-700 hover:bg-indigo-50 rounded-lg transition-colors">
                            {{ item.name }}
                        </a>
                        <div class="pt-4 border-t border-gray-200 mt-2 space-y-3">
                            <a href="#"
                                class="block w-full px-4 py-2 text-base font-medium text-center text-gray-700 hover:text-indigo-700 hover:bg-gray-50 rounded-lg transition-colors">
                                Iniciar sesión
                            </a>
                            <a href="#"
                                class="block w-full px-4 py-2 text-base font-medium text-center text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg transition-colors shadow-sm">
                                Registrarse
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </header>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const itemsNavegacion = ref([
    { name: 'Inicio', path: '#', active: true },
    { name: 'Servicios', path: '#', active: false },
    { name: 'Sucursales', path: '#', active: false },
    { name: 'Contacto', path: '#', active: false }
])

const obtenerClassItemNav = (item) => {
    const baseClass = 'px-4 py-2 text-sm font-medium rounded-lg transition-colors'

    if (item.active) {
        return `${baseClass} text-indigo-700 hover:bg-indigo-50`
    } else {
        return `${baseClass} text-gray-600 hover:text-indigo-700 hover:bg-indigo-50`
    }
}

// Métodos
const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}
</script>
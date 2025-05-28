<template>
  <div>
    <section class="py-12 bg-blue-50 rounded-lg shadow-inner mb-8">
      <div class="container mx-auto px-4">
        <div class="flex flex-col md:flex-row items-center">
          <div class="md:w-1/2 mb-8 md:mb-0">
            <h1 class="text-4xl font-bold text-blue-800 mb-4">Sistema de Gestión de Turnos Digital</h1>
            <p class="text-lg text-gray-700 mb-6">
              Optimiza la atención al cliente y reduce los tiempos de espera con nuestro sistema de gestión de turnos digital.
            </p>
            <div class="flex flex-wrap gap-4">
              <router-link to="/registro" class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition-colors">
                Registrarse
              </router-link>
              <router-link to="/iniciar-sesion" class="bg-white hover:bg-gray-100 text-blue-600 font-medium py-2 px-6 rounded-lg border border-blue-600 transition-colors">
                Iniciar Sesión
              </router-link>
            </div>
          </div>
          <div class="md:w-1/2">
            <img src="@/assets/hero-image.svg" alt="DigiTurno" class="w-full h-auto">
          </div>
        </div>
      </div>
    </section>

    <section class="mb-12">
      <div class="container mx-auto px-4">
        <h2 class="text-3xl font-bold text-center text-gray-800 mb-8">Características Principales</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="bg-white p-6 rounded-lg shadow-md">
            <div class="text-blue-600 text-4xl mb-4">
              <i class="fas fa-mobile-alt"></i>
            </div>
            <h3 class="text-xl font-semibold mb-2">Gestión de Turnos Digital</h3>
            <p class="text-gray-600">
              Permite a los usuarios solicitar turnos desde cualquier dispositivo, eliminando las filas físicas y mejorando la experiencia.
            </p>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow-md">
            <div class="text-blue-600 text-4xl mb-4">
              <i class="fas fa-chart-line"></i>
            </div>
            <h3 class="text-xl font-semibold mb-2">Estadísticas en Tiempo Real</h3>
            <p class="text-gray-600">
              Monitorea el rendimiento de tus servicios con estadísticas detalladas y en tiempo real para mejorar la atención.
            </p>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow-md">
            <div class="text-blue-600 text-4xl mb-4">
              <i class="fas fa-bell"></i>
            </div>
            <h3 class="text-xl font-semibold mb-2">Notificaciones Automáticas</h3>
            <p class="text-gray-600">
              Los usuarios reciben notificaciones sobre el estado de su turno, reduciendo la ansiedad y mejorando la satisfacción.
            </p>
          </div>
        </div>
      </div>
    </section>

    <section class="mb-12 bg-gray-50 py-12">
      <div class="container mx-auto px-4">
        <h2 class="text-3xl font-bold text-center text-gray-800 mb-8">¿Cómo Funciona?</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div class="text-center">
            <div class="bg-blue-100 text-blue-600 w-16 h-16 rounded-full flex items-center justify-center text-2xl mx-auto mb-4">
              1
            </div>
            <h3 class="text-xl font-semibold mb-2">Registro</h3>
            <p class="text-gray-600">
              Crea una cuenta en nuestra plataforma para comenzar a utilizar el sistema.
            </p>
          </div>
          
          <div class="text-center">
            <div class="bg-blue-100 text-blue-600 w-16 h-16 rounded-full flex items-center justify-center text-2xl mx-auto mb-4">
              2
            </div>
            <h3 class="text-xl font-semibold mb-2">Solicita un Turno</h3>
            <p class="text-gray-600">
              Selecciona la sucursal y el servicio deseado para obtener un turno digital.
            </p>
          </div>
          
          <div class="text-center">
            <div class="bg-blue-100 text-blue-600 w-16 h-16 rounded-full flex items-center justify-center text-2xl mx-auto mb-4">
              3
            </div>
            <h3 class="text-xl font-semibold mb-2">Recibe Notificaciones</h3>
            <p class="text-gray-600">
              Te notificaremos cuando sea tu turno o si hay cambios en el tiempo de espera.
            </p>
          </div>
          
          <div class="text-center">
            <div class="bg-blue-100 text-blue-600 w-16 h-16 rounded-full flex items-center justify-center text-2xl mx-auto mb-4">
              4
            </div>
            <h3 class="text-xl font-semibold mb-2">Atención Personalizada</h3>
            <p class="text-gray-600">
              Recibe atención sin esperas innecesarias y califica el servicio recibido.
            </p>
          </div>
        </div>
      </div>
    </section>

    <section class="mb-12">
      <div class="container mx-auto px-4">
        <h2 class="text-3xl font-bold text-center text-gray-800 mb-8">Testimonios</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="bg-white p-6 rounded-lg shadow-md">
            <div class="flex items-center mb-4">
              <div class="text-yellow-400 flex">
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
              </div>
            </div>
            <p class="text-gray-600 mb-4">
              "DigiTurno ha transformado completamente la experiencia de nuestros clientes. Los tiempos de espera se han reducido significativamente."
            </p>
            <div class="font-medium">Carlos Rodríguez</div>
            <div class="text-sm text-gray-500">Gerente de Sucursal</div>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow-md">
            <div class="flex items-center mb-4">
              <div class="text-yellow-400 flex">
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
              </div>
            </div>
            <p class="text-gray-600 mb-4">
              "Como cliente, valoro poder solicitar mi turno desde mi teléfono y recibir notificaciones sobre mi tiempo de espera. ¡Excelente servicio!"
            </p>
            <div class="font-medium">Laura Martínez</div>
            <div class="text-sm text-gray-500">Cliente</div>
          </div>
          
          <div class="bg-white p-6 rounded-lg shadow-md">
            <div class="flex items-center mb-4">
              <div class="text-yellow-400 flex">
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
                <i class="fas fa-star-half-alt"></i>
              </div>
            </div>
            <p class="text-gray-600 mb-4">
              "Las estadísticas que proporciona DigiTurno nos han permitido optimizar nuestros recursos y mejorar la calidad de atención."
            </p>
            <div class="font-medium">Ana Gómez</div>
            <div class="text-sm text-gray-500">Directora de Operaciones</div>
          </div>
        </div>
      </div>
    </section>

    <section class="bg-blue-600 text-white py-12 rounded-lg">
      <div class="container mx-auto px-4 text-center">
        <h2 class="text-3xl font-bold mb-6">¿Listo para optimizar la gestión de tus turnos?</h2>
        <p class="text-xl mb-8 max-w-3xl mx-auto">
          Únete a las empresas que ya están mejorando la experiencia de sus clientes con DigiTurno.
        </p>
        <router-link to="/registro" class="bg-white hover:bg-gray-100 text-blue-600 font-medium py-3 px-8 rounded-lg transition-colors inline-block">
          Comenzar Ahora
        </router-link>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'PaginaInicio',
}
</script>

<template>
  <div class="configuracion-admin">
    <h1>Configuración General del Sistema</h1>

    <div class="secciones-configuracion">
      <!-- Configuración de la Aplicación -->
      <section class="seccion">
        <h2><i class="fas fa-cogs"></i> Configuración de la Aplicación</h2>
        <form @submit.prevent="guardarConfiguracionApp">
          <div class="campo-config">
            <label for="nombreApp">Nombre de la Aplicación</label>
            <input type="text" id="nombreApp" v-model="configApp.nombreAplicacion" />
          </div>
          <div class="campo-config">
            <label for="logoApp">URL del Logo</label>
            <input type="url" id="logoApp" v-model="configApp.urlLogo" />
            <small>Dejar en blanco para usar el logo por defecto.</small>
          </div>
          <div class="campo-config">
            <label for="idiomaDefault">Idioma por Defecto</label>
            <select id="idiomaDefault" v-model="configApp.idiomaPredeterminado">
              <option value="es">Español</option>
              <option value="en">Inglés</option>
              <!-- Agregar más idiomas si es necesario -->
            </select>
          </div>
          <div class="campo-config">
            <label for="zonaHoraria">Zona Horaria</label>
            <select id="zonaHoraria" v-model="configApp.zonaHoraria">
              <option value="America/Bogota">America/Bogota (Colombia)</option>
              <option value="America/Mexico_City">America/Mexico_City</option>
              <option value="America/Lima">America/Lima (Perú)</option>
              <option value="Europe/Madrid">Europe/Madrid (España)</option>
              <!-- Agregar más zonas horarias -->
            </select>
          </div>
          <button type="submit" class="boton-primario">Guardar Configuración de Aplicación</button>
        </form>
      </section>

      <!-- Configuración de Notificaciones -->
      <section class="seccion">
        <h2><i class="fas fa-bell"></i> Configuración de Notificaciones</h2>
        <form @submit.prevent="guardarConfiguracionNotificaciones">
          <div class="campo-config">
            <label for="emailAdmin">Email del Administrador para Notificaciones</label>
            <input type="email" id="emailAdmin" v-model="configNotificaciones.emailAdmin" />
          </div>
          <div class="campo-config">
            <label>
              <input type="checkbox" v-model="configNotificaciones.notificarNuevoUsuario" />
              Notificar creación de nuevos usuarios
            </label>
          </div>
          <div class="campo-config">
            <label>
              <input type="checkbox" v-model="configNotificaciones.notificarTurnoCritico" />
              Notificar turnos con tiempo de espera crítico
            </label>
          </div>
          <button type="submit" class="boton-primario">Guardar Configuración de Notificaciones</button>
        </form>
      </section>

      <!-- Configuración de Turnos -->
      <section class="seccion">
        <h2><i class="fas fa-ticket"></i> Configuración de Turnos</h2>
        <form @submit.prevent="guardarConfiguracionTurnos">
          <div class="campo-config">
            <label for="prefijoTurno">Prefijo para Números de Turno</label>
            <input type="text" id="prefijoTurno" v-model="configTurnos.prefijo" maxlength="5" />
            <small>Ej: A, CITA, T-</small>
          </div>
          <div class="campo-config">
            <label for="longitudNumero">Longitud del Número de Turno (sin prefijo)</label>
            <input type="number" id="longitudNumero" v-model.number="configTurnos.longitudNumero" min="1" max="5" />
          </div>
          <div class="campo-config">
            <label for="tiempoMaxEspera">Tiempo Máximo de Espera Estimado (minutos)</label>
            <input type="number" id="tiempoMaxEspera" v-model.number="configTurnos.tiempoMaxEsperaEstimado" min="5" />
          </div>
           <div class="campo-config">
            <label>
              <input type="checkbox" v-model="configTurnos.permitirCancelacionUsuario" />
              Permitir a los usuarios cancelar sus propios turnos
            </label>
          </div>
          <button type="submit" class="boton-primario">Guardar Configuración de Turnos</button>
        </form>
      </section>

      <!-- Mantenimiento del Sistema -->
      <section class="seccion">
        <h2><i class="fas fa-tools"></i> Mantenimiento del Sistema</h2>
        <div class="acciones-mantenimiento">
          <button @click="limpiarCache" class="boton-secundario">
            <i class="fas fa-broom"></i> Limpiar Caché de la Aplicación
          </button>
          <button @click="regenerarIndices" class="boton-secundario">
            <i class="fas fa-database"></i> Regenerar Índices de Base de Datos
          </button>
          <button @click="verLogsSistema" class="boton-secundario">
            <i class="fas fa-file-alt"></i> Ver Logs del Sistema
          </button>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConfiguracionAdmin',
  data() {
    return {
      configApp: {
        nombreAplicacion: 'Digiturno Pro',
        urlLogo: '',
        idiomaPredeterminado: 'es',
        zonaHoraria: 'America/Bogota'
      },
      configNotificaciones: {
        emailAdmin: 'admin@example.com',
        notificarNuevoUsuario: true,
        notificarTurnoCritico: true
      },
      configTurnos: {
        prefijo: 'A',
        longitudNumero: 3,
        tiempoMaxEsperaEstimado: 60,
        permitirCancelacionUsuario: true
      }
    };
  },
  mounted() {
    this.cargarConfiguraciones();
  },
  methods: {
    cargarConfiguraciones() {
      // Simulación de carga de configuraciones desde el backend
      console.log('Cargando configuraciones...');
      // En una aplicación real, aquí se haría una llamada API para obtener los valores
      // this.configApp = api.getConfigApp();
      // this.configNotificaciones = api.getConfigNotificaciones();
      // this.configTurnos = api.getConfigTurnos();
    },
    guardarConfiguracionApp() {
      console.log('Guardando configuración de la aplicación:', this.configApp);
      // Lógica para guardar en el backend
      this.$toast.success('Configuración de la aplicación guardada.');
    },
    guardarConfiguracionNotificaciones() {
      console.log('Guardando configuración de notificaciones:', this.configNotificaciones);
      // Lógica para guardar en el backend
      this.$toast.success('Configuración de notificaciones guardada.');
    },
    guardarConfiguracionTurnos() {
      console.log('Guardando configuración de turnos:', this.configTurnos);
      // Lógica para guardar en el backend
      this.$toast.success('Configuración de turnos guardada.');
    },
    limpiarCache() {
      if (confirm('¿Está seguro de que desea limpiar la caché de la aplicación?')) {
        console.log('Limpiando caché...');
        // Lógica para limpiar caché en el backend
        this.$toast.info('Caché de la aplicación limpiada.');
      }
    },
    regenerarIndices() {
      if (confirm('Esta acción puede tardar y afectar el rendimiento temporalmente. ¿Desea continuar?')) {
        console.log('Regenerando índices...');
        // Lógica para regenerar índices en el backend
        this.$toast.info('Iniciada la regeneración de índices de la base de datos.');
      }
    },
    verLogsSistema() {
      console.log('Abriendo logs del sistema...');
      // Esto podría redirigir a una nueva página o mostrar un modal con los logs
      this.$toast.info('Funcionalidad de ver logs aún no implementada.');
    }
  }
};
</script>

<style scoped>
.configuracion-admin {
  padding: 2rem;
}

h1 {
  margin-bottom: 2rem;
  color: #333;
  text-align: center;
}

.secciones-configuracion {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.seccion {
  background-color: #ffffff;
  border-radius: 8px;
  padding: 1.5rem 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.seccion h2 {
  font-size: 1.3rem;
  color: #007bff;
  margin-top: 0;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #007bff;
  padding-bottom: 0.5rem;
}

.seccion h2 i {
  margin-right: 0.75rem;
}

.campo-config {
  margin-bottom: 1.2rem;
}

.campo-config label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #555;
}

.campo-config input[type="text"],
.campo-config input[type="url"],
.campo-config input[type="email"],
.campo-config input[type="number"],
.campo-config select {
  width: 100%;
  padding: 0.7rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.95rem;
  box-sizing: border-box;
}

.campo-config input[type="checkbox"] {
  margin-right: 0.5rem;
  vertical-align: middle;
}

.campo-config small {
  display: block;
  margin-top: 0.3rem;
  font-size: 0.8rem;
  color: #777;
}

.boton-primario {
  background-color: #007bff;
  color: white;
  padding: 0.7rem 1.3rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background-color 0.2s;
  margin-top: 0.5rem;
}

.boton-primario:hover {
  background-color: #0056b3;
}

.boton-secundario {
  background-color: #6c757d;
  color: white;
  padding: 0.7rem 1.3rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background-color 0.2s;
}

.boton-secundario:hover {
  background-color: #545b62;
}

.boton-secundario i {
  margin-right: 0.5rem;
}

.acciones-mantenimiento {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

@media (max-width: 900px) {
  .secciones-configuracion {
    grid-template-columns: 1fr; /* Una columna en pantallas más pequeñas */
  }
}
</style>

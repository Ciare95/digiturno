<template>
  <div class="perfil-usuario">
    <h1>Mi Perfil</h1>
    <div class="contenedor-perfil">
      <div class="seccion-informacion">
        <h2>Información Personal</h2>
        <form @submit.prevent="actualizarPerfil">
          <div class="campo-formulario">
            <label for="nombre">Nombre</label>
            <input type="text" id="nombre" v-model="usuario.nombre" required />
          </div>
          <div class="campo-formulario">
            <label for="apellido">Apellido</label>
            <input type="text" id="apellido" v-model="usuario.apellido" required />
          </div>
          <div class="campo-formulario">
            <label for="email">Correo Electrónico</label>
            <input type="email" id="email" v-model="usuario.email" required disabled />
          </div>
          <div class="campo-formulario">
            <label for="telefono">Teléfono</label>
            <input type="tel" id="telefono" v-model="usuario.telefono" />
          </div>
          <button type="submit" class="boton-primario">Guardar Cambios</button>
        </form>
      </div>
      
      <div class="seccion-seguridad">
        <h2>Seguridad</h2>
        <form @submit.prevent="cambiarContrasena">
          <div class="campo-formulario">
            <label for="contrasenaActual">Contraseña Actual</label>
            <input type="password" id="contrasenaActual" v-model="cambioContrasena.actual" required />
          </div>
          <div class="campo-formulario">
            <label for="nuevaContrasena">Nueva Contraseña</label>
            <input type="password" id="nuevaContrasena" v-model="cambioContrasena.nueva" required />
          </div>
          <div class="campo-formulario">
            <label for="confirmarContrasena">Confirmar Contraseña</label>
            <input type="password" id="confirmarContrasena" v-model="cambioContrasena.confirmar" required />
          </div>
          <button type="submit" class="boton-secundario">Cambiar Contraseña</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PerfilUsuario',
  data() {
    return {
      usuario: {
        nombre: '',
        apellido: '',
        email: '',
        telefono: ''
      },
      cambioContrasena: {
        actual: '',
        nueva: '',
        confirmar: ''
      },
      cargando: false,
      mensaje: ''
    };
  },
  mounted() {
    this.cargarDatosUsuario();
  },
  methods: {
    // Cargar datos del usuario desde el servidor
    cargarDatosUsuario() {
      // Aquí se implementaría la lógica para cargar los datos del usuario
      // desde el servidor o desde el estado de la aplicación
      this.cargando = true;
      
      // Simulación de carga de datos
      setTimeout(() => {
        // Estos datos vendrían de una API real
        this.usuario = {
          nombre: 'Nombre Usuario',
          apellido: 'Apellido Usuario',
          email: 'usuario@ejemplo.com',
          telefono: '123456789'
        };
        this.cargando = false;
      }, 500);
    },
    
    // Actualizar perfil del usuario
    actualizarPerfil() {
      // Aquí se implementaría la lógica para actualizar el perfil
      // del usuario en el servidor
      this.cargando = true;
      
      // Simulación de actualización
      setTimeout(() => {
        // Aquí iría la llamada a la API para actualizar el perfil
        this.mensaje = 'Perfil actualizado correctamente';
        this.cargando = false;
        
        // Mostrar mensaje de éxito
        this.$toast.success(this.mensaje);
      }, 800);
    },
    
    // Cambiar contraseña del usuario
    cambiarContrasena() {
      // Validar que las contraseñas coincidan
      if (this.cambioContrasena.nueva !== this.cambioContrasena.confirmar) {
        this.mensaje = 'Las contraseñas no coinciden';
        this.$toast.error(this.mensaje);
        return;
      }
      
      this.cargando = true;
      
      // Simulación de cambio de contraseña
      setTimeout(() => {
        // Aquí iría la llamada a la API para cambiar la contraseña
        this.mensaje = 'Contraseña actualizada correctamente';
        this.cargando = false;
        
        // Limpiar campos
        this.cambioContrasena = {
          actual: '',
          nueva: '',
          confirmar: ''
        };
        
        // Mostrar mensaje de éxito
        this.$toast.success(this.mensaje);
      }, 800);
    }
  }
};
</script>

<style scoped>
.perfil-usuario {
  padding: 2rem;
}

.contenedor-perfil {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

@media (max-width: 768px) {
  .contenedor-perfil {
    grid-template-columns: 1fr;
  }
}

.seccion-informacion,
.seccion-seguridad {
  background-color: #ffffff;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h1 {
  margin-bottom: 2rem;
  color: #333;
}

h2 {
  margin-bottom: 1.5rem;
  color: #555;
  font-size: 1.2rem;
}

.campo-formulario {
  margin-bottom: 1.2rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #666;
}

input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

input:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

button {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.boton-primario {
  background-color: #4a90e2;
  color: white;
}

.boton-primario:hover {
  background-color: #3a7bc8;
}

.boton-secundario {
  background-color: #6c757d;
  color: white;
}

.boton-secundario:hover {
  background-color: #5a6268;
}
</style>

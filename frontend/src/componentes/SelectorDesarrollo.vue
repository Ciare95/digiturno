<template>
  <div v-if="modoDesarrollo" class="selector-desarrollo">
    <div class="contenedor">
      <div class="titulo">Modo Desarrollo</div>
      <div class="descripcion">Selecciona un rol para navegar:</div>
      
      <div class="botones">
        <button 
          @click="cambiarRol('usuario')" 
          :class="['boton', rolActual === 'usuario' ? 'activo' : '']">
          Usuario
        </button>
        <button 
          @click="cambiarRol('empleado')" 
          :class="['boton', rolActual === 'empleado' ? 'activo' : '']">
          Empleado
        </button>
        <button 
          @click="cambiarRol('administrador')" 
          :class="['boton', rolActual === 'administrador' ? 'activo' : '']">
          Administrador
        </button>
      </div>
      
      <div class="acciones">
        <button @click="irAPanelRol" class="boton-accion">
          Ir al Panel
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'SelectorDesarrollo',
  setup() {
    const router = useRouter();
    const modoDesarrollo = ref(true);
    const rolActual = ref('usuario');
    
    // Obtener el rol actual del localStorage al montar el componente
    onMounted(() => {
      const usuarioGuardado = localStorage.getItem('usuario');
      if (usuarioGuardado) {
        try {
          const usuario = JSON.parse(usuarioGuardado);
          if (usuario && usuario.rol) {
            rolActual.value = usuario.rol;
          }
        } catch (e) {
          console.error('Error al parsear usuario:', e);
        }
      }
    });
    
    // Función para cambiar el rol del usuario simulado
    const cambiarRol = (nuevoRol) => {
      rolActual.value = nuevoRol;
      
      // Crear usuario simulado según el rol
      const usuarioSimulado = {
        id: 1,
        first_name: 'Usuario',
        last_name: 'Simulado',
        email: `${nuevoRol}@ejemplo.com`,
        rol: nuevoRol
      };
      
      // Guardar en localStorage
      localStorage.setItem('usuario', JSON.stringify(usuarioSimulado));
      localStorage.setItem('token', 'token-simulado-desarrollo');
    };
    
    // Función para ir al panel correspondiente al rol
    const irAPanelRol = () => {
      if (rolActual.value === 'usuario') {
        router.push('/usuario');
      } else if (rolActual.value === 'empleado') {
        router.push('/empleado');
      } else if (rolActual.value === 'administrador') {
        router.push('/admin');
      }
    };
    
    return {
      modoDesarrollo,
      rolActual,
      cambiarRol,
      irAPanelRol
    };
  }
}
</script>

<style scoped>
.selector-desarrollo {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 9999;
}

.contenedor {
  background-color: #2c3e50;
  color: white;
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  width: 250px;
}

.titulo {
  font-weight: bold;
  font-size: 16px;
  margin-bottom: 8px;
  border-bottom: 1px solid #3d5a74;
  padding-bottom: 6px;
}

.descripcion {
  font-size: 14px;
  margin-bottom: 10px;
  color: #a3c5e0;
}

.botones {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.boton {
  flex: 1;
  background-color: #34495e;
  border: none;
  color: white;
  padding: 6px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s;
}

.boton:hover {
  background-color: #3d5a74;
}

.boton.activo {
  background-color: #3498db;
}

.acciones {
  display: flex;
  justify-content: center;
}

.boton-accion {
  background-color: #2ecc71;
  border: none;
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  width: 100%;
  transition: all 0.2s;
}

.boton-accion:hover {
  background-color: #27ae60;
}
</style>

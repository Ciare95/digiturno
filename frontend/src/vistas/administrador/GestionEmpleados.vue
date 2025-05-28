<template>
  <div class="gestion-empleados">
    <h1>Gestión de Empleados</h1>
    
    <div class="acciones-superiores">
      <button @click="mostrarModalNuevoEmpleado = true" class="boton-primario">
        <i class="fas fa-plus"></i> Nuevo Empleado
      </button>
      <input type="text" v-model="busqueda" placeholder="Buscar empleado..." class="campo-busqueda" />
    </div>
    
    <div class="tabla-contenedor">
      <table v-if="empleadosFiltrados.length > 0" class="tabla-empleados">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Apellido</th>
            <th>Correo Electrónico</th>
            <th>Rol</th>
            <th>Sucursal</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="empleado in empleadosFiltrados" :key="empleado.id">
            <td>{{ empleado.nombre }}</td>
            <td>{{ empleado.apellido }}</td>
            <td>{{ empleado.email }}</td>
            <td>{{ empleado.rol }}</td>
            <td>{{ empleado.sucursal ? empleado.sucursal.nombre : 'N/A' }}</td>
            <td>
              <span class="estado" :class="'estado-' + (empleado.activo ? 'activo' : 'inactivo')">
                {{ empleado.activo ? 'Activo' : 'Inactivo' }}
              </span>
            </td>
            <td class="acciones-tabla">
              <button @click="editarEmpleado(empleado)" class="boton-icono" title="Editar">
                <i class="fas fa-edit"></i>
              </button>
              <button @click="cambiarEstadoEmpleado(empleado)" class="boton-icono" :title="empleado.activo ? 'Desactivar' : 'Activar'">
                <i :class="['fas', empleado.activo ? 'fa-toggle-off' : 'fa-toggle-on']"></i>
              </button>
              <button @click="eliminarEmpleado(empleado)" class="boton-icono boton-eliminar" title="Eliminar">
                <i class="fas fa-trash-alt"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="mensaje-vacio">
        No se encontraron empleados que coincidan con la búsqueda o no hay empleados registrados.
      </div>
    </div>
    
    <!-- Modal para Nuevo/Editar Empleado -->
    <div v-if="mostrarModalNuevoEmpleado || empleadoSeleccionado" class="modal-overlay">
      <div class="modal-contenido">
        <h2>{{ empleadoSeleccionado ? 'Editar Empleado' : 'Nuevo Empleado' }}</h2>
        <form @submit.prevent="guardarEmpleado">
          <div class="campo-formulario">
            <label for="nombre">Nombre</label>
            <input type="text" id="nombre" v-model="formEmpleado.nombre" required />
          </div>
          <div class="campo-formulario">
            <label for="apellido">Apellido</label>
            <input type="text" id="apellido" v-model="formEmpleado.apellido" required />
          </div>
          <div class="campo-formulario">
            <label for="email">Correo Electrónico</label>
            <input type="email" id="email" v-model="formEmpleado.email" required :disabled="!!empleadoSeleccionado"/>
          </div>
          <div class="campo-formulario" v-if="!empleadoSeleccionado">
            <label for="contrasena">Contraseña</label>
            <input type="password" id="contrasena" v-model="formEmpleado.contrasena" :required="!empleadoSeleccionado" />
          </div>
          <div class="campo-formulario">
            <label for="rol">Rol</label>
            <select id="rol" v-model="formEmpleado.rol" required>
              <option value="empleado">Empleado</option>
              <option value="administrador">Administrador</option>
            </select>
          </div>
          <div class="campo-formulario">
            <label for="sucursal">Sucursal Asignada</label>
            <select id="sucursal" v-model="formEmpleado.sucursalId">
              <option :value="null">Ninguna</option>
              <option v-for="sucursal in sucursales" :key="sucursal.id" :value="sucursal.id">
                {{ sucursal.nombre }}
              </option>
            </select>
          </div>
          
          <div class="acciones-modal">
            <button type="button" @click="cerrarModal" class="boton-secundario">Cancelar</button>
            <button type="submit" class="boton-primario">{{ empleadoSeleccionado ? 'Guardar Cambios' : 'Crear Empleado' }}</button>
          </div>
        </form>
      </div>
    </div>
    
  </div>
</template>

<script>
export default {
  name: 'GestionEmpleados',
  data() {
    return {
      empleados: [],
      sucursales: [],
      busqueda: '',
      mostrarModalNuevoEmpleado: false,
      empleadoSeleccionado: null,
      formEmpleado: {
        id: null,
        nombre: '',
        apellido: '',
        email: '',
        contrasena: '',
        rol: 'empleado',
        sucursalId: null,
        activo: true
      }
    };
  },
  computed: {
    empleadosFiltrados() {
      if (!this.busqueda) {
        return this.empleados;
      }
      const termino = this.busqueda.toLowerCase();
      return this.empleados.filter(emp => 
        emp.nombre.toLowerCase().includes(termino) ||
        emp.apellido.toLowerCase().includes(termino) ||
        emp.email.toLowerCase().includes(termino)
      );
    }
  },
  mounted() {
    this.cargarEmpleados();
    this.cargarSucursales();
  },
  methods: {
    cargarEmpleados() {
      // Simulación de carga de empleados
      setTimeout(() => {
        this.empleados = [
          {
            id: 1,
            nombre: 'Ana',
            apellido: 'García',
            email: 'ana.garcia@example.com',
            rol: 'empleado',
            sucursal: { id: 1, nombre: 'Sucursal Centro' },
            activo: true
          },
          {
            id: 2,
            nombre: 'Luis',
            apellido: 'Martínez',
            email: 'luis.martinez@example.com',
            rol: 'empleado',
            sucursal: { id: 2, nombre: 'Sucursal Norte' },
            activo: true
          },
          {
            id: 3,
            nombre: 'Laura',
            apellido: 'Fernández',
            email: 'laura.fernandez@example.com',
            rol: 'administrador',
            sucursal: null,
            activo: false
          },
          {
            id: 4,
            nombre: 'Carlos',
            apellido: 'López',
            email: 'carlos.lopez@example.com',
            rol: 'empleado',
            sucursal: { id: 1, nombre: 'Sucursal Centro' },
            activo: true
          }
        ];
      }, 500);
    },
    cargarSucursales() {
      // Simulación de carga de sucursales
      setTimeout(() => {
        this.sucursales = [
          { id: 1, nombre: 'Sucursal Centro' },
          { id: 2, nombre: 'Sucursal Norte' },
          { id: 3, nombre: 'Sucursal Sur' }
        ];
      }, 300);
    },
    editarEmpleado(empleado) {
      this.empleadoSeleccionado = { ...empleado };
      this.formEmpleado = {
        id: empleado.id,
        nombre: empleado.nombre,
        apellido: empleado.apellido,
        email: empleado.email,
        contrasena: '', // No se carga la contraseña por seguridad
        rol: empleado.rol,
        sucursalId: empleado.sucursal ? empleado.sucursal.id : null,
        activo: empleado.activo
      };
    },
    cambiarEstadoEmpleado(empleado) {
      // Lógica para cambiar estado en el backend
      const indice = this.empleados.findIndex(e => e.id === empleado.id);
      if (indice !== -1) {
        this.empleados[indice].activo = !this.empleados[indice].activo;
        this.$toast.success(`Estado de ${empleado.nombre} actualizado.`);
      }
    },
    eliminarEmpleado(empleado) {
      if (confirm(`¿Está seguro de eliminar a ${empleado.nombre} ${empleado.apellido}? Esta acción no se puede deshacer.`)) {
        // Lógica para eliminar en el backend
        this.empleados = this.empleados.filter(e => e.id !== empleado.id);
        this.$toast.success(`${empleado.nombre} ${empleado.apellido} ha sido eliminado.`);
      }
    },
    guardarEmpleado() {
      // Lógica para guardar (crear o actualizar) en el backend
      if (this.empleadoSeleccionado) { // Actualizar
        const indice = this.empleados.findIndex(e => e.id === this.formEmpleado.id);
        if (indice !== -1) {
          // Actualizar sucursal si se seleccionó una
          const sucursalSeleccionada = this.sucursales.find(s => s.id === this.formEmpleado.sucursalId);
          this.empleados[indice] = { 
            ...this.empleados[indice], 
            ...this.formEmpleado, 
            sucursal: sucursalSeleccionada 
          };
          this.$toast.success('Empleado actualizado correctamente.');
        }
      } else { // Crear
        const nuevoId = this.empleados.length > 0 ? Math.max(...this.empleados.map(e => e.id)) + 1 : 1;
        const sucursalSeleccionada = this.sucursales.find(s => s.id === this.formEmpleado.sucursalId);
        this.empleados.push({
          id: nuevoId,
          ...this.formEmpleado,
          sucursal: sucursalSeleccionada,
          activo: true // Por defecto, los nuevos empleados están activos
        });
        this.$toast.success('Empleado creado correctamente.');
      }
      this.cerrarModal();
    },
    cerrarModal() {
      this.mostrarModalNuevoEmpleado = false;
      this.empleadoSeleccionado = null;
      this.formEmpleado = {
        id: null,
        nombre: '',
        apellido: '',
        email: '',
        contrasena: '',
        rol: 'empleado',
        sucursalId: null,
        activo: true
      };
    }
  }
};
</script>

<style scoped>
.gestion-empleados {
  padding: 2rem;
}

h1 {
  margin-bottom: 1.5rem;
  color: #333;
}

.acciones-superiores {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.campo-busqueda {
  padding: 0.6rem 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9rem;
  width: 300px;
}

.tabla-contenedor {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  overflow-x: auto;
}

.tabla-empleados {
  width: 100%;
  border-collapse: collapse;
}

.tabla-empleados th,
.tabla-empleados td {
  padding: 0.8rem 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
  vertical-align: middle;
}

.tabla-empleados th {
  background-color: #f8f9fa;
  font-weight: 600;
  font-size: 0.9rem;
}

.estado {
  padding: 0.3rem 0.7rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
  text-transform: capitalize;
}

.estado-activo {
  background-color: #d4edda;
  color: #155724;
}

.estado-inactivo {
  background-color: #f8d7da;
  color: #721c24;
}

.acciones-tabla {
  display: flex;
  gap: 0.5rem;
}

.boton-icono {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  color: #555;
  font-size: 1.1rem;
}

.boton-icono:hover {
  color: #007bff;
}

.boton-icono.boton-eliminar:hover {
  color: #dc3545;
}

.mensaje-vacio {
  padding: 2rem;
  text-align: center;
  color: #6c757d;
}

/* Estilos del Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-contenido {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  width: 90%;
  max-width: 500px;
}

.modal-contenido h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #333;
}

.campo-formulario {
  margin-bottom: 1rem;
}

.campo-formulario label {
  display: block;
  margin-bottom: 0.3rem;
  font-weight: 500;
  color: #555;
}

.campo-formulario input,
.campo-formulario select {
  width: 100%;
  padding: 0.7rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.95rem;
}

.acciones-modal {
  display: flex;
  justify-content: flex-end;
  gap: 0.8rem;
  margin-top: 1.5rem;
}

.boton-primario {
  background-color: #007bff;
  color: white;
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background-color 0.2s;
}

.boton-primario:hover {
  background-color: #0056b3;
}

.boton-secundario {
  background-color: #6c757d;
  color: white;
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background-color 0.2s;
}

.boton-secundario:hover {
  background-color: #545b62;
}

.boton-primario i {
  margin-right: 0.5rem;
}
</style>

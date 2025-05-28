<template>
  <div class="gestion-sucursales">
    <h1>Gestión de Sucursales</h1>
    
    <div class="acciones-superiores">
      <button @click="mostrarModalNuevaSucursal = true" class="boton-primario">
        <i class="fas fa-plus"></i> Nueva Sucursal
      </button>
      <input type="text" v-model="busqueda" placeholder="Buscar sucursal..." class="campo-busqueda" />
    </div>
    
    <div class="tabla-contenedor">
      <table v-if="sucursalesFiltradas.length > 0" class="tabla-sucursales">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Dirección</th>
            <th>Teléfono</th>
            <th>Horario</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sucursal in sucursalesFiltradas" :key="sucursal.id">
            <td>{{ sucursal.nombre }}</td>
            <td>{{ sucursal.direccion }}</td>
            <td>{{ sucursal.telefono }}</td>
            <td>{{ sucursal.horarioAtencion }}</td>
            <td>
              <span class="estado" :class="'estado-' + (sucursal.activa ? 'activa' : 'inactiva')">
                {{ sucursal.activa ? 'Activa' : 'Inactiva' }}
              </span>
            </td>
            <td class="acciones-tabla">
              <button @click="editarSucursal(sucursal)" class="boton-icono" title="Editar">
                <i class="fas fa-edit"></i>
              </button>
              <button @click="cambiarEstadoSucursal(sucursal)" class="boton-icono" :title="sucursal.activa ? 'Desactivar' : 'Activar'">
                <i :class="['fas', sucursal.activa ? 'fa-store-slash' : 'fa-store']"></i>
              </button>
              <button @click="eliminarSucursal(sucursal)" class="boton-icono boton-eliminar" title="Eliminar">
                <i class="fas fa-trash-alt"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="mensaje-vacio">
        No se encontraron sucursales que coincidan con la búsqueda o no hay sucursales registradas.
      </div>
    </div>
    
    <!-- Modal para Nueva/Editar Sucursal -->
    <div v-if="mostrarModalNuevaSucursal || sucursalSeleccionada" class="modal-overlay">
      <div class="modal-contenido">
        <h2>{{ sucursalSeleccionada ? 'Editar Sucursal' : 'Nueva Sucursal' }}</h2>
        <form @submit.prevent="guardarSucursal">
          <div class="campo-formulario">
            <label for="nombre">Nombre</label>
            <input type="text" id="nombre" v-model="formSucursal.nombre" required />
          </div>
          <div class="campo-formulario">
            <label for="direccion">Dirección</label>
            <input type="text" id="direccion" v-model="formSucursal.direccion" required />
          </div>
          <div class="campo-formulario">
            <label for="telefono">Teléfono</label>
            <input type="tel" id="telefono" v-model="formSucursal.telefono" />
          </div>
          <div class="campo-formulario">
            <label for="horario">Horario de Atención</label>
            <input type="text" id="horario" v-model="formSucursal.horarioAtencion" placeholder="Ej: Lunes a Viernes de 9:00 a 18:00" />
          </div>
          <div class="campo-formulario">
            <label for="latitud">Latitud (Opcional)</label>
            <input type="number" step="any" id="latitud" v-model.number="formSucursal.latitud" />
          </div>
          <div class="campo-formulario">
            <label for="longitud">Longitud (Opcional)</label>
            <input type="number" step="any" id="longitud" v-model.number="formSucursal.longitud" />
          </div>
          
          <div class="acciones-modal">
            <button type="button" @click="cerrarModal" class="boton-secundario">Cancelar</button>
            <button type="submit" class="boton-primario">{{ sucursalSeleccionada ? 'Guardar Cambios' : 'Crear Sucursal' }}</button>
          </div>
        </form>
      </div>
    </div>
    
  </div>
</template>

<script>
export default {
  name: 'GestionSucursales',
  data() {
    return {
      sucursales: [],
      busqueda: '',
      mostrarModalNuevaSucursal: false,
      sucursalSeleccionada: null,
      formSucursal: {
        id: null,
        nombre: '',
        direccion: '',
        telefono: '',
        horarioAtencion: '',
        latitud: null,
        longitud: null,
        activa: true
      }
    };
  },
  computed: {
    sucursalesFiltradas() {
      if (!this.busqueda) {
        return this.sucursales;
      }
      const termino = this.busqueda.toLowerCase();
      return this.sucursales.filter(suc => 
        suc.nombre.toLowerCase().includes(termino) ||
        suc.direccion.toLowerCase().includes(termino)
      );
    }
  },
  mounted() {
    this.cargarSucursales();
  },
  methods: {
    cargarSucursales() {
      // Simulación de carga de sucursales
      setTimeout(() => {
        this.sucursales = [
          {
            id: 1,
            nombre: 'Sucursal Principal',
            direccion: 'Av. Siempreviva 742',
            telefono: '555-1234',
            horarioAtencion: 'L-V 9:00-18:00, S 9:00-13:00',
            latitud: -34.603722,
            longitud: -58.381592,
            activa: true
          },
          {
            id: 2,
            nombre: 'Sucursal Norte',
            direccion: 'Calle Falsa 123',
            telefono: '555-5678',
            horarioAtencion: 'L-V 10:00-19:00',
            latitud: -34.5410, 
            longitud: -58.4500,
            activa: true
          },
          {
            id: 3,
            nombre: 'Sucursal Oeste (Próximamente)',
            direccion: 'Boulevard de los Sueños Rotos 456',
            telefono: '555-9012',
            horarioAtencion: 'No definido',
            latitud: null,
            longitud: null,
            activa: false
          }
        ];
      }, 500);
    },
    editarSucursal(sucursal) {
      this.sucursalSeleccionada = { ...sucursal }; // Copia para evitar modificar original directamente
      this.formSucursal = { ...sucursal }; // Carga datos en el formulario
    },
    cambiarEstadoSucursal(sucursal) {
      // Lógica para cambiar estado en el backend
      const indice = this.sucursales.findIndex(s => s.id === sucursal.id);
      if (indice !== -1) {
        this.sucursales[indice].activa = !this.sucursales[indice].activa;
        this.$toast.success(`Estado de la sucursal ${sucursal.nombre} actualizado.`);
      }
    },
    eliminarSucursal(sucursal) {
      if (confirm(`¿Está seguro de eliminar la sucursal ${sucursal.nombre}? Esta acción no se puede deshacer.`)) {
        // Lógica para eliminar en el backend
        this.sucursales = this.sucursales.filter(s => s.id !== sucursal.id);
        this.$toast.success(`Sucursal ${sucursal.nombre} ha sido eliminada.`);
      }
    },
    guardarSucursal() {
      // Lógica para guardar (crear o actualizar) en el backend
      if (this.sucursalSeleccionada) { // Actualizar
        const indice = this.sucursales.findIndex(s => s.id === this.formSucursal.id);
        if (indice !== -1) {
          this.sucursales[indice] = { ...this.formSucursal };
          this.$toast.success('Sucursal actualizada correctamente.');
        }
      } else { // Crear
        const nuevoId = this.sucursales.length > 0 ? Math.max(...this.sucursales.map(s => s.id)) + 1 : 1;
        this.sucursales.push({
          id: nuevoId,
          ...this.formSucursal,
          activa: true // Por defecto, las nuevas sucursales están activas
        });
        this.$toast.success('Sucursal creada correctamente.');
      }
      this.cerrarModal();
    },
    cerrarModal() {
      this.mostrarModalNuevaSucursal = false;
      this.sucursalSeleccionada = null;
      this.formSucursal = {
        id: null,
        nombre: '',
        direccion: '',
        telefono: '',
        horarioAtencion: '',
        latitud: null,
        longitud: null,
        activa: true
      };
    }
  }
};
</script>

<style scoped>
.gestion-sucursales {
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

.tabla-sucursales {
  width: 100%;
  border-collapse: collapse;
}

.tabla-sucursales th,
.tabla-sucursales td {
  padding: 0.8rem 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
  vertical-align: middle;
}

.tabla-sucursales th {
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

.estado-activa {
  background-color: #d4edda;
  color: #155724;
}

.estado-inactiva {
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
  max-width: 600px; /* Un poco más ancho para más campos */
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

.campo-formulario input {
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

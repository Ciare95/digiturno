<template>
  <div class="gestion-servicios">
    <h1>Gestión de Servicios</h1>
    
    <div class="acciones-superiores">
      <button @click="mostrarModalNuevoServicio = true" class="boton-primario">
        <i class="fas fa-plus"></i> Nuevo Servicio
      </button>
      <input type="text" v-model="busqueda" placeholder="Buscar servicio..." class="campo-busqueda" />
    </div>
    
    <div class="tabla-contenedor">
      <table v-if="serviciosFiltrados.length > 0" class="tabla-servicios">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Descripción</th>
            <th>Duración Estimada</th>
            <th>Precio</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="servicio in serviciosFiltrados" :key="servicio.id">
            <td>{{ servicio.nombre }}</td>
            <td>{{ servicio.descripcion }}</td>
            <td>{{ servicio.duracionEstimada }} min</td>
            <td>{{ servicio.precio ? `$${servicio.precio.toFixed(2)}` : 'N/A' }}</td>
            <td>
              <span class="estado" :class="'estado-' + (servicio.activo ? 'activo' : 'inactivo')">
                {{ servicio.activo ? 'Activo' : 'Inactivo' }}
              </span>
            </td>
            <td class="acciones-tabla">
              <button @click="editarServicio(servicio)" class="boton-icono" title="Editar">
                <i class="fas fa-edit"></i>
              </button>
              <button @click="cambiarEstadoServicio(servicio)" class="boton-icono" :title="servicio.activo ? 'Desactivar' : 'Activar'">
                <i :class="['fas', servicio.activo ? 'fa-toggle-off' : 'fa-toggle-on']"></i>
              </button>
              <button @click="eliminarServicio(servicio)" class="boton-icono boton-eliminar" title="Eliminar">
                <i class="fas fa-trash-alt"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="mensaje-vacio">
        No se encontraron servicios que coincidan con la búsqueda o no hay servicios registrados.
      </div>
    </div>
    
    <!-- Modal para Nuevo/Editar Servicio -->
    <div v-if="mostrarModalNuevoServicio || servicioSeleccionado" class="modal-overlay">
      <div class="modal-contenido">
        <h2>{{ servicioSeleccionado ? 'Editar Servicio' : 'Nuevo Servicio' }}</h2>
        <form @submit.prevent="guardarServicio">
          <div class="campo-formulario">
            <label for="nombre">Nombre del Servicio</label>
            <input type="text" id="nombre" v-model="formServicio.nombre" required />
          </div>
          <div class="campo-formulario">
            <label for="descripcion">Descripción</label>
            <textarea id="descripcion" v-model="formServicio.descripcion" rows="3"></textarea>
          </div>
          <div class="campo-formulario">
            <label for="duracion">Duración Estimada (minutos)</label>
            <input type="number" id="duracion" v-model.number="formServicio.duracionEstimada" min="1" required />
          </div>
          <div class="campo-formulario">
            <label for="precio">Precio (Opcional)</label>
            <input type="number" step="0.01" id="precio" v-model.number="formServicio.precio" min="0" />
          </div>
          <div class="campo-formulario">
            <label for="requiereConfirmacion">¿Requiere confirmación previa?</label>
            <input type="checkbox" id="requiereConfirmacion" v-model="formServicio.requiereConfirmacion" />
          </div>
          
          <div class="acciones-modal">
            <button type="button" @click="cerrarModal" class="boton-secundario">Cancelar</button>
            <button type="submit" class="boton-primario">{{ servicioSeleccionado ? 'Guardar Cambios' : 'Crear Servicio' }}</button>
          </div>
        </form>
      </div>
    </div>
    
  </div>
</template>

<script>
export default {
  name: 'GestionServicios',
  data() {
    return {
      servicios: [],
      busqueda: '',
      mostrarModalNuevoServicio: false,
      servicioSeleccionado: null,
      formServicio: {
        id: null,
        nombre: '',
        descripcion: '',
        duracionEstimada: 15,
        precio: null,
        requiereConfirmacion: false,
        activo: true
      }
    };
  },
  computed: {
    serviciosFiltrados() {
      if (!this.busqueda) {
        return this.servicios;
      }
      const termino = this.busqueda.toLowerCase();
      return this.servicios.filter(serv => 
        serv.nombre.toLowerCase().includes(termino) ||
        (serv.descripcion && serv.descripcion.toLowerCase().includes(termino))
      );
    }
  },
  mounted() {
    this.cargarServicios();
  },
  methods: {
    cargarServicios() {
      // Simulación de carga de servicios
      setTimeout(() => {
        this.servicios = [
          {
            id: 1,
            nombre: 'Consulta General',
            descripcion: 'Atención médica primaria para evaluación general.',
            duracionEstimada: 20,
            precio: 50.00,
            requiereConfirmacion: false,
            activo: true
          },
          {
            id: 2,
            nombre: 'Trámite Documentario',
            descripcion: 'Gestión y seguimiento de documentos varios.',
            duracionEstimada: 30,
            precio: null,
            requiereConfirmacion: true,
            activo: true
          },
          {
            id: 3,
            nombre: 'Asesoría Legal Básica',
            descripcion: 'Orientación legal sobre temas generales.',
            duracionEstimada: 45,
            precio: 75.50,
            requiereConfirmacion: false,
            activo: false
          },
          {
            id: 4,
            nombre: 'Soporte Técnico Nivel 1',
            descripcion: 'Resolución de problemas técnicos básicos.',
            duracionEstimada: 15,
            precio: 25.00,
            requiereConfirmacion: false,
            activo: true
          }
        ];
      }, 500);
    },
    editarServicio(servicio) {
      this.servicioSeleccionado = { ...servicio };
      this.formServicio = { ...servicio };
    },
    cambiarEstadoServicio(servicio) {
      const indice = this.servicios.findIndex(s => s.id === servicio.id);
      if (indice !== -1) {
        this.servicios[indice].activo = !this.servicios[indice].activo;
        this.$toast.success(`Estado del servicio ${servicio.nombre} actualizado.`);
      }
    },
    eliminarServicio(servicio) {
      if (confirm(`¿Está seguro de eliminar el servicio ${servicio.nombre}?`)) {
        this.servicios = this.servicios.filter(s => s.id !== servicio.id);
        this.$toast.success(`Servicio ${servicio.nombre} ha sido eliminado.`);
      }
    },
    guardarServicio() {
      if (this.servicioSeleccionado) { // Actualizar
        const indice = this.servicios.findIndex(s => s.id === this.formServicio.id);
        if (indice !== -1) {
          this.servicios[indice] = { ...this.formServicio };
          this.$toast.success('Servicio actualizado correctamente.');
        }
      } else { // Crear
        const nuevoId = this.servicios.length > 0 ? Math.max(...this.servicios.map(s => s.id)) + 1 : 1;
        this.servicios.push({
          id: nuevoId,
          ...this.formServicio,
          activo: true // Por defecto, los nuevos servicios están activos
        });
        this.$toast.success('Servicio creado correctamente.');
      }
      this.cerrarModal();
    },
    cerrarModal() {
      this.mostrarModalNuevoServicio = false;
      this.servicioSeleccionado = null;
      this.formServicio = {
        id: null,
        nombre: '',
        descripcion: '',
        duracionEstimada: 15,
        precio: null,
        requiereConfirmacion: false,
        activo: true
      };
    }
  }
};
</script>

<style scoped>
.gestion-servicios {
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

.tabla-servicios {
  width: 100%;
  border-collapse: collapse;
}

.tabla-servicios th,
.tabla-servicios td {
  padding: 0.8rem 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
  vertical-align: middle;
}

.tabla-servicios th {
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
  max-width: 550px;
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

.campo-formulario input[type="text"],
.campo-formulario input[type="number"],
.campo-formulario textarea {
  width: 100%;
  padding: 0.7rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.95rem;
}

.campo-formulario input[type="checkbox"] {
  margin-right: 0.5rem;
  vertical-align: middle;
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

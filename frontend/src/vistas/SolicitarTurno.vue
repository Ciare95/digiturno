<template>
  <div class="max-w-2xl mx-auto p-4 sm:p-6 lg:p-8">
    <div class="card">
      <div v-if="turnoGenerado">
        <h2 class="card-title text-center text-green-600">¡Turno Generado Exitosamente!</h2>
        <div class="text-center bg-blue-50 p-6 rounded-lg">
          <p class="text-lg text-gray-600 mb-2">Tu código de turno es:</p>
          <p class="text-6xl font-bold text-blue-600 tracking-wider">{{ turnoGenerado.codigo_turno }}</p>
          <p class="text-md text-gray-500 mt-4">Servicio: {{ turnoGenerado.servicio.nombre }}</p>
          <p class="text-md text-gray-500">Sucursal: {{ turnoGenerado.sucursal.nombre }}</p>
        </div>
        <div class="mt-6 text-center">
          <button @click="solicitarOtroTurno" class="btn btn-primary">
            Solicitar Otro Turno
          </button>
        </div>
      </div>

      <div v-else>
        <h2 class="card-title">Solicitar un Nuevo Turno</h2>
        <p class="mb-6 text-gray-600">
          Hola, por favor selecciona una sucursal y un servicio para generar tu turno.
        </p>

        <form @submit.prevent="generarTurno">
          <div v-if="error" class="mb-4 p-3 bg-red-100 text-red-700 rounded-md">
            {{ error }}
          </div>

          <div class="form-group">
            <label for="sucursal" class="form-label">Sucursal</label>
            <select 
              id="sucursal" 
              v-model="sucursalSeleccionada"
              @change="onSucursalChange"
              class="form-input"
              required
            >
              <option disabled value="">Por favor seleccione una sucursal</option>
              <option v-for="sucursal in sucursales" :key="sucursal.id" :value="sucursal.id">
                {{ sucursal.nombre }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="servicio" class="form-label">Servicio</label>
            <select 
              id="servicio" 
              v-model="servicioSeleccionado" 
              class="form-input"
              :disabled="!sucursalSeleccionada || cargandoServicios"
              required
            >
              <option disabled value="">Por favor seleccione un servicio</option>
              <option v-if="cargandoServicios" value="">Cargando servicios...</option>
              <option v-for="servicio in servicios" :key="servicio.id" :value="servicio.id">
                {{ servicio.nombre }}
              </option>
            </select>
             <p v-if="sucursalSeleccionada && !cargandoServicios && servicios.length === 0" class="text-sm text-gray-500 mt-1">
              No hay servicios disponibles para esta sucursal.
            </p>
          </div>

          <div class="mt-6">
            <button 
              type="submit" 
              class="w-full btn btn-primary"
              :disabled="!formularioValido || cargando"
            >
              <span v-if="cargando">Generando turno...</span>
              <span v-else>Generar Turno</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

export default {
  name: 'SolicitarTurno',
  setup() {
    const store = useStore();
    const router = useRouter();

    const sucursalSeleccionada = ref('');
    const servicioSeleccionado = ref('');
    const turnoGenerado = ref(null);
    const error = ref('');
    const cargando = ref(false);
    const cargandoServicios = ref(false);

    const sucursales = computed(() => store.getters.obtenerSucursales);
    const servicios = computed(() => store.getters.obtenerServicios);
    const datosAccesoRapido = computed(() => store.state.datosAccesoRapido);

    onMounted(() => {
      if (!datosAccesoRapido.value) {
        // Si no hay datos de acceso rápido, el usuario no debería estar aquí.
        // Redirigir a la página de acceso.
        router.push('/acceso-sin-usuario');
        return;
      }
      store.dispatch('cargarSucursales');
    });

    const onSucursalChange = async () => {
      servicioSeleccionado.value = '';
      if (sucursalSeleccionada.value) {
        cargandoServicios.value = true;
        try {
          await store.dispatch('cargarServicios', sucursalSeleccionada.value);
        } catch (err) {
          error.value = 'No se pudieron cargar los servicios para esta sucursal.';
        } finally {
          cargandoServicios.value = false;
        }
      }
    };

    const generarTurno = async () => {
      cargando.value = true;
      error.value = '';
      try {
        const datosTurno = {
          sucursal: sucursalSeleccionada.value,
          servicio: servicioSeleccionado.value,
          cedula: datosAccesoRapido.value.cedula,
          telefono: datosAccesoRapido.value.telefono,
          email: datosAccesoRapido.value.email
        };
        const nuevoTurno = await store.dispatch('crearTurno', datosTurno);
        turnoGenerado.value = nuevoTurno;
      } catch (err) {
        error.value = err.message || 'Ocurrió un error al generar el turno.';
      } finally {
        cargando.value = false;
      }
    };
    
    const solicitarOtroTurno = () => {
      turnoGenerado.value = null;
      sucursalSeleccionada.value = '';
      servicioSeleccionado.value = '';
      error.value = '';
    };

    const formularioValido = computed(() => {
      return sucursalSeleccionada.value && servicioSeleccionado.value;
    });

    return {
      sucursalSeleccionada,
      servicioSeleccionado,
      sucursales,
      servicios,
      onSucursalChange,
      generarTurno,
      turnoGenerado,
      solicitarOtroTurno,
      error,
      cargando,
      cargandoServicios,
      formularioValido
    };
  }
}
</script>

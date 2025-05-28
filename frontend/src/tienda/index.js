import { createStore } from 'vuex';
import axios from 'axios';

// Configuración de axios
axios.defaults.baseURL = 'http://localhost:8000/api';
axios.defaults.headers.common['Content-Type'] = 'application/json';

// Obtener token del almacenamiento local
const token = localStorage.getItem('token');
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

// Crear tienda Vuex
export const tienda = createStore({
  state: {
    usuario: JSON.parse(localStorage.getItem('usuario')) || null,
    token: token || null,
    cargando: false,
    error: null,
    notificaciones: [],
    sucursales: [],
    servicios: [],
    turnos: [],
    estadisticas: null
  },
  
  getters: {
    estaAutenticado: state => !!state.token,
    esUsuario: state => state.usuario && state.usuario.rol === 'usuario',
    esEmpleado: state => state.usuario && state.usuario.rol === 'empleado',
    esAdministrador: state => state.usuario && state.usuario.rol === 'administrador',
    obtenerUsuario: state => state.usuario,
    obtenerError: state => state.error,
    obtenerCargando: state => state.cargando,
    obtenerNotificaciones: state => state.notificaciones,
    obtenerSucursales: state => state.sucursales,
    obtenerServicios: state => state.servicios,
    obtenerTurnos: state => state.turnos,
    obtenerEstadisticas: state => state.estadisticas
  },
  
  mutations: {
    establecerUsuario(state, usuario) {
      state.usuario = usuario;
      localStorage.setItem('usuario', JSON.stringify(usuario));
    },
    
    establecerToken(state, token) {
      state.token = token;
      localStorage.setItem('token', token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    },
    
    establecerCargando(state, valor) {
      state.cargando = valor;
    },
    
    establecerError(state, error) {
      state.error = error;
    },
    
    limpiarError(state) {
      state.error = null;
    },
    
    cerrarSesion(state) {
      state.usuario = null;
      state.token = null;
      localStorage.removeItem('usuario');
      localStorage.removeItem('token');
      delete axios.defaults.headers.common['Authorization'];
    },
    
    agregarNotificacion(state, notificacion) {
      state.notificaciones.push(notificacion);
    },
    
    eliminarNotificacion(state, id) {
      state.notificaciones = state.notificaciones.filter(n => n.id !== id);
    },
    
    establecerSucursales(state, sucursales) {
      state.sucursales = sucursales;
    },
    
    establecerServicios(state, servicios) {
      state.servicios = servicios;
    },
    
    establecerTurnos(state, turnos) {
      state.turnos = turnos;
    },
    
    establecerEstadisticas(state, estadisticas) {
      state.estadisticas = estadisticas;
    }
  },
  
  actions: {
    // Autenticación
    async iniciarSesion({ commit }, credenciales) {
      commit('establecerCargando', true);
      commit('limpiarError');
      
      try {
        const respuesta = await axios.post('/auth/login/', credenciales);
        const { usuario, token } = respuesta.data;
        
        commit('establecerUsuario', usuario);
        commit('establecerToken', token);
        return usuario;
      } catch (error) {
        commit('establecerError', error.response?.data?.message || 'Error al iniciar sesión');
        throw error;
      } finally {
        commit('establecerCargando', false);
      }
    },
    
    cerrarSesion({ commit }) {
      commit('cerrarSesion');
    },
    
    // Usuarios
    async registrarUsuario({ commit }, datosUsuario) {
      commit('establecerCargando', true);
      commit('limpiarError');
      
      try {
        const respuesta = await axios.post('/usuarios/', datosUsuario);
        return respuesta.data;
      } catch (error) {
        commit('establecerError', error.response?.data?.message || 'Error al registrar usuario');
        throw error;
      } finally {
        commit('establecerCargando', false);
      }
    },
    
    async actualizarPerfil({ commit, state }, datosPerfil) {
      commit('establecerCargando', true);
      commit('limpiarError');
      
      try {
        const respuesta = await axios.put(`/usuarios/${state.usuario.id}/`, datosPerfil);
        commit('establecerUsuario', { ...state.usuario, ...respuesta.data });
        return respuesta.data;
      } catch (error) {
        commit('establecerError', error.response?.data?.message || 'Error al actualizar perfil');
        throw error;
      } finally {
        commit('establecerCargando', false);
      }
    },
    
    // Sucursales
    async cargarSucursales({ commit }) {
      commit('establecerCargando', true);
      
      try {
        const respuesta = await axios.get('/sucursales/');
        commit('establecerSucursales', respuesta.data);
        return respuesta.data;
      } catch (error) {
        commit('establecerError', error.response?.data?.message || 'Error al cargar sucursales');
        throw error;
      } finally {
        commit('establecerCargando', false);
      }
    },
    
    // Servicios
    async cargarServicios({ commit }, sucursalId) {
      commit('establecerCargando', true);
      
      try {
        const respuesta = await axios.get(`/servicios/?sucursal=${sucursalId}`);
        commit('establecerServicios', respuesta.data);
        return respuesta.data;
      } catch (error) {
        commit('establecerError', error.response?.data?.message || 'Error al cargar servicios');
        throw error;
      } finally {
        commit('establecerCargando', false);
      }
    },
    
    // Turnos
    async crearTurno({ commit }, datosTurno) {
      commit('establecerCargando', true);
      commit('limpiarError');
      
      try {
        const respuesta = await axios.post('/turnos/', datosTurno);
        return respuesta.data;
      } catch (error) {
        commit('establecerError', error.response?.data?.message || 'Error al crear turno');
        throw error;
      } finally {
        commit('establecerCargando', false);
      }
    },
    
    async cargarTurnosUsuario({ commit, state }) {
      commit('establecerCargando', true);
      
      try {
        const respuesta = await axios.get(`/turnos/?usuario=${state.usuario.id}`);
        commit('establecerTurnos', respuesta.data);
        return respuesta.data;
      } catch (error) {
        commit('establecerError', error.response?.data?.message || 'Error al cargar turnos');
        throw error;
      } finally {
        commit('establecerCargando', false);
      }
    },
    
    async cargarTurnosEmpleado({ commit, state }) {
      commit('establecerCargando', true);
      
      try {
        const respuesta = await axios.get(`/turnos/empleado/${state.usuario.id}/`);
        commit('establecerTurnos', respuesta.data);
        return respuesta.data;
      } catch (error) {
        commit('establecerError', error.response?.data?.message || 'Error al cargar turnos');
        throw error;
      } finally {
        commit('establecerCargando', false);
      }
    },
    
    async cargarTurnosSucursal({ commit }, sucursalId) {
      commit('establecerCargando', true);
      
      try {
        const respuesta = await axios.get(`/turnos/sucursal/${sucursalId}/`);
        commit('establecerTurnos', respuesta.data);
        return respuesta.data;
      } catch (error) {
        commit('establecerError', error.response?.data?.message || 'Error al cargar turnos');
        throw error;
      } finally {
        commit('establecerCargando', false);
      }
    },
    
    async cambiarEstadoTurno({ commit }, { turnoId, estado }) {
      commit('establecerCargando', true);
      commit('limpiarError');
      
      try {
        const respuesta = await axios.patch(`/turnos/${turnoId}/`, { estado });
        return respuesta.data;
      } catch (error) {
        commit('establecerError', error.response?.data?.message || 'Error al cambiar estado del turno');
        throw error;
      } finally {
        commit('establecerCargando', false);
      }
    },
    
    // Estadísticas
    async cargarEstadisticas({ commit }, params) {
      commit('establecerCargando', true);
      
      try {
        const respuesta = await axios.get('/estadisticas/', { params });
        commit('establecerEstadisticas', respuesta.data);
        return respuesta.data;
      } catch (error) {
        commit('establecerError', error.response?.data?.message || 'Error al cargar estadísticas');
        throw error;
      } finally {
        commit('establecerCargando', false);
      }
    }
  }
});

export default tienda;

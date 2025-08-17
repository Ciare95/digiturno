// src/Services/EmpleadoService.js
import api from './api';

const API_URL = '/turns'; // ya tenemos baseURL en api

class EmpleadoService {
  async obtenerEstadisticas() {
    const { data } = await api.get(`${API_URL}/estadisticas-empleado/`);
    return data;
  }

  async obtenerTurnosPendientes() {
    try {
      const { data } = await api.get(`${API_URL}/cola-turnos-empleado/`, { params: { _: Date.now() } });
      const results = data?.results || data;
      if (Array.isArray(results)) {
        return results.map((item) => {
          const turnoData = item.turno ? {
            id: item.turno,
            numero: item.turno_numero,
            servicio: item.servicio_nombre,
            cliente: item.cliente_nombre,
            estado: item.estado_turno,
            fecha_creacion: item.fecha_creacion
          } : {
            id: item.id,
            numero: item.numero_turno,
            servicio: item.servicio_nombre,
            cliente: item.nombre_cliente,
            estado: item.estado_display,
            fecha_creacion: item.fecha_creacion
          };
          return {
            id: turnoData.id,
            numero: turnoData.numero,
            servicio: item.servicio_nombre || item.servicio?.nombre || 'Servicio no disponible',
            cliente: item.cliente_nombre || item.turno?.cliente_nombre || item.nombre_cliente || 'Cliente no disponible',
            estado: item.estado_turno || item.estado_display || 'Pendiente',
            fecha_creacion: item.turno?.fecha_creacion || item.fecha_creacion,
            rawData: item
          };
        });
      }
      return [];
    } catch (error) {
      console.error('Error getting pending turns:', error);
      return [];
    }
  }

  async obtenerTurnoActual() {
    const { data } = await api.get(`${API_URL}/turno-actual-empleado/`);
    return data ? {
      id: data.id,
      numero: data.numero_turno,
      servicio: data.servicio_nombre,
      cliente: data.nombre_cliente || 'Cliente no disponible',
      estado: data.estado_display,
      fecha_creacion: data.fecha_creacion
    } : null;
  }

  async iniciarAtencion(turnoId) {
    try {
      const payload = turnoId ? { turno_id: turnoId } : {};
      const res = await api.post(`${API_URL}/empleado/turnos/siguiente/`, payload);

      if (res.status === 204) throw new Error('No hay turnos disponibles en la cola.');

      const d = res.data;
      return {
        id: d.id,
        numero: d.numero_turno,
        servicio: d.servicio_nombre,
        cliente: d.nombre_cliente || 'Cliente no disponible',
        estado: d.estado_display,
        fecha_creacion: d.fecha_creacion,
        ventanilla: d.ventanilla
      };
    } catch (error) {
      if (error.response) {
        if (error.response.status === 400) throw new Error(error.response.data.detail || 'Error al procesar el turno');
        if (error.response.status === 404) {
          const availableTurns = error.response.data?.available_turns || [];
          throw new Error(`Turno no encontrado. Turnos disponibles: ${JSON.stringify(availableTurns)}`);
        }
      }
      throw error.message ? error : new Error('Error al procesar el turno');
    }
  }

  async finalizarAtencion(turnoId) {
    const { data } = await api.post(`${API_URL}/finalizar-atencion/`, { turno_id: turnoId });
    return {
      id: data.id,
      numero: data.numero_turno,
      servicio: data.servicio_nombre || 'Servicio no disponible',
      cliente: data.nombre_cliente || 'Cliente no disponible',
      estado: 'Atendido',
      estado_display: 'Atendido',
      fecha_creacion: data.fecha_creacion,
      hora: data.fecha_finalizacion
        ? new Date(data.fecha_finalizacion).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
        : new Date().toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' }),
      numero_turno: data.numero_turno,
      servicio_nombre: data.servicio_nombre,
      nombre_cliente: data.nombre_cliente,
      fecha_finalizacion: data.fecha_finalizacion
    };
  }

  async obtenerHistorial() {
    try {
      const { data } = await api.get(`${API_URL}/ultimos-turnos-finalizados/`);
      const list = Array.isArray(data) ? data : [data].filter(Boolean);
      return list.map((turno) => ({
        id: turno.id,
        numero: turno.numero_turno,
        servicio: turno.servicio || 'Servicio no disponible',
        cliente: turno.cliente || 'Cliente no disponible',
        estado: turno.estado || 'Finalizado',
        fecha_creacion: turno.fecha_creacion,
        hora: turno.hora || '--:--'
      }));
    } catch (error) {
      console.error('Error getting history:', error);
      return [];
    }
  }

  async transferirTurno(turnoId, nuevoServicioId) {
    try {
      const { data } = await api.post(`${API_URL}/empleado/turnos/${turnoId}/transferir/`, {
        nuevo_servicio_id: nuevoServicioId
      });
      return data;
    } catch (error) {
      if (error.response) {
        if (error.response.status === 400) throw new Error(error.response.data.detail || 'Error al transferir el turno');
        if (error.response.status === 404) throw new Error('Turno no encontrado');
      }
      throw error;
    }
  }

  async obtenerInfoEmpleado() {
    try {
      const { data } = await api.get(`/empleado/info/`);
      return data || {
        nombre: '',
        codigo_empleado: '',
        ventanilla_asignada: '',
        estado_conexion: false,
        sucursal_nombre: ''
      };
    } catch (error) {
      console.error('Error getting employee info:', error);
      return {
        nombre: '',
        codigo_empleado: '',
        ventanilla_asignada: '',
        estado_conexion: false,
        sucursal_nombre: ''
      };
    }
  }
}

export default new EmpleadoService();

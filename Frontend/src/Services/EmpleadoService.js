import axios from "axios"

const API_URL = "http://127.0.0.1:8000/api/turns"

class EmpleadoService {
  async obtenerEstadisticas() {
    const response = await axios.get(`${API_URL}/estadisticas-empleado/`)
    return response.data
  }

  async obtenerTurnosPendientes() {
    try {
      const response = await axios.get(`${API_URL}/cola-turnos-empleado/`)
      console.log('Raw API response:', response.data)
      
      if (!response.data) return []
      const results = response.data.results || response.data
      if (Array.isArray(results)) {
        const mapped = results.map(item => {
          console.log('Raw turn item:', item);
          // Handle both direct turn objects and queue items with nested turno
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
        console.log('Mapped turns:', mapped)
        return mapped
      }
      return []
    } catch (error) {
      console.error('Error getting pending turns:', error)
      return []
    }
  }

  async obtenerTurnoActual() {
    const response = await axios.get(`${API_URL}/turno-actual-empleado/`)
    return response.data ? {
      id: response.data.id,
      numero: response.data.numero_turno,
      servicio: response.data.servicio_nombre,
      cliente: response.data.nombre_cliente || 'Cliente no disponible',
      estado: response.data.estado_display,
      fecha_creacion: response.data.fecha_creacion
    } : null
  }

  async iniciarAtencion(turnoId) {
    try {
      console.log('Starting attention for turn ID:', turnoId)
      const requestData = turnoId ? { turno_id: turnoId } : {}
      
      const response = await axios.post(`${API_URL}/empleado/turnos/siguiente/`, requestData)
      console.log('Start attention response:', response.data)
      
      if (response.status === 204) {
        throw new Error("No hay turnos disponibles en la cola.")
      }

      return {
        id: response.data.id,
        numero: response.data.numero_turno,
        servicio: response.data.servicio_nombre,
        cliente: response.data.nombre_cliente || 'Cliente no disponible',
        estado: response.data.estado_display,
        fecha_creacion: response.data.fecha_creacion
      }
    } catch (error) {
      console.error('Error starting attention:', error)
      if (error.response) {
        console.error('Error response:', error.response.data);
        if (error.response.status === 400) {
          throw new Error(error.response.data.detail || 'Error al procesar el turno')
        }
        if (error.response.status === 404) {
          const availableTurns = error.response.data?.available_turns || [];
          throw new Error(`Turno no encontrado. Turnos disponibles: ${JSON.stringify(availableTurns)}`)
        }
      }
      console.error('Full error object:', error);
      throw error.message ? error : new Error('Error al procesar el turno')
    }
  }

  async finalizarAtencion(turnoId) {
    const response = await axios.post(`${API_URL}/finalizar-atencion/`, { turno_id: turnoId })
    return {
      id: response.data.id,
      numero: response.data.numero_turno,
      servicio: response.data.servicio_nombre,
      cliente: response.data.nombre_cliente || 'Cliente no disponible',
      estado: response.data.estado_display,
      fecha_creacion: response.data.fecha_creacion
    }
  }

  async obtenerHistorial() {
    try {
      const response = await axios.get(`${API_URL}/turnos/historial/`)
      return response.data ? (Array.isArray(response.data) ? response.data : [response.data]) : []
    } catch (error) {
      console.error('Error getting history:', error)
      return []
    }
  }

  async obtenerInfoEmpleado() {
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/empleado/info/")
      return response.data || {
        nombre: '',
        codigo_empleado: '',
        ventanilla_asignada: '',
        estado_conexion: false
      }
    } catch (error) {
      console.error('Error getting employee info:', error)
      return {
        nombre: '',
        codigo_empleado: '',
        ventanilla_asignada: '',
        estado_conexion: false
      }
    }
  }
}

export default new EmpleadoService()

import axios from "axios"

const API_URL = "http://127.0.0.1:8000/api"

class EmpleadoService {
  async obtenerEstadisticas() {
    const response = await axios.get(`${API_URL}/turns/estadisticas-empleado/`)
    return response.data
  }

  async obtenerTurnosPendientes() {
    try {
      const response = await axios.get(`${API_URL}/turns/cola-turnos-empleado/`)
      console.log('Turnos pendientes response:', response.data) // Debugging
      
      if (!response.data) return []
      const results = response.data.results || response.data
      if (Array.isArray(results)) {
        return results.map(item => ({
          id: item.turno?.id || item.id,
          numero: item.turno_numero || item.numero_turno,
          servicio: item.servicio_nombre || item.servicio?.nombre || 'Servicio no disponible',
          cliente: item.turno?.cliente_nombre || item.nombre_cliente || 'Cliente no disponible',
          estado: item.estado_turno || item.estado_display || 'Pendiente',
          fecha_creacion: item.turno?.fecha_creacion || item.fecha_creacion
        }))
      }
      return []
    } catch (error) {
      console.error('Error obteniendo turnos pendientes:', error)
      return []
    }
  }

  async obtenerTurnoActual() {
    const response = await axios.get(`${API_URL}/turns/turno-actual-empleado/`)
    if (response.data) {
      return {
        id: response.data.id,
        numero: response.data.numero_turno,
        servicio: response.data.servicio_nombre,
        cliente: response.data.nombre_cliente || 'Cliente no disponible',
        estado: response.data.estado_display,
        fecha_creacion: response.data.fecha_creacion
      }
    }
    return null
  }

  async iniciarAtencion(turnoId) {
    const response = await axios.post(`${API_URL}/turns/iniciar-atencion/`, { turno_id: turnoId })
    return {
      id: response.data.id,
      numero: response.data.numero_turno,
      servicio: response.data.servicio_nombre,
      cliente: response.data.nombre_cliente || 'Cliente no disponible',
      estado: response.data.estado_display,
      fecha_creacion: response.data.fecha_creacion
    }
  }

  async finalizarAtencion(turnoId) {
    const response = await axios.post(`${API_URL}/turns/finalizar-atencion/`, { turno_id: turnoId })
    return {
      id: response.data.id,
      numero: response.data.numero_turno,
      servicio: response.data.servicio_nombre,
      cliente: response.data.nombre_cliente || 'Cliente no disponible',
      estado: response.data.estado_display,
      fecha_creacion: response.data.fecha_creacion
    }
  }
}

export default new EmpleadoService()

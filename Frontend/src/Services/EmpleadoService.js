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
    const response = await axios.get(`${API_URL}/turno-actual-empleado/`)
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
    try {
      // First call the turn (set to LLAMADO state)
      const llamadoResponse = await axios.post(`${API_URL}/empleado/turnos/siguiente/`, { turno_id: turnoId })
      
      // Then start attention (set to EN_ATENCION state)
      const response = await axios.post(`${API_URL}/empleado/iniciar-atencion/`, { turno_id: llamadoResponse.data.id })
      return {
        id: response.data.id,
        numero: response.data.numero_turno,
        servicio: response.data.servicio_nombre,
        cliente: response.data.nombre_cliente || 'Cliente no disponible',
        estado: response.data.estado_display,
        fecha_creacion: response.data.fecha_creacion
      }
    } catch (error) {
      if (error.response) {
        if (error.response.status === 400 && error.response.data.detail) {
          throw new Error(error.response.data.detail)
        }
        if (error.response.status === 404) {
          throw new Error('El turno ya no está disponible. Por favor actualice la lista de turnos.')
        }
      }
      throw new Error('Error al procesar el turno. Intente nuevamente.')
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
}

export default new EmpleadoService()

import axios from "axios"

const API_URL = "http://127.0.0.1:8000/api"

class EmpleadoService {
  async obtenerEstadisticas() {
    const response = await axios.get(`${API_URL}/turns/estadisticas-empleado/`)
    return response.data
  }

  async obtenerTurnosPendientes() {
    const response = await axios.get(`${API_URL}/turns/cola-turnos-empleado/`)
    return response.data
  }

  async obtenerTurnoActual() {
    const response = await axios.get(`${API_URL}/turns/turno-actual-empleado/`)
    return response.data
  }

  async iniciarAtencion(turnoId) {
    const response = await axios.post(`${API_URL}/turns/iniciar-atencion/`, { turno_id: turnoId })
    return response.data
  }

  async finalizarAtencion(turnoId) {
    const response = await axios.post(`${API_URL}/turns/finalizar-atencion/`, { turno_id: turnoId })
    return response.data
  }
}

export default new EmpleadoService()

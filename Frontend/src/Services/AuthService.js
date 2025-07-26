import axios from "axios"

const API_URL = "http://127.0.0.1:8000/api"

class AuthService {
  async login(username, password) {
    const response = await axios.post(`${API_URL}/auth/iniciar-sesion/`, {
      username,
      password,
    })
    return response.data
  }

  async logout() {
    await axios.post(`${API_URL}/logout/`)
  }
}

export default new AuthService()
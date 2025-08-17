// src/Services/AuthService.js
import api from './api';

class AuthService {
  async login(username, password) {
    const { data } = await api.post('/auth/iniciar-sesion/', { username, password });

    // Maneja ambos mundos:
    // a) JWT: vienen access/refresh o token
    // b) Sesión por cookie: no vienen tokens (el Set-Cookie crea la sesión)
    const access = data.access || data.token || null;
    const refresh = data.refresh || null;

    if (access) localStorage.setItem('access', access);
    if (refresh) localStorage.setItem('refresh', refresh);
    localStorage.setItem('auth_mode', access ? 'jwt' : 'cookie');

    // guarda datos útiles del usuario
    localStorage.setItem('user', JSON.stringify({
      username,
      es_empleado: data.es_empleado,
      es_admin: data.es_admin,
    }));

    return { ...data };
  }

  async logout() {
    try {
      // Ajusta si tu backend expone /auth/logout/ u otra ruta
      await api.post('/logout/');
    } catch (_) {
      // even if server doesn't have endpoint, sigue con cleanup local
    } finally {
      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
      localStorage.removeItem('auth_mode');
      localStorage.removeItem('user');
    }
  }
}

export default new AuthService();
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  withCredentials: true,              // necesario si el backend usa sesión por cookie
  headers: { 'Accept': 'application/json' },
  xsrfCookieName: 'csrftoken',        // Django por defecto
  xsrfHeaderName: 'X-CSRFToken',
});

// ---- REQUEST: adjunta Bearer si hay access token ----
api.interceptors.request.use((config) => {
  const access = localStorage.getItem('access');
  if (access) config.headers.Authorization = `Bearer ${access}`;
  return config;
});

// ---- RESPONSE: auto-refresh si 401 y hay refresh token ----
let refreshing = false;
let queue = [];

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const { config, response } = error;
    if (!response) return Promise.reject(error);

    // Evita loop infinito
    if (response.status === 401 && !config.__isRetryRequest) {
      const refresh = localStorage.getItem('refresh');
      if (!refresh) return Promise.reject(error);

      // serializa refresh
      if (refreshing) {
        await new Promise((resolve) => queue.push(resolve));
      } else {
        try {
          refreshing = true;

          // Ajusta al endpoint real de tu backend (algunos usan /auth/refresh/, otros /auth/jwt/refresh/)
          const { data } = await axios.post('http://127.0.0.1:8000/api/auth/refresh/', { refresh }, {
            withCredentials: true,
            headers: { 'Accept': 'application/json' },
          });

          const newAccess = data.access || data.token;
          if (newAccess) localStorage.setItem('access', newAccess);
        } catch (e) {
          // refresh falló: limpiar sesión
          localStorage.removeItem('access');
          localStorage.removeItem('refresh');
          localStorage.removeItem('auth_mode');
          localStorage.removeItem('user');
          queue.forEach((r) => r());
          queue = [];
          refreshing = false;
          return Promise.reject(error);
        } finally {
          queue.forEach((r) => r());
          queue = [];
          refreshing = false;
        }
      }

      config.__isRetryRequest = true;
      const access = localStorage.getItem('access');
      if (access) config.headers.Authorization = `Bearer ${access}`;
      return api.request(config);
    }

    return Promise.reject(error);
  }
);

export default api;

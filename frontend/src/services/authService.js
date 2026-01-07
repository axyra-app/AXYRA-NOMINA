import api from './api'

export const authService = {
  // Registrar usuario
  signup: async (email, password, displayName) => {
    const response = await api.post('/auth/signup', {
      email,
      password,
      display_name: displayName,
    })
    return response.data
  },

  // Verificar token
  verifyToken: async (token) => {
    const response = await api.post('/auth/verify-token', null, {
      params: { token }
    })
    return response.data
  },

  // Obtener usuario actual
  getCurrentUser: async (token) => {
    const response = await api.get('/auth/me', {
      params: { token }
    })
    return response.data
  },
}

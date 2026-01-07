import axios from 'axios'

// En producción, si no hay VITE_API_URL, usar una URL relativa (mismo dominio)
const API_URL = import.meta.env.VITE_API_URL || (
  typeof window !== 'undefined' && window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : '/api'
)

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor para agregar token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Interceptor para manejo de errores
api.interceptors.response.use(
  response => response,
  error => {
    // NO hacer logout automático en 401
    // Dejar que el componente maneje el error
    // if (error.response?.status === 401) {
    //   localStorage.removeItem('authToken')
    //   window.location.href = '/auth/login'
    // }
    
    // Mejorar mensaje de error
    if (error.response?.data?.detail) {
      error.message = error.response.data.detail
    } else if (error.response?.statusText) {
      error.message = error.response.statusText
    } else if (error.code === 'ECONNABORTED') {
      error.message = 'Tiempo de conexión agotado'
    } else if (!error.response) {
      error.message = 'No hay conexión con el servidor'
    }
    
    return Promise.reject(error)
  }
)

// Función para reintentar llamadas con backoff exponencial
export const apiWithRetry = async (
  method,
  url,
  config = {},
  maxRetries = 3,
  delay = 1000
) => {
  let lastError
  
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await api({
        method,
        url,
        ...config,
      })
    } catch (error) {
      lastError = error
      
      // No reintentar en errores 4xx (excepto timeouts)
      if (error.response && error.response.status >= 400 && error.response.status < 500) {
        throw error
      }
      
      // Si es el último intento, no esperar
      if (i < maxRetries - 1) {
        const waitTime = delay * Math.pow(2, i) // Backoff exponencial
        await new Promise(resolve => setTimeout(resolve, waitTime))
      }
    }
  }
  
  throw lastError
}

export default api
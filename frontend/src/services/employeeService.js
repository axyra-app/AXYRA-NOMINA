import api from './api'

export const employeeService = {
  // Crear empleado
  create: async (clientId, employee) => {
    const response = await api.post('/employees', employee, {
      params: { client_id: clientId }
    })
    return response.data
  },

  // Listar empleados
  list: async (clientId) => {
    const response = await api.get('/employees', {
      params: { client_id: clientId }
    })
    return response.data
  },

  // Obtener empleado específico
  get: async (clientId, employeeId) => {
    const response = await api.get(`/employees/${employeeId}`, {
      params: { client_id: clientId }
    })
    return response.data
  },

  // Actualizar empleado
  update: async (clientId, employeeId, data) => {
    const response = await api.put(`/employees/${employeeId}`, data, {
      params: { client_id: clientId }
    })
    return response.data
  },

  // Eliminar empleado
  delete: async (clientId, employeeId) => {
    await api.delete(`/employees/${employeeId}`, {
      params: { client_id: clientId }
    })
  },
}

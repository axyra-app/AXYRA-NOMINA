import api from './api'

export const hoursService = {
  // Crear registro de horas
  create: async (clientId, hours) => {
    const response = await api.post('/api/hours', hours, {
      params: { client_id: clientId }
    })
    return response.data
  },

  // Obtener horas por empleado y quincena
  getByEmployeeQuincena: async (clientId, employeeId, quincena) => {
    const response = await api.get(`/api/hours/employee/${employeeId}/quincena/${quincena}`, {
      params: { client_id: clientId }
    })
    return response.data
  },

  // Actualizar horas
  update: async (clientId, hoursId, data) => {
    const response = await api.put(`/api/hours/${hoursId}`, data, {
      params: { client_id: clientId }
    })
    return response.data
  },

  // Eliminar horas
  delete: async (clientId, hoursId) => {
    await api.delete(`/api/hours/${hoursId}`, {
      params: { client_id: clientId }
    })
  },
}

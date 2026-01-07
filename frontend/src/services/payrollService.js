import api from './api'

export const payrollService = {
  // Calcular nómina de un empleado
  calculateEmployee: async (clientId, employeeId, quincena, horas) => {
    const response = await api.post(
      `/payroll/calculate/${employeeId}`,
      { horas },
      {
        params: {
          client_id: clientId,
          quincena: quincena
        }
      }
    )
    return response.data
  },

  // Calcular lote de nóminas
  calculateBatch: async (clientId, quincena, horasBatch) => {
    const response = await api.post(
      `/payroll/batch/${quincena}`,
      { horas_batch: horasBatch },
      {
        params: { client_id: clientId }
      }
    )
    return response.data
  },

  // Obtener lote específico
  getBatch: async (clientId, quincena, batchId) => {
    const response = await api.get(
      `/payroll/batch/${quincena}/${batchId}`,
      {
        params: { client_id: clientId }
      }
    )
    return response.data
  },

  // Actualizar estado del lote
  updateBatchStatus: async (clientId, quincena, batchId, newStatus) => {
    const response = await api.put(
      `/payroll/batch/${quincena}/${batchId}/status/${newStatus}`,
      {},
      {
        params: { client_id: clientId }
      }
    )
    return response.data
  },

  // Listar lotes de una quincena
  listBatches: async (clientId, quincena) => {
    const response = await api.get(
      `/payroll/batches/${quincena}`,
      {
        params: { client_id: clientId }
      }
    )
    return response.data
  },
}

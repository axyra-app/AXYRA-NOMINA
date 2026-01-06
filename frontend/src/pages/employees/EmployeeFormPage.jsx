import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowLeft, User, FileText, DollarSign, AlertCircle } from 'lucide-react'
import { employeeService } from '../../services/employeeService'

export default function EmployeeFormPage() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [formData, setFormData] = useState({
    nombre: '',
    cedula: '',
    tipo: 'FIJO',
    salario: '',
    comentario: '',
    deducir_salud: true,
    deducir_pension: true,
    deducir_auxilioTransporte: true,
    deuda_consumos: 0,
  })

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      // Validaciones básicas
      if (!formData.nombre.trim()) {
        setError('El nombre es requerido')
        setLoading(false)
        return
      }

      if (!formData.cedula.trim()) {
        setError('La cédula es requerida')
        setLoading(false)
        return
      }

      if (!formData.salario) {
        setError('El salario es requerido')
        setLoading(false)
        return
      }

      if (parseInt(formData.salario) <= 0) {
        setError('El salario debe ser mayor a 0')
        setLoading(false)
        return
      }

      // Preparar datos para envío
      const employeeData = {
        nombre: formData.nombre,
        cedula: formData.cedula,
        tipo: formData.tipo,
        salario: parseInt(formData.salario),
        comentario: formData.comentario,
        deducir_salud: formData.deducir_salud,
        deducir_pension: formData.deducir_pension,
        deducir_auxilioTransporte: formData.deducir_auxilioTransporte,
        deuda_consumos: parseFloat(formData.deuda_consumos) || 0,
      }

      // Enviar al backend
      const clientId = localStorage.getItem('client_id') || 'default-client'
      await employeeService.create(clientId, employeeData)

      // Redirigir a empleados
      navigate('/employees')
    } catch (err) {
      console.error('Error creando empleado:', err)
      setError(err.message || 'Error al crear el empleado')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="mb-8 flex items-center gap-4">
          <button
            onClick={() => navigate('/employees')}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 px-4 py-2 rounded-lg hover:bg-gray-200 transition"
          >
            <ArrowLeft size={20} />
            Volver
          </button>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Crear Empleado</h1>
            <p className="text-gray-600 mt-1">Registra un nuevo empleado en el sistema</p>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 flex items-center gap-3 bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg">
            <AlertCircle size={20} className="flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Form */}
        <div className="bg-white rounded-lg shadow p-6 space-y-6">
          {/* Información Personal */}
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
              <User size={20} />
              Información Personal
            </h2>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Nombre Completo *
              </label>
              <input
                type="text"
                name="nombre"
                value={formData.nombre}
                onChange={handleChange}
                disabled={loading}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
                placeholder="Juan Pérez"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Cédula *
              </label>
              <input
                type="text"
                name="cedula"
                value={formData.cedula}
                onChange={handleChange}
                disabled={loading}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
                placeholder="1234567890"
              />
            </div>
          </div>

          {/* Información Laboral */}
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
              <FileText size={20} />
              Información Laboral
            </h2>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Tipo de Contrato *
              </label>
              <select
                name="tipo"
                value={formData.tipo}
                onChange={handleChange}
                disabled={loading}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
              >
                <option value="FIJO">Fijo</option>
                <option value="TEMPORAL">Temporal</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Comentarios
              </label>
              <textarea
                name="comentario"
                value={formData.comentario}
                onChange={handleChange}
                disabled={loading}
                rows="3"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
                placeholder="Notas adicionales sobre el empleado..."
              />
            </div>
          </div>

          {/* Información Salarial */}
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
              <DollarSign size={20} />
              Información Salarial
            </h2>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Salario Base *
              </label>
              <input
                type="number"
                name="salario"
                value={formData.salario}
                onChange={handleChange}
                disabled={loading}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
                placeholder="1200000"
              />
              <p className="text-xs text-gray-500 mt-1">Salario mensual en COP</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Deuda de Consumos
              </label>
              <input
                type="number"
                name="deuda_consumos"
                value={formData.deuda_consumos}
                onChange={handleChange}
                disabled={loading}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
                placeholder="0"
              />
            </div>
          </div>

          {/* Deducciones - Solo para empleados FIJO */}
          {formData.tipo === 'FIJO' && (
            <div className="space-y-4">
              <h2 className="text-lg font-semibold text-gray-900">Deducciones</h2>

              <div className="space-y-3">
                <label className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    name="deducir_salud"
                    checked={formData.deducir_salud}
                    onChange={handleChange}
                    disabled={loading}
                    className="w-4 h-4 text-blue-600 rounded"
                  />
                  <span className="text-sm font-medium text-gray-700">
                    Deducir afiliación en salud (4%)
                  </span>
                </label>

                <label className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    name="deducir_pension"
                    checked={formData.deducir_pension}
                    onChange={handleChange}
                    disabled={loading}
                    className="w-4 h-4 text-blue-600 rounded"
                  />
                  <span className="text-sm font-medium text-gray-700">
                    Deducir afiliación en pensión (4%)
                  </span>
                </label>

                <label className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    name="deducir_auxilioTransporte"
                    checked={formData.deducir_auxilioTransporte}
                    onChange={handleChange}
                    disabled={loading}
                    className="w-4 h-4 text-blue-600 rounded"
                  />
                  <span className="text-sm font-medium text-gray-700">
                    Incluir auxilio de transporte
                  </span>
                </label>
              </div>
            </div>
          )}

          {/* Aviso para empleados temporales */}
          {formData.tipo === 'TEMPORAL' && (
            <div className="bg-blue-50 border border-blue-200 text-blue-700 p-4 rounded-lg">
              <p className="text-sm font-medium">
                ℹ️ Los empleados temporales no tienen deducciones de salud ni pensión.
              </p>
            </div>
          )}

          {/* Botones */}
          <div className="flex gap-4 pt-6 border-t">
            <button
              onClick={() => navigate('/employees')}
              disabled={loading}
              className="flex-1 px-6 py-3 border border-gray-300 text-gray-700 font-semibold rounded-lg hover:bg-gray-50 transition disabled:opacity-50"
            >
              Cancelar
            </button>
            <button
              onClick={handleSubmit}
              disabled={loading}
              className="flex-1 px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  Guardando...
                </>
              ) : (
                'Crear Empleado'
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

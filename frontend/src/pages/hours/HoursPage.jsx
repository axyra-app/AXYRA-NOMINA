import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Plus, Save, X, Clock, AlertCircle } from 'lucide-react';

export default function HoursPage() {
  const [employees, setEmployees] = useState([]);
  const [hours, setHours] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [message, setMessage] = useState(null);
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [formErrors, setFormErrors] = useState({});

  const [formData, setFormData] = useState({
    employee_id: '',
    fecha: new Date().toISOString().split('T')[0],
    quincena: '2026-01',
    horas_ordinarias: 0,
    recargo_nocturno: 0,
    recargo_diurno_dominical: 0,
    recargo_nocturno_dominical: 0,
    hora_extra_diurna: 0,
    hora_extra_nocturna: 0,
    hora_diurna_dominical_o_festivo: 0,
    hora_extra_diurna_dominical_o_festivo: 0,
    hora_nocturna_dominical_o_festivo: 0,
    hora_extra_nocturna_dominical_o_festivo: 0,
    motivo_deuda: '',
    valor_deuda: 0,
    notas: '',
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [empRes, hoursRes] = await Promise.all([
        axios.get(`${import.meta.env.VITE_API_URL}/api/employees`, {
          params: { client_id: 'default-client' },
        }),
        axios.get(`${import.meta.env.VITE_API_URL}/api/hours`, {
          params: { client_id: 'default-client' },
        }),
      ]);
      setEmployees(empRes.data || []);
      setHours(hoursRes.data || []);
    } catch (error) {
      const errorMsg = error.response?.data?.detail || 'Error al cargar datos';
      setMessage({ type: 'error', text: errorMsg });
    } finally {
      setLoading(false);
    }
  };

  const validateForm = () => {
    const errors = {};
    
    // Validar empleado
    if (!formData.employee_id) {
      errors.employee_id = 'Debes seleccionar un empleado';
    }
    
    // Validar período (YYYY-MM)
    if (!/^\d{4}-\d{2}$/.test(formData.quincena)) {
      errors.quincena = 'Período inválido (formato: YYYY-MM)';
    } else {
      const [year, month] = formData.quincena.split('-');
      const monthNum = parseInt(month);
      if (monthNum < 1 || monthNum > 12) {
        errors.quincena = 'El mes debe estar entre 01 y 12';
      }
    }
    
    // Validar que las horas sean no negativas
    const horasFields = [
      'horas_ordinarias', 'recargo_nocturno', 'recargo_diurno_dominical',
      'recargo_nocturno_dominical', 'hora_extra_diurna', 'hora_extra_nocturna',
      'hora_diurna_dominical_o_festivo', 'hora_extra_diurna_dominical_o_festivo',
      'hora_nocturna_dominical_o_festivo', 'hora_extra_nocturna_dominical_o_festivo'
    ];
    
    let totalHoras = 0;
    for (const field of horasFields) {
      const valor = parseFloat(formData[field]) || 0;
      if (valor < 0) {
        errors[field] = 'Las horas no pueden ser negativas';
      }
      totalHoras += valor;
    }
    
    // Validar total de horas por día
    if (totalHoras > 24) {
      errors.totalHoras = 'El total de horas no puede exceder 24 por día';
    }
    
    // Validar deuda
    if (formData.valor_deuda < 0) {
      errors.valor_deuda = 'La deuda no puede ser negativa';
    }
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleInputChange = (e) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'number' ? parseFloat(value) || 0 : value,
    }));
    // Limpiar error del campo
    if (formErrors[name]) {
      setFormErrors(prev => ({ ...prev, [name]: null }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      setMessage({ type: 'error', text: 'Por favor corrige los errores en el formulario' });
      return;
    }

    try {
      if (editingId) {
        await axios.put(
          `${import.meta.env.VITE_API_URL}/api/hours/${editingId}`,
          formData,
          { params: { client_id: 'default-client' } }
        );
        setMessage({ type: 'success', text: 'Registro actualizado' });
      } else {
        await axios.post(
          `${import.meta.env.VITE_API_URL}/api/hours`,
          formData,
          { params: { client_id: 'default-client' } }
        );
        setMessage({ type: 'success', text: 'Horas registradas' });
      }
      loadData();
      resetForm();
      setTimeout(() => setMessage(null), 3000);
    } catch (error) {
      const errorMsg = error.response?.data?.detail || 'Error al guardar registro';
      setMessage({ type: 'error', text: errorMsg });
    }
  };

  const resetForm = () => {
    setFormData({
      employee_id: '',
      fecha: new Date().toISOString().split('T')[0],
      quincena: '2026-01',
      horas_ordinarias: 0,
      recargo_nocturno: 0,
      recargo_diurno_dominical: 0,
      recargo_nocturno_dominical: 0,
      hora_extra_diurna: 0,
      hora_extra_nocturna: 0,
      hora_diurna_dominical_o_festivo: 0,
      hora_extra_diurna_dominical_o_festivo: 0,
      hora_nocturna_dominical_o_festivo: 0,
      hora_extra_nocturna_dominical_o_festivo: 0,
      motivo_deuda: '',
      valor_deuda: 0,
      notas: '',
    });
    setEditingId(null);
    setShowForm(false);
    setSelectedEmployee(null);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando datos...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <Clock className="w-8 h-8 text-blue-600" />
              <h1 className="text-3xl font-bold text-gray-900">Gestión de Horas Trabajadas</h1>
            </div>
            <p className="text-gray-600">Registra y gestiona las horas de tus empleados</p>
          </div>
          <button
            onClick={() => setShowForm(!showForm)}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
          >
            <Plus className="w-5 h-5" />
            Nueva Entrada
          </button>
        </div>

        {/* Message */}
        {message && (
          <div
            className={`mb-4 p-4 rounded-lg ${
              message.type === 'success'
                ? 'bg-green-100 text-green-800'
                : 'bg-red-100 text-red-800'
            }`}
          >
            {message.text}
          </div>
        )}

        {/* Form */}
        {showForm && (
          <div className="bg-white rounded-lg shadow p-8 mb-8">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">Registrar Horas Trabajadas</h2>
              <button onClick={resetForm} className="text-gray-500 hover:text-gray-700">
                <X className="w-6 h-6" />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Employee Selection */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Seleccionar Empleado
                </label>
                <select
                  name="employee_id"
                  value={formData.employee_id}
                  onChange={(e) => {
                    handleInputChange(e);
                    const emp = employees.find((e) => e.id === e.target.value);
                    setSelectedEmployee(emp);
                  }}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">-- Selecciona un empleado --</option>
                  {employees.map((emp) => (
                    <option key={emp.id} value={emp.id}>
                      {emp.nombre} - {emp.cedula}
                    </option>
                  ))}
                </select>
              </div>

              {/* Date and Period */}
              <div className="grid grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Fecha
                  </label>
                  <input
                    type="date"
                    name="fecha"
                    value={formData.fecha}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Quincena (YYYY-MM)
                  </label>
                  <input
                    type="text"
                    name="quincena"
                    value={formData.quincena}
                    onChange={handleInputChange}
                    placeholder="2026-01"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>

              {/* Hours Input */}
              <div className="border-t pt-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">Registro de Horas</h3>
                <div className="grid grid-cols-2 gap-4">
                  {[
                    { label: 'Horas Ordinarias', name: 'horas_ordinarias' },
                    { label: 'Recargo Nocturno', name: 'recargo_nocturno' },
                    { label: 'Recargo Diurno Dominical', name: 'recargo_diurno_dominical' },
                    { label: 'Recargo Nocturno Dominical', name: 'recargo_nocturno_dominical' },
                    { label: 'Hora Extra Diurna', name: 'hora_extra_diurna' },
                    { label: 'Hora Extra Nocturna', name: 'hora_extra_nocturna' },
                    { label: 'Hora Diurna Dominical/Festivo', name: 'hora_diurna_dominical_o_festivo' },
                    { label: 'Hora Extra Diurna Dominical/Festivo', name: 'hora_extra_diurna_dominical_o_festivo' },
                    { label: 'Hora Nocturna Dominical/Festivo', name: 'hora_nocturna_dominical_o_festivo' },
                    { label: 'Hora Extra Nocturna Dominical/Festivo', name: 'hora_extra_nocturna_dominical_o_festivo' },
                  ].map((field) => (
                    <div key={field.name}>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        {field.label}
                      </label>
                      <input
                        type="number"
                        step="0.5"
                        name={field.name}
                        value={formData[field.name]}
                        onChange={handleInputChange}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>
                  ))}
                </div>
              </div>

              {/* Debt Information */}
              <div className="border-t pt-6 bg-orange-50 p-4 rounded-lg">
                <h3 className="text-lg font-bold text-gray-900 mb-4">Información de Deuda</h3>
                <div className="grid grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Motivo de Deuda
                    </label>
                    <input
                      type="text"
                      name="motivo_deuda"
                      value={formData.motivo_deuda}
                      onChange={handleInputChange}
                      placeholder="Ej: Consumos"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Valor de Deuda
                    </label>
                    <input
                      type="number"
                      name="valor_deuda"
                      value={formData.valor_deuda}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>
              </div>

              {/* Notes */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Notas (Opcional)
                </label>
                <textarea
                  name="notas"
                  value={formData.notas}
                  onChange={handleInputChange}
                  rows="3"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              {/* Buttons */}
              <div className="flex gap-2 justify-end">
                <button
                  type="button"
                  onClick={resetForm}
                  className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
                >
                  <Save className="w-5 h-5" />
                  Guardar Registro
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Hours History */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="p-6 border-b">
            <h2 className="text-2xl font-bold text-gray-900">Historial de Horas</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-100">
                <tr>
                  <th className="px-6 py-3 text-left font-semibold text-gray-700">Empleado</th>
                  <th className="px-6 py-3 text-left font-semibold text-gray-700">Fecha</th>
                  <th className="px-6 py-3 text-left font-semibold text-gray-700">Total Horas</th>
                  <th className="px-6 py-3 text-left font-semibold text-gray-700">Total Valor</th>
                  <th className="px-6 py-3 text-left font-semibold text-gray-700">Quincena</th>
                </tr>
              </thead>
              <tbody>
                {hours.length > 0 ? (
                  hours.map((h) => (
                    <tr key={h.id} className="border-b hover:bg-gray-50">
                      <td className="px-6 py-4 font-medium text-gray-900">{h.employee_name}</td>
                      <td className="px-6 py-4 text-gray-600">{h.fecha}</td>
                      <td className="px-6 py-4 text-gray-600">{h.total_horas}</td>
                      <td className="px-6 py-4 text-gray-600">${h.total_valor.toLocaleString()}</td>
                      <td className="px-6 py-4 text-gray-600">{h.quincena}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="5" className="px-6 py-8 text-center text-gray-600">
                      No hay registros de horas. Crea uno para empezar.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

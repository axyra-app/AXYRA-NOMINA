import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Plus, Trash2, Edit, Save, X, AlertCircle } from 'lucide-react';

export default function EmployeesPage() {
  const navigate = useNavigate()
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [message, setMessage] = useState(null);
  const [formErrors, setFormErrors] = useState({});

  const [formData, setFormData] = useState({
    nombre: '',
    cedula: '',
    tipo: 'FIJO',
    salario: 0,
    comentario: '',
    deducir_salud: true,
    deducir_pension: true,
    deducir_auxilioTransporte: true,
    deuda_consumos: 0,
  });

  useEffect(() => {
    loadEmployees();
  }, []);

  const loadEmployees = async () => {
    try {
      setLoading(true);
      const response = await axios.get(
        `${import.meta.env.VITE_API_URL}/employees`,
        { params: { client_id: 'default-client' } }
      );
      setEmployees(response.data || []);
    } catch (error) {
      const errorMsg = error.response?.data?.detail || 'Error al cargar empleados';
      setMessage({ type: 'error', text: errorMsg });
    } finally {
      setLoading(false);
    }
  };

  const validateForm = () => {
    const errors = {};
    
    // Validar nombre
    if (!formData.nombre || formData.nombre.length < 2) {
      errors.nombre = 'El nombre debe tener al menos 2 caracteres';
    }
    if (formData.nombre.length > 100) {
      errors.nombre = 'El nombre no puede exceder 100 caracteres';
    }
    
    // Validar cédula
    if (!formData.cedula || !/^\d{5,20}$/.test(formData.cedula)) {
      errors.cedula = 'La cédula debe ser numérica (5-20 dígitos)';
    }
    
    // Validar tipo
    if (!['FIJO', 'TEMPORAL', 'CONTRATISTA'].includes(formData.tipo)) {
      errors.tipo = 'Tipo de empleado inválido';
    }
    
    // Validar salario
    if (formData.salario < 1000000) {
      errors.salario = 'El salario debe ser mayor a 1.000.000 COP';
    }
    
    // Validar deuda
    if (formData.deuda_consumos < 0) {
      errors.deuda_consumos = 'La deuda no puede ser negativa';
    }
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : type === 'number' ? parseFloat(value) || 0 : value,
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
          `${import.meta.env.VITE_API_URL}/employees/${editingId}`,
          formData,
          { params: { client_id: 'default-client' } }
        );
        setMessage({ type: 'success', text: 'Empleado actualizado' });
      } else {
        await axios.post(
          `${import.meta.env.VITE_API_URL}/employees`,
          formData,
          { params: { client_id: 'default-client' } }
        );
        setMessage({ type: 'success', text: 'Empleado creado' });
      }
      loadEmployees();
      resetForm();
      setTimeout(() => setMessage(null), 3000);
    } catch (error) {
      const errorMsg = error.response?.data?.detail || 'Error al guardar empleado';
      setMessage({ type: 'error', text: errorMsg });
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Estás seguro de eliminar este empleado?')) {
      try {
        await axios.delete(
          `${import.meta.env.VITE_API_URL}/employees/${id}`,
          { params: { client_id: 'default-client' } }
        );
        loadEmployees();
        setMessage({ type: 'success', text: 'Empleado eliminado' });
      } catch (error) {
        const errorMsg = error.response?.data?.detail || 'Error al eliminar empleado';
        setMessage({ type: 'error', text: errorMsg });
      }
    }
  };

  const handleEdit = (employee) => {
    setFormData(employee);
    setEditingId(employee.id);
    setShowForm(true);
    setFormErrors({});
  };

  const resetForm = () => {
    setFormData({
      nombre: '',
      cedula: '',
      tipo: 'FIJO',
      salario: 0,
      comentario: '',
      deducir_salud: true,
      deducir_pension: true,
      deducir_auxilioTransporte: true,
      deuda_consumos: 0,
    });
    setEditingId(null);
    setShowForm(false);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando empleados...</p>
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
            <h1 className="text-3xl font-bold text-gray-900">Gestión de Empleados</h1>
            <p className="text-gray-600 mt-1">Total: {employees.length} empleados</p>
          </div>
          <button
            onClick={() => navigate('/employees/new')}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
          >
            <Plus className="w-5 h-5" />
            Registrar Nuevo Empleado
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
          <div className="bg-white rounded-lg shadow p-6 mb-8">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-bold">
                {editingId ? 'Editar Empleado' : 'Registrar Nuevo Empleado'}
              </h2>
              <button onClick={resetForm} className="text-gray-500 hover:text-gray-700">
                <X className="w-6 h-6" />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Nombre Completo
                  </label>
                  <input
                    type="text"
                    name="nombre"
                    value={formData.nombre}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Cédula / Identificación
                  </label>
                  <input
                    type="text"
                    name="cedula"
                    value={formData.cedula}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Tipo de Contrato
                  </label>
                  <select
                    name="tipo"
                    value={formData.tipo}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="FIJO">Fijo</option>
                    <option value="TEMPORAL">Temporal</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Salario Base
                  </label>
                  <input
                    type="number"
                    name="salario"
                    value={formData.salario}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div className="col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Comentarios (Opcional)
                  </label>
                  <textarea
                    name="comentario"
                    value={formData.comentario}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    rows="2"
                  />
                </div>
              </div>

              <div className="border-t pt-4">
                {formData.tipo === 'FIJO' ? (
                  <>
                    <h3 className="font-bold text-gray-900 mb-4">Deducciones</h3>
                    <div className="grid grid-cols-2 gap-4">
                      <label className="flex items-center gap-2">
                        <input
                          type="checkbox"
                          name="deducir_salud"
                          checked={formData.deducir_salud}
                          onChange={handleInputChange}
                          className="w-5 h-5"
                        />
                        <span className="text-gray-700">Descontar Salud (EPS)</span>
                      </label>

                      <label className="flex items-center gap-2">
                        <input
                          type="checkbox"
                          name="deducir_pension"
                          checked={formData.deducir_pension}
                          onChange={handleInputChange}
                          className="w-5 h-5"
                        />
                        <span className="text-gray-700">Descontar Pensión (AFP)</span>
                      </label>

                      <label className="flex items-center gap-2">
                        <input
                          type="checkbox"
                          name="deducir_auxilioTransporte"
                          checked={formData.deducir_auxilioTransporte}
                          onChange={handleInputChange}
                          className="w-5 h-5"
                        />
                        <span className="text-gray-700">Descontar Auxilio de Transporte</span>
                      </label>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Deuda por Consumos
                        </label>
                        <input
                          type="number"
                          name="deuda_consumos"
                          value={formData.deuda_consumos}
                          onChange={handleInputChange}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                      </div>
                    </div>
                  </>
                ) : (
                  <div className="bg-blue-50 border border-blue-200 text-blue-700 p-4 rounded-lg">
                    <p className="text-sm font-medium">
                      ℹ️ Los empleados temporales no tienen deducciones de salud ni pensión.
                    </p>
                  </div>
                )}
              </div>

              <div className="flex gap-2 justify-end">
                <button
                  type="button"
                  onClick={resetForm}
                  className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
                >
                  <Save className="w-5 h-5" />
                  {editingId ? 'Actualizar' : 'Registrar'}
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Employees Table */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="w-full">
            <thead className="bg-blue-600 text-white">
              <tr>
                <th className="px-6 py-3 text-left font-semibold">Nombre</th>
                <th className="px-6 py-3 text-left font-semibold">Cédula</th>
                <th className="px-6 py-3 text-left font-semibold">Tipo</th>
                <th className="px-6 py-3 text-left font-semibold">Salario</th>
                <th className="px-6 py-3 text-left font-semibold">Deuda</th>
                <th className="px-6 py-3 text-center font-semibold">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {employees.map((emp) => (
                <tr key={emp.id} className="border-b hover:bg-gray-50">
                  <td className="px-6 py-4 font-medium text-gray-900">{emp.nombre}</td>
                  <td className="px-6 py-4 text-gray-600">{emp.cedula}</td>
                  <td className="px-6 py-4">
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-medium ${
                        emp.tipo === 'FIJO'
                          ? 'bg-green-100 text-green-800'
                          : 'bg-yellow-100 text-yellow-800'
                      }`}
                    >
                      {emp.tipo}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-gray-600">${emp.salario.toLocaleString()}</td>
                  <td className="px-6 py-4 text-gray-600">
                    ${emp.deuda_consumos?.toLocaleString() || 0}
                  </td>
                  <td className="px-6 py-4 text-center flex gap-2 justify-center">
                    <button
                      onClick={() => handleEdit(emp)}
                      className="text-blue-600 hover:text-blue-800"
                    >
                      <Edit className="w-5 h-5" />
                    </button>
                    <button
                      onClick={() => handleDelete(emp.id)}
                      className="text-red-600 hover:text-red-800"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {employees.length === 0 && (
            <div className="p-8 text-center text-gray-600">
              No hay empleados registrados. Crea uno para empezar.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

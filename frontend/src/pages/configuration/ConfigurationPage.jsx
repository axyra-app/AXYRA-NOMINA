import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Settings, Save, RotateCcw } from 'lucide-react';

const ConfigurationPage = () => {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [activeTab, setActiveTab] = useState('company');
  const [message, setMessage] = useState(null);

  const [company, setCompany] = useState({
    empresa_nombre: '',
    empresa_nit: '',
    empresa_direccion: '',
    salario_minimo_legal: 0,
    auxilio_transporte: 0,
    descuento_salud_porcentaje: 4.0,
    descuento_pension_porcentaje: 4.0,
  });

  const [hours, setHours] = useState({
    valor_hora_ordinaria: 0,
    horas_por_config: {},
  });

  useEffect(() => {
    loadConfiguration();
  }, []);

  const loadConfiguration = async () => {
    try {
      setLoading(true);
      const response = await axios.get(
        `${import.meta.env.VITE_API_URL}/api/config/system`,
        {
          params: { client_id: 'default-client' },
        }
      );
      setCompany(response.data.company);
      setHours(response.data.hours);
      setMessage(null);
    } catch (error) {
      setMessage({ type: 'error', text: 'Error al cargar configuración' });
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCompanyChange = (field, value) => {
    setCompany((prev) => ({ ...prev, [field]: value }));
  };

  const handleHourChange = (field, value) => {
    setHours((prev) => ({ ...prev, [field]: value }));
  };

  const handleHourConfigChange = (hourType, field, value) => {
    setHours((prev) => ({
      ...prev,
      horas_por_config: {
        ...prev.horas_por_config,
        [hourType]: {
          ...prev.horas_por_config[hourType],
          [field]: value,
        },
      },
    }));
  };

  const saveCompanyConfig = async () => {
    try {
      setSaving(true);
      await axios.put(
        `${import.meta.env.VITE_API_URL}/api/config/company`,
        company,
        { params: { client_id: 'default-client' } }
      );
      setMessage({ type: 'success', text: 'Configuración de empresa guardada' });
      setTimeout(() => setMessage(null), 3000);
    } catch (error) {
      setMessage({ type: 'error', text: 'Error al guardar configuración' });
      console.error(error);
    } finally {
      setSaving(false);
    }
  };

  const saveHoursConfig = async () => {
    try {
      setSaving(true);
      await axios.put(
        `${import.meta.env.VITE_API_URL}/api/config/hours`,
        hours,
        { params: { client_id: 'default-client' } }
      );
      setMessage({ type: 'success', text: 'Configuración de horas guardada' });
      setTimeout(() => setMessage(null), 3000);
    } catch (error) {
      setMessage({ type: 'error', text: 'Error al guardar configuración' });
      console.error(error);
    } finally {
      setSaving(false);
    }
  };

  const resetDefaults = async () => {
    if (window.confirm('¿Estás seguro que deseas reiniciar todas las configuraciones a valores por defecto?')) {
      try {
        setSaving(true);
        await axios.post(
          `${import.meta.env.VITE_API_URL}/api/config/reset-defaults`,
          {},
          { params: { client_id: 'default-client' } }
        );
        loadConfiguration();
        setMessage({ type: 'success', text: 'Configuraciones reiniciadas a valores por defecto' });
      } catch (error) {
        setMessage({ type: 'error', text: 'Error al reiniciar configuraciones' });
        console.error(error);
      } finally {
        setSaving(false);
      }
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando configuración...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <Settings className="w-8 h-8 text-blue-600" />
            <h1 className="text-3xl font-bold text-gray-900">Configuración del Sistema</h1>
          </div>
          <p className="text-gray-600">Gestiona los parámetros y valores de tu empresa</p>
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

        {/* Tabs */}
        <div className="flex gap-2 mb-6 border-b">
          <button
            onClick={() => setActiveTab('company')}
            className={`px-4 py-2 font-medium ${
              activeTab === 'company'
                ? 'border-b-2 border-blue-600 text-blue-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Información de Empresa
          </button>
          <button
            onClick={() => setActiveTab('hours')}
            className={`px-4 py-2 font-medium ${
              activeTab === 'hours'
                ? 'border-b-2 border-blue-600 text-blue-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Configuración de Horas
          </button>
        </div>

        {/* Company Configuration */}
        {activeTab === 'company' && (
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h2 className="text-2xl font-bold mb-6 text-gray-900">Información de la Empresa</h2>

            <div className="grid grid-cols-2 gap-6 mb-8">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Nombre Empresa
                </label>
                <input
                  type="text"
                  value={company.empresa_nombre}
                  onChange={(e) => handleCompanyChange('empresa_nombre', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  NIT / Identificación
                </label>
                <input
                  type="text"
                  value={company.empresa_nit}
                  onChange={(e) => handleCompanyChange('empresa_nit', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div className="col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Dirección
                </label>
                <input
                  type="text"
                  value={company.empresa_direccion}
                  onChange={(e) => handleCompanyChange('empresa_direccion', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            <h3 className="text-xl font-bold mb-4 text-gray-900">Valores Económicos</h3>

            <div className="grid grid-cols-2 gap-6 mb-8">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Salario Mínimo Legal
                </label>
                <input
                  type="number"
                  value={company.salario_minimo_legal}
                  onChange={(e) =>
                    handleCompanyChange('salario_minimo_legal', parseFloat(e.target.value))
                  }
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Auxilio de Transporte
                </label>
                <input
                  type="number"
                  value={company.auxilio_transporte}
                  onChange={(e) =>
                    handleCompanyChange('auxilio_transporte', parseFloat(e.target.value))
                  }
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            <h3 className="text-xl font-bold mb-4 text-gray-900">Descuentos a Empleados</h3>

            <div className="grid grid-cols-2 gap-6 mb-8">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Descuento Salud (%)
                </label>
                <input
                  type="number"
                  step="0.1"
                  value={company.descuento_salud_porcentaje}
                  onChange={(e) =>
                    handleCompanyChange('descuento_salud_porcentaje', parseFloat(e.target.value))
                  }
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Descuento Pensión (%)
                </label>
                <input
                  type="number"
                  step="0.1"
                  value={company.descuento_pension_porcentaje}
                  onChange={(e) =>
                    handleCompanyChange('descuento_pension_porcentaje', parseFloat(e.target.value))
                  }
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            <button
              onClick={saveCompanyConfig}
              disabled={saving}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
            >
              <Save className="w-5 h-5" />
              {saving ? 'Guardando...' : 'Guardar Cambios'}
            </button>
          </div>
        )}

        {/* Hours Configuration */}
        {activeTab === 'hours' && (
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h2 className="text-2xl font-bold mb-6 text-gray-900">Configuración de Horas y Recargas</h2>

            <div className="mb-8">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Valor Hora Ordinaria
              </label>
              <input
                type="number"
                step="0.01"
                value={hours.valor_hora_ordinaria}
                onChange={(e) => handleHourChange('valor_hora_ordinaria', parseFloat(e.target.value))}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <h3 className="text-xl font-bold mb-4 text-gray-900">Recargas por Tipo de Hora</h3>

            <div className="overflow-x-auto mb-8">
              <table className="w-full">
                <thead>
                  <tr className="bg-blue-600 text-white">
                    <th className="px-4 py-2 text-left">Tipo de Hora</th>
                    <th className="px-4 py-2 text-center">Recargo (%)</th>
                    <th className="px-4 py-2 text-center">Aplica Fijos</th>
                    <th className="px-4 py-2 text-center">Aplica Temporales</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(hours.horas_por_config || {}).map(([key, config]) => (
                    <tr key={key} className="border-b hover:bg-gray-50">
                      <td className="px-4 py-2 font-medium">{config.nombre}</td>
                      <td className="px-4 py-2">
                        <input
                          type="number"
                          step="0.1"
                          value={config.recargo_porcentaje}
                          onChange={(e) =>
                            handleHourConfigChange(key, 'recargo_porcentaje', parseFloat(e.target.value))
                          }
                          className="w-20 px-2 py-1 border border-gray-300 rounded text-center"
                        />
                      </td>
                      <td className="px-4 py-2 text-center">
                        <input
                          type="checkbox"
                          checked={config.aplica_fijo}
                          onChange={(e) =>
                            handleHourConfigChange(key, 'aplica_fijo', e.target.checked)
                          }
                          className="w-5 h-5"
                        />
                      </td>
                      <td className="px-4 py-2 text-center">
                        <input
                          type="checkbox"
                          checked={config.aplica_temporal}
                          onChange={(e) =>
                            handleHourConfigChange(key, 'aplica_temporal', e.target.checked)
                          }
                          className="w-5 h-5"
                        />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="flex gap-4">
              <button
                onClick={saveHoursConfig}
                disabled={saving}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
              >
                <Save className="w-5 h-5" />
                {saving ? 'Guardando...' : 'Guardar Cambios'}
              </button>

              <button
                onClick={resetDefaults}
                disabled={saving}
                className="bg-orange-600 text-white px-6 py-2 rounded-lg hover:bg-orange-700 disabled:opacity-50 flex items-center gap-2"
              >
                <RotateCcw className="w-5 h-5" />
                Restaurar Predeterminados
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ConfigurationPage;

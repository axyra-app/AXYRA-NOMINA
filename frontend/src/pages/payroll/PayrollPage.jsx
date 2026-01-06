import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Calculator, Download, TrendingUp, AlertCircle } from 'lucide-react';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

export default function PayrollPage() {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(false);
  const [periodo, setPeriodo] = useState(
    new Date().toISOString().slice(0, 7)
  );
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [payrollResult, setPayrollResult] = useState(null);
  const [batchPayrolls, setBatchPayrolls] = useState(null);
  const [message, setMessage] = useState(null);
  const [viewType, setViewType] = useState('individual');

  useEffect(() => {
    loadEmployees();
  }, []);

  const loadEmployees = async () => {
    try {
      const response = await axios.get(
        `${import.meta.env.VITE_API_URL}/api/employees`,
        { params: { client_id: 'default-client' } }
      );
      setEmployees(response.data || []);
    } catch (error) {
      setMessage({ 
        type: 'error', 
        text: error.response?.data?.detail || 'Error cargando empleados' 
      });
    }
  };

  const validatePeriodo = (periodo) => {
    const regex = /^\d{4}-\d{2}$/;
    if (!regex.test(periodo)) {
      return false;
    }
    const [year, month] = periodo.split('-');
    const monthNum = parseInt(month);
    return monthNum >= 1 && monthNum <= 12;
  };

  const calculateIndividual = async () => {
    if (!selectedEmployee) {
      setMessage({ type: 'error', text: 'Selecciona un empleado' });
      setTimeout(() => setMessage(null), 3000);
      return;
    }

    if (!validatePeriodo(periodo)) {
      setMessage({ type: 'error', text: 'Período inválido (formato: YYYY-MM)' });
      setTimeout(() => setMessage(null), 3000);
      return;
    }

    try {
      setLoading(true);
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/api/payroll/calculate/${selectedEmployee.id}`,
        {},
        {
          params: {
            client_id: 'default-client',
            periodo: periodo,
          },
        }
      );
      setPayrollResult(response.data.data);
      setMessage({ type: 'success', text: 'Nómina calculada correctamente' });
      setTimeout(() => setMessage(null), 3000);
    } catch (error) {
      const errorMsg = error.response?.data?.detail || 'Error calculando nómina';
      setMessage({ type: 'error', text: errorMsg });
      setTimeout(() => setMessage(null), 3000);
    } finally {
      setLoading(false);
    }
  };

  const calculateBatch = async () => {
    if (!validatePeriodo(periodo)) {
      setMessage({ type: 'error', text: 'Período inválido (formato: YYYY-MM)' });
      setTimeout(() => setMessage(null), 3000);
      return;
    }

    try {
      setLoading(true);
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/api/payroll/batch-calculate`,
        {},
        {
          params: {
            client_id: 'default-client',
            periodo: periodo,
          },
        }
      );
      setBatchPayrolls(response.data);
      setMessage({
        type: 'success',
        text: `Nómina calculada para ${response.data.cantidad_empleados || response.data.length} empleados`,
      });
      setTimeout(() => setMessage(null), 3000);
    } catch (error) {
      const errorMsg = error.response?.data?.detail || 'Error en cálculo batch';
      setMessage({ type: 'error', text: errorMsg });
      setTimeout(() => setMessage(null), 3000);
    } finally {
      setLoading(false);
    }
  };

  const downloadPDF = async () => {
    try {
      const element = document.getElementById('payroll-card');
      if (!element) {
        setMessage({ type: 'error', text: 'No hay datos para descargar' });
        return;
      }

      setLoading(true);
      const canvas = await html2canvas(element, { scale: 2 });
      const imgData = canvas.toDataURL('image/png');
      
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
      
      pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
      
      const fileName = `nomina-${selectedEmployee?.nombre || 'comprobante'}-${periodo}.pdf`;
      pdf.save(fileName);
      
      setMessage({ 
        type: 'success', 
        text: 'PDF descargado correctamente' 
      });
      setTimeout(() => setMessage(null), 3000);
    } catch (error) {
      setMessage({ 
        type: 'error', 
        text: 'Error generando PDF: ' + error.message 
      });
      setTimeout(() => setMessage(null), 3000);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectEmployee = (e) => {
    const emp = employees.find((employee) => employee.id === e.target.value);
    setSelectedEmployee(emp);
    setPayrollResult(null);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center gap-3 mb-8">
          <div className="bg-blue-100 p-3 rounded-lg">
            <Calculator className="w-8 h-8 text-blue-600" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              Cálculo de Nómina
            </h1>
            <p className="text-gray-600">
              Calcula y gestiona las nóminas de tus empleados
            </p>
          </div>
        </div>

        {/* Message */}
        {message && (
          <div
            className={`mb-6 p-4 rounded-lg font-medium ${
              message.type === 'success'
                ? 'bg-green-100 text-green-800 border border-green-300'
                : message.type === 'error'
                ? 'bg-red-100 text-red-800 border border-red-300'
                : 'bg-blue-100 text-blue-800 border border-blue-300'
            }`}
          >
            {message.text}
          </div>
        )}

        {/* Tabs */}
        <div className="flex gap-2 mb-6 border-b border-gray-300">
          <button
            onClick={() => {
              setViewType('individual');
              setPayrollResult(null);
              setBatchPayrolls(null);
            }}
            className={`px-6 py-3 font-semibold transition-colors ${
              viewType === 'individual'
                ? 'border-b-2 border-blue-600 text-blue-600'
                : 'text-gray-600 hover:text-gray-800'
            }`}
          >
            Individual
          </button>
          <button
            onClick={() => {
              setViewType('batch');
              setPayrollResult(null);
              setBatchPayrolls(null);
            }}
            className={`px-6 py-3 font-semibold transition-colors ${
              viewType === 'batch'
                ? 'border-b-2 border-blue-600 text-blue-600'
                : 'text-gray-600 hover:text-gray-800'
            }`}
          >
            Lote (Todos)
          </button>
        </div>

        {/* Individual Calculation */}
        {viewType === 'individual' && (
          <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              Cálculo Individual
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Seleccionar Empleado
                </label>
                <select
                  value={selectedEmployee?.id || ''}
                  onChange={handleSelectEmployee}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">-- Selecciona un empleado --</option>
                  {employees.map((emp) => (
                    <option key={emp.id} value={emp.id}>
                      {emp.nombre} ({emp.cedula})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Quincena (YYYY-MM)
                </label>
                <input
                  type="month"
                  value={periodo}
                  onChange={(e) => setPeriodo(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div className="flex items-end">
                <button
                  onClick={calculateIndividual}
                  disabled={loading || !selectedEmployee}
                  className="w-full bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-semibold transition-colors"
                >
                  {loading ? 'Calculando...' : 'Calcular Nómina'}
                </button>
              </div>
            </div>

            {/* Results */}
            {payrollResult && (
              <div className="space-y-6" id="payroll-card">
                {/* Summary Cards */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-lg border border-blue-200">
                    <p className="text-gray-600 text-sm font-medium mb-1">
                      Total Bruto
                    </p>
                    <p className="text-3xl font-bold text-blue-600">
                      ${payrollResult.total_bruto.toLocaleString()}
                    </p>
                  </div>

                  <div className="bg-gradient-to-br from-red-50 to-red-100 p-6 rounded-lg border border-red-200">
                    <p className="text-gray-600 text-sm font-medium mb-1">
                      Total Descuentos
                    </p>
                    <p className="text-3xl font-bold text-red-600">
                      -${payrollResult.total_descuentos.toLocaleString()}
                    </p>
                  </div>

                  <div className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-lg border border-green-200">
                    <p className="text-gray-600 text-sm font-medium mb-1">
                      NETO A PAGAR
                    </p>
                    <p className="text-3xl font-bold text-green-600">
                      ${payrollResult.neto_a_pagar.toLocaleString()}
                    </p>
                  </div>
                </div>

                {/* Detalle de Horas */}
                {payrollResult.detalle && payrollResult.detalle.length > 0 && (
                  <div className="bg-gray-50 rounded-lg p-6">
                    <h3 className="font-bold text-lg mb-4 flex items-center gap-2">
                      <TrendingUp className="w-5 h-5" />
                      Detalle de Horas Trabajadas
                    </h3>
                    <div className="overflow-x-auto">
                      <table className="w-full text-sm">
                        <thead className="bg-gray-200">
                          <tr>
                            <th className="px-4 py-3 text-left font-semibold">
                              Tipo de Hora
                            </th>
                            <th className="px-4 py-3 text-right font-semibold">
                              Cantidad
                            </th>
                            <th className="px-4 py-3 text-right font-semibold">
                              Valor Unit
                            </th>
                            <th className="px-4 py-3 text-right font-semibold">
                              Recargo %
                            </th>
                            <th className="px-4 py-3 text-right font-semibold">
                              Subtotal
                            </th>
                          </tr>
                        </thead>
                        <tbody>
                          {payrollResult.detalle.map((item, idx) => (
                            <tr
                              key={idx}
                              className={`border-b ${
                                idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'
                              } hover:bg-gray-100 transition-colors`}
                            >
                              <td className="px-4 py-3 font-medium text-gray-900">
                                {item.tipo_hora}
                              </td>
                              <td className="px-4 py-3 text-right text-gray-700">
                                {item.cantidad}
                              </td>
                              <td className="px-4 py-3 text-right text-gray-700">
                                ${item.valor_unitario}
                              </td>
                              <td className="px-4 py-3 text-right text-gray-700">
                                {item.recargo_porcentaje}%
                              </td>
                              <td className="px-4 py-3 text-right font-bold text-gray-900">
                                ${item.subtotal.toLocaleString()}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}

                {/* Descuentos */}
                <div className="bg-gray-50 rounded-lg p-6">
                  <h3 className="font-bold text-lg mb-4">Descuentos Aplicados</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center py-2 border-b border-gray-200">
                      <span className="text-gray-700">Salud (EPS)</span>
                      <span className="font-semibold text-gray-900">
                        ${payrollResult.descuento_salud.toLocaleString()}
                      </span>
                    </div>
                    <div className="flex justify-between items-center py-2 border-b border-gray-200">
                      <span className="text-gray-700">Pensión (AFP)</span>
                      <span className="font-semibold text-gray-900">
                        ${payrollResult.descuento_pension.toLocaleString()}
                      </span>
                    </div>
                    <div className="flex justify-between items-center py-2 border-b border-gray-200">
                      <span className="text-gray-700">Auxilio Transporte</span>
                      <span className="font-semibold text-green-600">
                        +${payrollResult.auxilio_transporte.toLocaleString()}
                      </span>
                    </div>
                    {payrollResult.deuda_consumos > 0 && (
                      <div className="flex justify-between items-center py-2 border-b border-gray-200">
                        <span className="text-gray-700">Deuda Consumos</span>
                        <span className="font-semibold text-red-600">
                          -${payrollResult.deuda_consumos.toLocaleString()}
                        </span>
                      </div>
                    )}
                  </div>
                </div>

                {/* Download Button */}
                <button
                  onClick={downloadPDF}
                  className="w-full bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 flex items-center justify-center gap-2 font-semibold transition-colors"
                >
                  <Download className="w-5 h-5" />
                  Descargar Comprobante PDF
                </button>
              </div>
            )}
          </div>
        )}

        {/* Batch Calculation */}
        {viewType === 'batch' && (
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              Cálculo en Lote
            </h2>
            <p className="text-gray-600 mb-6">
              Calcula la nómina de todos los empleados en una sola operación
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Seleccionar Quincena
                </label>
                <input
                  type="month"
                  value={periodo}
                  onChange={(e) => setPeriodo(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div className="flex items-end">
                <button
                  onClick={calculateBatch}
                  disabled={loading}
                  className="w-full bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-semibold transition-colors"
                >
                  {loading ? 'Calculando...' : 'Calcular Nómina en Lote'}
                </button>
              </div>
            </div>

            {batchPayrolls && (
              <div className="space-y-6">
                {/* Summary Cards */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-6 rounded-lg border border-purple-200">
                    <p className="text-gray-600 text-sm font-medium mb-1">
                      Total Empleados
                    </p>
                    <p className="text-3xl font-bold text-purple-600">
                      {batchPayrolls.cantidad_empleados}
                    </p>
                  </div>

                  <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-lg border border-blue-200">
                    <p className="text-gray-600 text-sm font-medium mb-1">
                      Total Bruto
                    </p>
                    <p className="text-3xl font-bold text-blue-600">
                      $
                      {batchPayrolls.totales.total_bruto.toLocaleString()}
                    </p>
                  </div>

                  <div className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-lg border border-green-200">
                    <p className="text-gray-600 text-sm font-medium mb-1">
                      Total Neto a Pagar
                    </p>
                    <p className="text-3xl font-bold text-green-600">
                      $
                      {batchPayrolls.totales.total_neto.toLocaleString()}
                    </p>
                  </div>
                </div>

                {/* Table */}
                <div className="bg-gray-50 rounded-lg overflow-hidden">
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead className="bg-gray-200">
                        <tr>
                          <th className="px-4 py-3 text-left font-semibold">
                            Empleado
                          </th>
                          <th className="px-4 py-3 text-left font-semibold">
                            Cédula
                          </th>
                          <th className="px-4 py-3 text-left font-semibold">
                            Tipo
                          </th>
                          <th className="px-4 py-3 text-right font-semibold">
                            Total Bruto
                          </th>
                          <th className="px-4 py-3 text-right font-semibold">
                            Descuentos
                          </th>
                          <th className="px-4 py-3 text-right font-semibold">
                            Neto a Pagar
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {batchPayrolls.payrolls.map((payroll, idx) => (
                          <tr
                            key={idx}
                            className={`border-b ${
                              idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'
                            } hover:bg-blue-50 transition-colors`}
                          >
                            <td className="px-4 py-3 font-medium text-gray-900">
                              {payroll.employee_name}
                            </td>
                            <td className="px-4 py-3 text-gray-700">
                              {payroll.cedula}
                            </td>
                            <td className="px-4 py-3">
                              <span
                                className={`px-2 py-1 rounded-full text-xs font-semibold ${
                                  payroll.tipo === 'FIJO'
                                    ? 'bg-blue-100 text-blue-800'
                                    : 'bg-orange-100 text-orange-800'
                                }`}
                              >
                                {payroll.tipo}
                              </span>
                            </td>
                            <td className="px-4 py-3 text-right text-gray-700">
                              ${payroll.total_bruto.toLocaleString()}
                            </td>
                            <td className="px-4 py-3 text-right text-red-600 font-medium">
                              -${payroll.total_descuentos.toLocaleString()}
                            </td>
                            <td className="px-4 py-3 text-right font-bold text-green-600">
                              ${payroll.neto_a_pagar.toLocaleString()}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

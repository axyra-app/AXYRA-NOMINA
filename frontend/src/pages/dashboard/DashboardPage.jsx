import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Users, DollarSign, Clock, TrendingUp, AlertCircle } from 'lucide-react';

const SkeletonCard = () => (
  <div className="bg-white rounded-lg p-6 shadow animate-pulse">
    <div className="h-4 bg-gray-200 rounded w-1/3 mb-4"></div>
    <div className="h-8 bg-gray-200 rounded w-1/2"></div>
  </div>
);

const SkeletonTable = () => (
  <div className="space-y-3">
    {[1, 2, 3, 4, 5].map((i) => (
      <div key={i} className="bg-white p-4 rounded-lg animate-pulse">
        <div className="h-4 bg-gray-200 rounded w-3/4"></div>
      </div>
    ))}
  </div>
);

export default function DashboardPage() {
  const [stats, setStats] = useState({
    totalEmpleados: 0,
    totalNomina: 0,
    horasRegistradas: 0,
    nominas: [],
    loading: true
  });

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const [empRes, hoursRes, payrollRes] = await Promise.all([
        axios.get(`${import.meta.env.VITE_API_URL}/employees`, 
          { params: { client_id: 'default-client' } }).catch(() => ({ data: [] })),
        axios.get(`${import.meta.env.VITE_API_URL}/hours`, 
          { params: { client_id: 'default-client' } }).catch(() => ({ data: [] })),
        axios.get(`${import.meta.env.VITE_API_URL}/payroll/history`, 
          { params: { client_id: 'default-client' } }).catch(() => ({ data: [] }))
      ]);

      const employees = empRes.data || [];
      const hours = hoursRes.data || [];
      const payrolls = payrollRes.data || [];

      const totalNomina = employees.reduce((sum, e) => sum + (e.salario || 0), 0);

      setStats({
        totalEmpleados: employees.length,
        totalNomina,
        horasRegistradas: hours.length,
        nominas: payrolls.slice(0, 5),
        loading: false
      });
    } catch (error) {
      console.error('Error loading stats:', error);
      setStats(prev => ({ ...prev, loading: false }));
    }
  };

  if (stats.loading) {
    return (
      <div className="p-8 bg-gray-50 min-h-screen">
        <div className="max-w-7xl mx-auto">
          <div className="mb-8">
            <div className="h-8 bg-gray-200 rounded w-1/4 mb-2 animate-pulse"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2 animate-pulse"></div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {[1, 2, 3, 4].map((i) => <SkeletonCard key={i} />)}
          </div>
          <div className="bg-white rounded-lg p-6 shadow">
            <div className="h-6 bg-gray-200 rounded w-1/4 mb-6 animate-pulse"></div>
            <SkeletonTable />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 p-8 min-h-screen bg-gray-50">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">Bienvenido a tu sistema de nómina</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatCard
          icon={<Users className="w-8 h-8" />}
          title="Total Empleados"
          value={stats.totalEmpleados}
          color="blue"
        />
        <StatCard
          icon={<DollarSign className="w-8 h-8" />}
          title="Nómina Mensual"
          value={`$${(stats.totalNomina / 1000000).toFixed(1)}M`}
          color="green"
        />
        <StatCard
          icon={<Clock className="w-8 h-8" />}
          title="Registros de Horas"
          value={stats.horasRegistradas}
          color="yellow"
        />
        <StatCard
          icon={<TrendingUp className="w-8 h-8" />}
          title="Nóminas Procesadas"
          value={stats.nominas.length}
          color="purple"
        />
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <QuickActionCard 
          title="📝 Registrar Empleado"
          description="Agregar nuevo empleado al sistema"
          link="/employees"
        />
        <QuickActionCard 
          title="⏰ Registrar Horas"
          description="Registrar horas trabajadas"
          link="/hours"
        />
        <QuickActionCard 
          title="💰 Calcular Nómina"
          description="Calcular nómina de empleados"
          link="/payroll"
        />
        <QuickActionCard 
          title="⚙️ Configuración"
          description="Editar parámetros del sistema"
          link="/configuration"
        />
      </div>

      {/* Recent Payrolls */}
      {stats.nominas.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5" />
            Últimas Nóminas
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-gray-100">
                <tr>
                  <th className="px-4 py-2 text-left">Período</th>
                  <th className="px-4 py-2 text-right">Total Bruto</th>
                  <th className="px-4 py-2 text-right">Descuentos</th>
                  <th className="px-4 py-2 text-right">Neto</th>
                </tr>
              </thead>
              <tbody>
                {stats.nominas.map((payroll, idx) => (
                  <tr key={idx} className="border-b hover:bg-gray-50">
                    <td className="px-4 py-2 font-medium">{payroll.periodo || payroll.employee_name}</td>
                    <td className="px-4 py-2 text-right">${(payroll.total_bruto || 0).toLocaleString()}</td>
                    <td className="px-4 py-2 text-right">-${(payroll.total_descuentos || 0).toLocaleString()}</td>
                    <td className="px-4 py-2 text-right font-bold text-green-600">
                      ${(payroll.neto_a_pagar || 0).toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Info Alert */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 flex gap-3">
        <AlertCircle className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
        <div>
          <p className="font-medium text-blue-900">Información</p>
          <p className="text-sm text-blue-700 mt-1">
            Accede a Configuración para ajustar parámetros como descuentos y valores de horas.
          </p>
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon, title, value, color }) {
  const colors = {
    blue: 'from-blue-50 to-blue-100 border-blue-200',
    green: 'from-green-50 to-green-100 border-green-200',
    yellow: 'from-yellow-50 to-yellow-100 border-yellow-200',
    purple: 'from-purple-50 to-purple-100 border-purple-200'
  };

  const textColors = {
    blue: 'text-blue-600',
    green: 'text-green-600',
    yellow: 'text-yellow-600',
    purple: 'text-purple-600'
  };

  return (
    <div className={`bg-gradient-to-br ${colors[color]} border rounded-lg p-6`}>
      <div className="flex items-center gap-4">
        <div className={`p-3 bg-white rounded-lg ${textColors[color]}`}>
          {icon}
        </div>
        <div>
          <p className="text-gray-600 text-sm font-medium">{title}</p>
          <p className={`text-2xl font-bold mt-1 ${textColors[color]}`}>{value}</p>
        </div>
      </div>
    </div>
  );
}

function QuickActionCard({ title, description, link }) {
  return (
    <a href={link} className="block bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6 border border-gray-200">
      <h3 className="font-bold text-lg text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600 text-sm mb-4">{description}</p>
      <span className="text-blue-600 font-medium text-sm">Ir →</span>
    </a>
  );
}

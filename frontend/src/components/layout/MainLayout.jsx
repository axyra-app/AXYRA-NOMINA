import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import { LogOut, Menu, X, Settings } from 'lucide-react'
import { useState } from 'react'

export default function MainLayout({ children }) {
  const location = useLocation()
  const navigate = useNavigate()
  const { user, clearAuth } = useAuth()
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const navItems = [
    { path: '/', label: 'Dashboard', icon: '📊' },
    { path: '/employees', label: 'Empleados', icon: '👥' },
    { path: '/hours', label: 'Horas', icon: '🕒' },
    { path: '/payroll', label: 'Nómina', icon: '📋' },
    { path: '/configuration', label: 'Configuración', icon: '⚙️' },
  ]

  const handleLogout = () => {
    clearAuth()
    navigate('/login')
  }

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className={`${sidebarOpen ? 'w-64' : 'w-20'} bg-secondary text-white transition-all duration-300 flex flex-col`}>
        <div className="p-4 flex items-center justify-between border-b border-blue-700">
          {sidebarOpen && (
            <div className="flex items-center gap-3">
              <img src="/favicon.ico" alt="Axyra Logo" className="w-8 h-8" />
              <h1 className="font-bold text-lg">Axyra</h1>
            </div>
          )}
          {!sidebarOpen && <img src="/favicon.ico" alt="Axyra" className="w-8 h-8 mx-auto" />}
          <button onClick={() => setSidebarOpen(!sidebarOpen)}>
            {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>

        <nav className="flex-1 space-y-2 p-4">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center gap-3 px-4 py-2 rounded transition ${
                location.pathname === item.path
                  ? 'bg-primary'
                  : 'hover:bg-blue-700'
              }`}
            >
              <span className="text-xl">{item.icon}</span>
              {sidebarOpen && <span>{item.label}</span>}
            </Link>
          ))}
        </nav>

        <div className="p-4 border-t border-blue-700">
          <button
            onClick={handleLogout}
            className="flex items-center gap-3 w-full px-4 py-2 rounded hover:bg-blue-700 transition"
          >
            <LogOut size={20} />
            {sidebarOpen && <span>Salir</span>}
          </button>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top bar */}
        <header className="bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
          <h2 className="text-lg font-semibold text-gray-900">
            Sistema de Nómina Axyra
          </h2>
          <div className="text-sm text-gray-600">
            {user?.email}
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-auto p-6">
          {children}
        </main>
      </div>
    </div>
  )
}

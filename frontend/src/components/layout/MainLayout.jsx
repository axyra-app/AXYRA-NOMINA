import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import { LogOut, Menu, X } from 'lucide-react'
import { useState, useEffect } from 'react'

export default function MainLayout({ children }) {
  const location = useLocation()
  const navigate = useNavigate()
  const { user, clearAuth } = useAuth()
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768)

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768)
      if (window.innerWidth < 768) {
        setSidebarOpen(false)
      }
    }
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

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
      {/* Sidebar - Hidden on mobile */}
      <aside className={`${
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      } md:translate-x-0 ${
        sidebarOpen ? 'w-64' : isMobile ? 'hidden' : 'w-20'
      } bg-secondary text-white transition-all duration-300 flex flex-col fixed md:relative md:h-screen z-40 h-screen`}>
        <div className="p-4 flex items-center justify-between border-b border-blue-700">
          {(sidebarOpen || !isMobile) && (
            <div className="flex items-center gap-3">
              <img src="/favicon.ico" alt="Axyra Logo" className="w-8 h-8" />
              {sidebarOpen || !isMobile ? <h1 className="font-bold text-lg">Axyra</h1> : null}
            </div>
          )}
          {isMobile && sidebarOpen && (
            <button onClick={() => setSidebarOpen(false)} className="ml-auto">
              <X size={20} />
            </button>
          )}
        </div>

        <nav className="flex-1 space-y-2 p-4">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              onClick={() => isMobile && setSidebarOpen(false)}
              className={`flex items-center gap-3 px-4 py-2 rounded transition ${
                location.pathname === item.path
                  ? 'bg-primary'
                  : 'hover:bg-blue-700'
              }`}
            >
              <span className="text-xl">{item.icon}</span>
              {(sidebarOpen || !isMobile) && <span>{item.label}</span>}
            </Link>
          ))}
        </nav>

        <div className="p-4 border-t border-blue-700">
          <button
            onClick={handleLogout}
            className="flex items-center gap-3 w-full px-4 py-2 rounded hover:bg-blue-700 transition"
          >
            <LogOut size={20} />
            {(sidebarOpen || !isMobile) && <span>Salir</span>}
          </button>
        </div>
      </aside>

      {/* Mobile overlay */}
      {isMobile && sidebarOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-30"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden w-full">
        {/* Top bar */}
        <header className="bg-white border-b border-gray-200 px-4 md:px-6 py-3 md:py-4 flex justify-between items-center gap-4">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="md:hidden p-2 hover:bg-gray-100 rounded"
          >
            <Menu size={24} />
          </button>
          <h2 className="text-base md:text-lg font-semibold text-gray-900 flex-1">
            Sistema de Nómina Axyra
          </h2>
          <div className="text-xs md:text-sm text-gray-600 truncate">
            {user?.email}
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-auto p-3 md:p-6">
          {children}
        </main>
      </div>
    </div>
  )
}


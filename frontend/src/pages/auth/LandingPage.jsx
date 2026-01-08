import { useNavigate } from 'react-router-dom'
import { Users, Clock, FileText, BarChart3, Zap, Shield } from 'lucide-react'

export default function LandingPage() {
  const navigate = useNavigate()

  const features = [
    {
      icon: Users,
      title: 'Gestión de Empleados',
      description: 'Administra el perfil completo de tus empleados con toda la información necesaria'
    },
    {
      icon: Clock,
      title: 'Registro de Horas',
      description: 'Controla las horas trabajadas de forma fácil y precisa'
    },
    {
      icon: FileText,
      title: 'Cálculo de Nóminas',
      description: 'Genera nóminas automáticas según la legislación colombiana'
    },
    {
      icon: BarChart3,
      title: 'Reportes y Análisis',
      description: 'Visualiza datos en tiempo real con dashboards intuitivos'
    },
    {
      icon: Zap,
      title: 'Automatización',
      description: 'Procesos automatizados que ahorran tiempo y reducen errores'
    },
    {
      icon: Shield,
      title: 'Seguridad',
      description: 'Tus datos protegidos con autenticación y encriptación'
    }
  ]

  const stats = [
    { number: '100+', label: 'Empresas usando Axyra' },
    { number: '10K+', label: 'Empleados gestionados' },
    { number: '99.9%', label: 'Disponibilidad' }
  ]

  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="fixed w-full bg-white shadow-sm z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <img src="/favicon.ico" alt="Axyra Logo" className="w-10 h-10" />
            <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
              Axyra
            </h1>
          </div>
          <div className="flex gap-4">
            <button
              onClick={() => navigate('/login')}
              className="px-6 py-2 text-gray-700 hover:text-gray-900 font-medium transition"
            >
              Iniciar Sesión
            </button>
            <button
              onClick={() => navigate('/register')}
              className="px-6 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-lg font-medium hover:shadow-lg transition"
            >
              Registrarse
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div>
            <h2 className="text-5xl font-bold text-gray-900 mb-6 leading-tight">
              Gestión de Nóminas
              <span className="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent block">
                Inteligente y Fácil
              </span>
            </h2>
            <p className="text-xl text-gray-600 mb-8 leading-relaxed">
              Axyra es la solución completa para la administración de nóminas y recursos humanos. 
              Automatiza procesos, cumple con la legislación colombiana y obtén insights de tus datos.
            </p>
            <div className="flex gap-4">
              <button
                onClick={() => navigate('/register')}
                className="px-8 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-lg font-semibold hover:shadow-xl transition transform hover:scale-105"
              >
                Comenzar Ahora
              </button>
              <button
                onClick={() => navigate('/login')}
                className="px-8 py-3 border-2 border-gray-300 text-gray-700 rounded-lg font-semibold hover:border-blue-600 hover:text-blue-600 transition"
              >
                Ya tengo cuenta
              </button>
            </div>
          </div>
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl opacity-10 blur-3xl"></div>
            <div className="relative bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-8 shadow-xl">
              <div className="space-y-4">
                <div className="flex items-center gap-3 p-3 bg-white rounded-lg">
                  <Users size={20} className="text-blue-600" />
                  <div className="flex-1">
                    <p className="text-sm text-gray-600">Empleados Activos</p>
                    <p className="text-2xl font-bold text-gray-900">1,234</p>
                  </div>
                </div>
                <div className="flex items-center gap-3 p-3 bg-white rounded-lg">
                  <Clock size={20} className="text-green-600" />
                  <div className="flex-1">
                    <p className="text-sm text-gray-600">Horas Procesadas</p>
                    <p className="text-2xl font-bold text-gray-900">45,678</p>
                  </div>
                </div>
                <div className="flex items-center gap-3 p-3 bg-white rounded-lg">
                  <FileText size={20} className="text-orange-600" />
                  <div className="flex-1">
                    <p className="text-sm text-gray-600">Nóminas Generadas</p>
                    <p className="text-2xl font-bold text-gray-900">234</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gray-50 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h3 className="text-4xl font-bold text-gray-900 mb-4">
              Características Principales
            </h3>
            <p className="text-xl text-gray-600">
              Todo lo que necesitas para gestionar nóminas profesionalmente
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, idx) => {
              const IconComponent = feature.icon
              return (
                <div
                  key={idx}
                  className="bg-white p-8 rounded-xl shadow-sm hover:shadow-lg transition"
                >
                  <div className="bg-gradient-to-br from-blue-100 to-indigo-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
                    <IconComponent className="text-blue-600" size={24} />
                  </div>
                  <h4 className="text-xl font-semibold text-gray-900 mb-2">
                    {feature.title}
                  </h4>
                  <p className="text-gray-600">{feature.description}</p>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-indigo-600 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-3 gap-8 text-center">
            {stats.map((stat, idx) => (
              <div key={idx}>
                <p className="text-5xl font-bold text-white mb-2">{stat.number}</p>
                <p className="text-blue-100 text-lg">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* About Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div>
            <h3 className="text-4xl font-bold text-gray-900 mb-6">
              ¿Qué es Axyra?
            </h3>
            <p className="text-lg text-gray-600 mb-4 leading-relaxed">
              Axyra es una plataforma integral de gestión de nóminas diseñada para empresas 
              de todas los tamaños. Nuestro objetivo es simplificar la administración de recursos humanos 
              permitiendo que te enfoques en el crecimiento de tu negocio.
            </p>
            <p className="text-lg text-gray-600 mb-6 leading-relaxed">
              Cumplimos con toda la legislación laboral colombiana, incluyendo cálculos de salario, 
              deducciones y contribuciones automáticas.
            </p>
            <div className="space-y-3">
              <div className="flex items-center gap-3">
                <span className="text-red-500 text-xl">❤️</span>
                <span className="text-gray-700">Diseñado con amor para empresarios</span>
              </div>
              <div className="flex items-center gap-3">
                <Shield className="text-green-500" size={20} />
                <span className="text-gray-700">Seguridad de nivel enterprise</span>
              </div>
              <div className="flex items-center gap-3">
                <Zap className="text-yellow-500" size={20} />
                <span className="text-gray-700">Velocidad y automatización</span>
              </div>
            </div>
          </div>
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-12">
            <div className="space-y-6">
              <div className="border-l-4 border-blue-600 pl-6">
                <h4 className="font-semibold text-gray-900 mb-2">Misión</h4>
                <p className="text-gray-600">
                  Simplificar la gestión de nóminas para que los empresarios puedan enfocarse en crecer
                </p>
              </div>
              <div className="border-l-4 border-indigo-600 pl-6">
                <h4 className="font-semibold text-gray-900 mb-2">Visión</h4>
                <p className="text-gray-600">
                  Ser la plataforma número 1 de gestión de recursos humanos en América Latina
                </p>
              </div>
              <div className="border-l-4 border-purple-600 pl-6">
                <h4 className="font-semibold text-gray-900 mb-2">Valores</h4>
                <p className="text-gray-600">
                  Transparencia, confiabilidad, innovación y excelencia en cada interacción
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gray-900">
        <div className="max-w-4xl mx-auto text-center">
          <h3 className="text-4xl font-bold text-white mb-6">
            Comienza tu Prueba Gratuita Hoy
          </h3>
          <p className="text-xl text-gray-300 mb-8">
            No necesitas tarjeta de crédito. Acceso completo a todas las features.
          </p>
          <button
            onClick={() => navigate('/register')}
            className="px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-lg font-semibold hover:shadow-xl transition transform hover:scale-105 text-lg"
          >
            Registrarse Ahora
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-950 text-gray-400 py-8 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <p>&copy; 2026 Axyra - Soluciones de Nómina. Todos los derechos reservados.</p>
          <p className="mt-2 text-sm">Diseñado y desarrollado con pasión para empresarios</p>
        </div>
      </footer>
    </div>
  )
}

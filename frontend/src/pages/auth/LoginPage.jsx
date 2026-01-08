import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Mail, Lock, AlertCircle, Eye, EyeOff, FileText, ArrowLeft } from 'lucide-react'
import { useAuthStore } from '../../context/store'
import { apiWithRetry } from '../../services/api'
import { signInWithEmailAndPassword } from 'firebase/auth'
import { auth } from '../../services/firebase'

export default function LoginPage() {
  const navigate = useNavigate()
  const { setToken, setUser } = useAuthStore()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleLogin = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      if (!email || !password) {
        setError('Por favor completa todos los campos')
        setLoading(false)
        return
      }

      // Paso 1: Verificar credenciales con Firebase
      const userCredential = await signInWithEmailAndPassword(auth, email, password)
      const firebaseToken = await userCredential.user.getIdToken()
      
      // Paso 2: Llamar al backend para obtener JWT
      const response = await apiWithRetry('POST', '/api/auth/login', {
        data: { email, password }
      }, 3, 1000)
      
      const { access_token, uid, display_name } = response.data
      
      // Guardar token en localStorage
      localStorage.setItem('authToken', access_token)
      
      // Actualizar el store de autenticación
      setToken(access_token)
      setUser({
        email: email,
        uid: uid,
        displayName: display_name || email.split('@')[0]
      })
      
      navigate('/dashboard')
    } catch (err) {
      let errorMsg = 'Error al iniciar sesión'
      
      if (err.code === 'auth/user-not-found') {
        errorMsg = 'Usuario no encontrado'
      } else if (err.code === 'auth/wrong-password') {
        errorMsg = 'Contraseña incorrecta'
      } else if (err.code === 'auth/invalid-email') {
        errorMsg = 'Email inválido'
      } else if (err.response?.status === 401) {
        errorMsg = 'Email o contraseña incorrectos'
      } else if (err.response?.status === 422) {
        errorMsg = err.response?.data?.detail || 'Datos inválidos'
      } else if (err.code === 'ECONNREFUSED') {
        errorMsg = 'No se puede conectar al servidor'
      } else if (err.message === 'No hay conexión con el servidor') {
        errorMsg = 'Sin conexión con el servidor'
      } else if (err.code === 'auth/user-disabled') {
        errorMsg = 'Usuario deshabilitado'
      }
      
      setError(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-700 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-white opacity-10 rounded-full blur-3xl"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-white opacity-10 rounded-full blur-3xl"></div>
      </div>

      {/* Back button */}
      <button
        onClick={() => navigate('/')}
        className="absolute top-6 left-6 flex items-center gap-2 text-white hover:bg-white hover:bg-opacity-20 px-4 py-2 rounded-lg transition"
      >
        <ArrowLeft size={20} />
        <span>Volver</span>
      </button>

      {/* Main card */}
      <div className="w-full max-w-md relative z-10">
        {/* Animated gradient border */}
        <div className="absolute -inset-1 bg-gradient-to-r from-white via-white to-white opacity-20 rounded-2xl blur"></div>
        
        <div className="relative bg-white bg-opacity-95 backdrop-blur-sm rounded-2xl shadow-2xl p-8">
          {/* Logo and title */}
          <div className="flex flex-col items-center mb-8">
            <div className="bg-gradient-to-br from-blue-600 to-indigo-600 p-3 rounded-xl mb-4 shadow-lg">
              <FileText className="text-white" size={32} />
            </div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
              Axyra
            </h1>
            <p className="text-gray-600 text-sm mt-2">Gestión de Nóminas Inteligente</p>
          </div>

          {/* Login form */}
          <form onSubmit={handleLogin} className="space-y-5">
            {/* Error message */}
            {error && (
              <div className="flex items-center gap-3 bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg animate-shake">
                <AlertCircle size={20} className="flex-shrink-0" />
                <span className="text-sm font-medium">{error}</span>
              </div>
            )}

            {/* Email field */}
            <div>
              <label className="block text-sm font-semibold text-gray-800 mb-2">
                Correo Electrónico
              </label>
              <div className="relative">
                <Mail className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <input
                  type="email"
                  className="w-full pl-12 pr-4 py-3 bg-gray-50 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none focus:bg-white transition"
                  placeholder="tu@email.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={loading}
                />
              </div>
            </div>

            {/* Password field */}
            <div>
              <label className="block text-sm font-semibold text-gray-800 mb-2">
                Contraseña
              </label>
              <div className="relative">
                <Lock className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <input
                  type={showPassword ? 'text' : 'password'}
                  className="w-full pl-12 pr-12 py-3 bg-gray-50 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none focus:bg-white transition"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={loading}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>
            </div>

            {/* Remember me & Forgot password */}
            <div className="flex items-center justify-between text-sm">
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" className="w-4 h-4 text-blue-600 rounded" />
                <span className="text-gray-700">Recuérdame</span>
              </label>
              <a href="#" className="text-blue-600 hover:text-blue-700 font-semibold">
                ¿Olvidaste tu contraseña?
              </a>
            </div>

            {/* Submit button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-lg hover:shadow-lg hover:shadow-blue-500/50 transition transform disabled:opacity-50 disabled:cursor-not-allowed active:scale-95"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  Iniciando sesión...
                </span>
              ) : (
                'Iniciar Sesión'
              )}
            </button>
          </form>

          {/* Divider */}
          <div className="flex items-center gap-4 my-6">
            <div className="flex-1 h-px bg-gray-200"></div>
            <span className="text-gray-500 text-sm">o</span>
            <div className="flex-1 h-px bg-gray-200"></div>
          </div>

          {/* Sign up link */}
          <p className="text-center text-gray-700">
            ¿No tienes cuenta?{' '}
            <button
              onClick={() => navigate('/register')}
              className="text-blue-600 hover:text-blue-700 font-semibold hover:underline"
            >
              Registrarse aquí
            </button>
          </p>

          {/* Footer links */}
          <div className="mt-6 pt-6 border-t border-gray-200 flex gap-4 justify-center text-xs text-gray-600">
            <a href="/terms" className="hover:text-blue-600 transition">Términos y Condiciones</a>
            <span>•</span>
            <a href="/privacy" className="hover:text-blue-600 transition">Política de Privacidad</a>
          </div>
        </div>
      </div>
    </div>
  )
}

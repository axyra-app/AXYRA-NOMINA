import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useEffect } from 'react'
import { useAuth } from './hooks/useAuth'
import { useAuthStore } from './context/store'
import ErrorBoundary from './components/ErrorBoundary'

// Pages
import LandingPage from './pages/auth/LandingPage'
import LoginPage from './pages/auth/LoginPage'
import RegisterPage from './pages/auth/RegisterPage'
import DashboardPage from './pages/dashboard/DashboardPage'
import EmployeesPage from './pages/employees/EmployeesPage'
import EmployeeFormPage from './pages/employees/EmployeeFormPage'
import HoursPage from './pages/hours/HoursPage'
import PayrollPage from './pages/payroll/PayrollPage'
import ConfigurationPage from './pages/configuration/ConfigurationPage'
import TermsPage from './pages/legal/TermsPage'
import PrivacyPage from './pages/legal/PrivacyPage'

// Layout
import MainLayout from './components/layout/MainLayout'

function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth()
  return isAuthenticated ? children : <Navigate to="/login" />
}

function AppContent() {
  return (
    <Routes>
      {/* Public routes */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/terms" element={<TermsPage />} />
      <Route path="/privacy" element={<PrivacyPage />} />
    
      {/* Protected routes */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <MainLayout>
              <DashboardPage />
            </MainLayout>
          </ProtectedRoute>
        }
      />

      <Route
        path="/employees"
        element={
          <ProtectedRoute>
            <MainLayout>
              <EmployeesPage />
            </MainLayout>
          </ProtectedRoute>
        }
      />

      <Route
        path="/employees/new"
        element={
          <ProtectedRoute>
            <MainLayout>
              <EmployeeFormPage />
            </MainLayout>
          </ProtectedRoute>
        }
      />

      <Route
        path="/hours"
        element={
          <ProtectedRoute>
            <MainLayout>
              <HoursPage />
            </MainLayout>
          </ProtectedRoute>
        }
      />

      <Route
        path="/payroll"
        element={
          <ProtectedRoute>
            <MainLayout>
              <PayrollPage />
            </MainLayout>
          </ProtectedRoute>
        }
      />

      <Route
        path="/configuration"
        element={
          <ProtectedRoute>
            <MainLayout>
              <ConfigurationPage />
            </MainLayout>
          </ProtectedRoute>
        }
      />

      {/* Redirect old dashboard route */}
      <Route
        path="/old-dashboard"
        element={
          <ProtectedRoute>
            <MainLayout>
              <DashboardPage />
            </MainLayout>
          </ProtectedRoute>
        }
      />

      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  )
}

export default function App() {
  const { initializeAuth } = useAuthStore()

  useEffect(() => {
    // Inicializar autenticación al cargar la app
    initializeAuth()
  }, [initializeAuth])

  return (
    <ErrorBoundary>
      <BrowserRouter>
        <AppContent />
      </BrowserRouter>
    </ErrorBoundary>
  )
}

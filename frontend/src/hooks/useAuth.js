import { useAuthStore } from '../context/store'
import { useEffect, useCallback } from 'react'

export const useAuth = () => {
  const authStore = useAuthStore()
  return authStore
}

export const useRequireAuth = () => {
  const { isAuthenticated } = useAuthStore()

  useEffect(() => {
    if (!isAuthenticated) {
      window.location.href = '/login'
    }
  }, [isAuthenticated])

  return isAuthenticated
}

export const useAuthWithRetry = (maxRetries = 3) => {
  const authStore = useAuthStore()
  const { refreshToken } = authStore

  const retryRefreshToken = useCallback(async () => {
    for (let i = 0; i < maxRetries; i++) {
      try {
        await refreshToken()
        return true
      } catch (error) {
        if (i === maxRetries - 1) {
          // Last attempt failed, logout
          authStore.logout()
          return false
        }
        // Esperar antes de reintentar (backoff exponencial)
        await new Promise((resolve) =>
          setTimeout(resolve, Math.pow(2, i) * 1000)
        )
      }
    }
    return false
  }, [authStore, maxRetries, refreshToken])

  return {
    ...authStore,
    retryRefreshToken,
  }
}

import { create } from 'zustand'

export const useAuthStore = create((set) => ({
  user: null,
  token: localStorage.getItem('authToken'),
  isAuthenticated: !!localStorage.getItem('authToken'),
  loading: false,

  setUser: (user) => {
    set({ user })
    if (user) {
      localStorage.setItem('user', JSON.stringify(user))
    }
  },
  
  setToken: (token) => {
    localStorage.setItem('authToken', token)
    set({ token, isAuthenticated: true })
  },
  
  initializeAuth: () => {
    const token = localStorage.getItem('authToken')
    const user = localStorage.getItem('user')
    
    if (token && user) {
      set({
        token,
        user: JSON.parse(user),
        isAuthenticated: true
      })
    } else {
      set({
        token: null,
        user: null,
        isAuthenticated: false
      })
    }
  },
  
  clearAuth: () => {
    localStorage.removeItem('authToken')
    localStorage.removeItem('user')
    set({ user: null, token: null, isAuthenticated: false })
  },
  
  setLoading: (loading) => set({ loading }),
}))

export const useAppStore = create((set) => ({
  clientId: localStorage.getItem('clientId'),
  currentQuincena: null,
  employees: [],
  batches: [],

  setClientId: (id) => {
    localStorage.setItem('clientId', id)
    set({ clientId: id })
  },
  setCurrentQuincena: (quincena) => set({ currentQuincena: quincena }),
  setEmployees: (employees) => set({ employees }),
  setBatches: (batches) => set({ batches }),
}))

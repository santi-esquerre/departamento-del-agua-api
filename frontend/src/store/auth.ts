import { create } from 'zustand'

export interface Personal {
  id: number
  nombre: string
  cargo: string
  descripcion?: string
  foto_url?: string
  cv_url?: string
  orcid?: string
  email: string
  fecha_alta: string // ISO date “YYYY-MM-DD”
}

interface AuthState {
  token: string | null
  personal: Personal | null
  setToken: (t: string) => void
  clearToken: () => void
  setPersonal: (p: Personal) => void
  clearPersonal: () => void
}

const storedToken = localStorage.getItem('auth_token')
const storedPersonal = localStorage.getItem('auth_personal')

export const useAuthStore = create<AuthState>((set) => ({
  token: storedToken,
  personal: storedPersonal ? JSON.parse(storedPersonal) : null,
  setToken: (t) => {
    localStorage.setItem('auth_token', t)
    set({ token: t })
  },
  clearToken: () => {
    localStorage.removeItem('auth_token')
    set({ token: null })
  },
  setPersonal: (p) => {
    localStorage.setItem('auth_personal', JSON.stringify(p))
    set({ personal: p })
  },
  clearPersonal: () => {
    localStorage.removeItem('auth_personal')
    set({ personal: null })
  },
}))

export const getToken = () => useAuthStore.getState().token
export const clearToken = () => useAuthStore.getState().clearToken()
export const getPersonal = () => useAuthStore.getState().personal
export const clearPersonal = () => useAuthStore.getState().clearPersonal()

// frontend/src/lib/client.ts
import axios from 'axios'
import { getToken, clearToken } from '@/store/auth'

const api = axios.create({
  baseURL: "https://localhost/api", // Cambia esto por tu URL base
  withCredentials: true,
})

api.interceptors.request.use(config => {
  const token = getToken()
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  res => res,
  err => {
    const status = err.response?.status
    const url = err.config.url || ''
    const isLoginEndpoint = url.includes('/auth/login')

    if (status === 401 && !isLoginEndpoint) {
      clearToken()
      window.location.replace('/login')
    }
    return Promise.reject(err)
  }
)

export default api

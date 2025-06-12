// frontend/src/lib/auth.ts
import api from './client'

export interface LoginRequest { username: string; password: string }
export interface LoginResponse { access_token: string; token_type: 'bearer' }

export function loginAdmin(data: LoginRequest) {
  return api.post<LoginResponse>('/auth/login', data)
}

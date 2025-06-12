// frontend/src/types/auth.ts
export interface LoginRequest { username: string; password: string }
export interface LoginResponse { access_token: string; token_type: 'bearer' }

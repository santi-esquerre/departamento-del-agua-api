// frontend/src/lib/api.ts
import api from '@/lib/client'

// auth
export function loginAdmin(data: { email: string; password: string }) {
  return api.post('/auth/login', data)
}

// si necesitas mantener tu función de estudiantes:
export async function getStudents(offset: number, pageLimit: number, country: string) {
  const res = await api.get(`/sample-data/users?offset=${offset}&limit=${pageLimit}` + (country ? `&search=${country}` : ''))
  return res.data
}

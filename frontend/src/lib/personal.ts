// frontend/src/lib/personal.ts
import api from './client'
import type { Personal } from '@/store/auth'

export async function fetchPersonales(): Promise<Personal[]> {
  const { data } = await api.get<Personal[]>('/personal')
  return data
}

export async function createPersonal(data: Omit<Personal, 'id'>): Promise<Personal> {
  const res = await api.post<Personal>('/personal', data)
  return res.data
}

// actualizar personal
export async function updatePersonal(id: number, data: Partial<Personal>) {
  const res = await api.put<Personal>(`/personal/${id}`, data)
  return res.data
}

// borrar personal
export async function deletePersonal(id: number) {
  await api.delete(`/personal/${id}`)
}


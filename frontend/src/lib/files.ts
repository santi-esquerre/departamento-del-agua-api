import api from './client'

/**
 * Sube un archivo (foto o CV) y devuelve { id, url }
 */
export async function uploadFile(file: File) {
  const form = new FormData()
  form.append('file', file)
  const { data } = await api.post<{ id: number; ruta: string }>(
    '/archivos/upload',
    form,
    { headers: { 'Content-Type': 'multipart/form-data' } }
  )
  return data
}

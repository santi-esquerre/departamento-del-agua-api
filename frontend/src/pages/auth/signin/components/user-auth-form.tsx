// frontend/src/pages/auth/signin/components/user-auth-form.tsx
import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { useRouter } from '@/routes/hooks'
import { loginAdmin } from '@/lib/auth'
import { useAuthStore } from '@/store/auth'
import { toast } from '@/components/ui/use-toast'
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'

const schema = z.object({
  username: z.string().min(1, { message: 'El usuario es requerido' }),
  password: z.string().min(1, { message: 'La contraseña es requerida' }),
})
type FormData = z.infer<typeof schema>

export default function UserAuthForm() {
  const router = useRouter()
  const setToken = useAuthStore(state => state.setToken)
  const [loading, setLoading] = useState(false)

  const form = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: { username: '', password: '' },
  })

  const onSubmit = async (data: FormData) => {
    setLoading(true)
    try {
      const res = await loginAdmin({ username: data.username, password: data.password })
      setToken(res.data.access_token)
      toast({ title: 'Inicio de sesión exitoso' })
      router.replace('/identidad')
    } catch (err) {
      toast({ variant: 'destructive', title: 'Error', description: 'Credenciales incorrectas' })
      form.reset({ ...form.getValues(), password: '' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="username"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Usuario</FormLabel>
              <FormControl>
                <Input placeholder="Tu usuario" disabled={loading} {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Contraseña</FormLabel>
              <FormControl>
                <Input type="password" placeholder="••••••••" disabled={loading} {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" disabled={loading} className="w-full">
          {loading ? 'Validando…' : 'Iniciar sesión'}
        </Button>
      </form>
    </Form>
  )
}

// frontend/src/pages/identidad/index.tsx
import { useEffect, useState } from 'react';
import { fetchPersonales, createPersonal } from '@/lib/personal';
import { useAuthStore } from '@/store/auth';
import { useRouter } from '@/routes/hooks';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle
} from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { toast } from '@/components/ui/use-toast';
import type { Personal } from '@/store/auth';

export default function IdentidadPage() {
  const router = useRouter();
  const setPersonal = useAuthStore((s) => s.setPersonal);
  const [list, setList] = useState<Personal[]>([]);
  const [nuevo, setNuevo] = useState(false);
  const [loading, setLoading] = useState(false);

  const [form, setForm] = useState<Omit<Personal, 'id'>>({
    nombre: '',
    cargo: '',
    descripcion: '',
    foto_url: '',
    cv_url: '',
    orcid: '',
    email: '',
    fecha_alta: new Date().toISOString().slice(0, 10) // hoy
  });

  useEffect(() => {
    fetchPersonales()
      .then(setList)
      .catch(() =>
        toast({ variant: 'destructive', title: 'Error cargando identidades' })
      );
  }, []);

  const onSelect = (p: Personal) => {
    setPersonal(p);
    router.replace('/dashboard');
  };

  const onSubmitNuevo = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const created = await createPersonal(form);
      setList([...list, created]);
      toast({ title: 'Identidad creada' });
      setPersonal(created);
      router.replace('/dashboard');
    } catch {
      toast({ variant: 'destructive', title: 'No se pudo crear' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-4xl space-y-8 py-12">
      <h1 className="text-center text-3xl font-semibold">
        Seleccioná tu identidad
      </h1>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 md:grid-cols-3">
        {list.map((p) => (
          <Card
            key={p.id}
            onClick={() => onSelect(p)}
            className="cursor-pointer hover:shadow-lg"
          >
            <CardHeader>
              <CardTitle>{p.nombre}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-1">
              <p className="text-sm font-medium">{p.cargo}</p>
              <p className="line-clamp-3 text-xs text-muted-foreground">
                {p.descripcion}
              </p>
            </CardContent>
            <CardFooter className="flex items-center justify-between">
              {p.foto_url && (
                <img
                  src={p.foto_url}
                  alt={p.nombre}
                  className="h-10 w-10 rounded-full object-cover"
                />
              )}
              <Button size="sm" variant="secondary">
                Seleccionar
              </Button>
            </CardFooter>
          </Card>
        ))}

        <Card
          onClick={() => setNuevo(true)}
          className="flex items-center justify-center border-dashed"
        >
          <div className="text-muted-foreground">+ Nueva identidad</div>
        </Card>
      </div>

      {nuevo && (
        <form onSubmit={onSubmitNuevo} className="mx-auto max-w-md space-y-4">
          <Input
            required
            placeholder="Nombre completo"
            value={form.nombre}
            onChange={(e) => setForm({ ...form, nombre: e.target.value })}
          />
          <Input
            required
            placeholder="Cargo"
            value={form.cargo}
            onChange={(e) => setForm({ ...form, cargo: e.target.value })}
          />
          <Textarea
            required
            placeholder="Descripción breve"
            value={form.descripcion}
            onChange={(e) => setForm({ ...form, descripcion: e.target.value })}
          />
          <Input
            required
            type="email"
            placeholder="Email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
          />
          <Input
            placeholder="URL de foto"
            value={form.foto_url}
            onChange={(e) => setForm({ ...form, foto_url: e.target.value })}
          />
          <Input
            placeholder="URL de CV"
            value={form.cv_url}
            onChange={(e) => setForm({ ...form, cv_url: e.target.value })}
          />
          <Input
            placeholder="ORCID"
            value={form.orcid}
            onChange={(e) => setForm({ ...form, orcid: e.target.value })}
          />
          <Input
            required
            type="date"
            placeholder="Fecha de alta"
            value={form.fecha_alta}
            onChange={(e) => setForm({ ...form, fecha_alta: e.target.value })}
          />

          <div className="flex justify-end gap-2">
            <Button
              type="button"
              variant="outline"
              onClick={() => setNuevo(false)}
            >
              Cancelar
            </Button>
            <Button type="submit" disabled={loading}>
              {loading ? 'Creando…' : 'Crear identidad'}
            </Button>
          </div>
        </form>
      )}
    </div>
  );
}

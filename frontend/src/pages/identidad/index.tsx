// frontend/src/pages/identidad/index.tsx
import { useEffect, useState } from 'react';
import { fetchPersonales, createPersonal } from '@/lib/personal';
import { uploadFile } from '@/lib/files';
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

  // Para foto
  const [fotoFile, setFotoFile] = useState<File | null>(null);

  // Para CV: opción, enlace y archivo
  const [cvOption, setCvOption] = useState<'link' | 'upload'>('link');
  const [cvLink, setCvLink] = useState('');
  const [cvFile, setCvFile] = useState<File | null>(null);

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
      // 1) Subir FOTO si hay
      let fotoUrl = '';
      if (fotoFile) {
        const { ruta } = await uploadFile(fotoFile);
        fotoUrl = ruta;
      }

      // 2) Determinar URL de CV
      let cvUrl = '';
      if (cvOption === 'link') {
        cvUrl = cvLink.trim();
      } else if (cvOption === 'upload' && cvFile) {
        const { ruta } = await uploadFile(cvFile);
        cvUrl = ruta;
      }

      // 3) Crear Personal con todos los campos
      const nuevoPersonal = await createPersonal({
        ...form, // nombre, cargo, descripción, email, fecha_alta, etc.
        foto_url: fotoUrl,
        cv_url: cvUrl
      });

      // console.log('Nuevo personal creado:', nuevoPersonal);

      // 4) Continuar flujo
      setList([...list, nuevoPersonal]);
      setPersonal(nuevoPersonal);
      toast({ title: 'Identidad creada' });
      router.replace('/dashboard');
    } catch {
      toast({ variant: 'destructive', title: 'Error al crear identidad' });
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

          {/* --- Campo FOTO --- */}
          <label className="block">
            <span className="text-sm font-medium">Foto (JPG, PNG)</span>
            <input
              type="file"
              accept="image/*"
              onChange={(e) => setFotoFile(e.target.files?.[0] ?? null)}
              className="mt-1 block w-full"
            />
            {fotoFile && (
              <img
                src={URL.createObjectURL(fotoFile)}
                alt="Preview"
                className="mt-2 h-16 w-16 rounded-full object-cover"
              />
            )}
          </label>

          {/* --- Selector opción CV --- */}
          <div className="mt-4">
            <span className="mb-2 block font-medium">CV</span>
            <div className="mb-2 flex items-center gap-6">
              <label className="inline-flex items-center">
                <input
                  type="radio"
                  name="cvOption"
                  value="link"
                  checked={cvOption === 'link'}
                  onChange={() => setCvOption('link')}
                  className="mr-2"
                />
                Enlace
              </label>
              <label className="inline-flex items-center">
                <input
                  type="radio"
                  name="cvOption"
                  value="upload"
                  checked={cvOption === 'upload'}
                  onChange={() => setCvOption('upload')}
                  className="mr-2"
                />
                Subir PDF
              </label>
            </div>

            {/* Campo ENLACE */}
            {cvOption === 'link' && (
              <input
                type="url"
                placeholder="https://ejemplo.com/mi-cv.pdf"
                value={cvLink}
                onChange={(e) => setCvLink(e.target.value)}
                className="block w-full rounded-md border px-3 py-2 text-muted-foreground"
              />
            )}

            {/* Campo SUBIDA */}
            {cvOption === 'upload' && (
              <>
                <input
                  type="file"
                  accept="application/pdf"
                  onChange={(e) => setCvFile(e.target.files?.[0] ?? null)}
                  className="block w-full rounded-md border px-3 py-2"
                />
                {cvFile && (
                  <p className="mt-1 text-sm text-muted-foreground">
                    Seleccionado: {cvFile.name}
                  </p>
                )}
              </>
            )}
          </div>
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

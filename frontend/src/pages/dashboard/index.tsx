// frontend/src/pages/dashboard/index.tsx
import { useState, useEffect } from 'react';
import { useAuthStore, Personal } from '@/store/auth';
import { updatePersonal, deletePersonal } from '@/lib/personal';
import { useRouter } from '@/routes/hooks';
import { useLocation } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardFooter
} from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import { toast } from '@/components/ui/use-toast';
import FileUpload from '@/components/shared/fileupload';
import DataTable from '@/components/shared/data-table';
import { uploadFile } from '@/lib/files';
import api from '@/lib/client';

// Interfaces para tipado de datos
interface Proyecto {
  nombre: string;
  rol: string;
  fecha_inicio?: string;
  fecha_fin?: string;
}

interface Servicio {
  nombre: string;
  descripcion: string;
  fecha?: string;
}

interface Publicacion {
  titulo: string;
  fecha: string;
  estado: string;
  autores?: string;
}

interface BlogPost {
  titulo: string;
  creado_en: string;
  estado: string;
  autor_id: number;
}

export default function DashboardPage() {
  const router = useRouter();
  const location = useLocation();
  const personal = useAuthStore((s) => s.personal)!;
  const setPersonal = useAuthStore((s) => s.setPersonal);
  const clearPersonal = useAuthStore((s) => s.clearPersonal);
  const userId = personal?.id;

  // Estado para subida de foto
  const [files, setFiles] = useState<File[]>([]);

  // Estado de edición
  const [editMode, setEditMode] = useState(false);
  const [form, setForm] = useState<Partial<Personal>>({
    nombre: personal.nombre,
    cargo: personal.cargo,
    descripcion: personal.descripcion,
    email: personal.email,
    foto_url: personal.foto_url,
    cv_url: personal.cv_url,
    orcid: personal.orcid,
    fecha_alta: personal.fecha_alta
  });
  const [loading, setLoading] = useState(false);

  // Determinar pestaña activa basada en la ruta
  const [activeTab, setActiveTab] = useState('personal');

  useEffect(() => {
    // Extraer la ruta base para determinar la pestaña activa
    const path = location.pathname.split('/')[1] || '';
    if (
      ['personal', 'proyectos', 'servicios', 'publicaciones', 'blog'].includes(
        path
      )
    ) {
      setActiveTab(path);
    } else {
      setActiveTab('personal');
    }
  }, [location]);

  // Datos para pestañas
  // Proyectos
  const { data: proyectos = [] } = useQuery<Proyecto[]>({
    queryKey: ['proyectosDelPersonal', userId],
    queryFn: async () => {
      if (!userId) return [];
      const res = await api.get(`/personal/${userId}/proyectos`);
      return res.data;
    },
    enabled:
      !!userId &&
      (activeTab === 'proyectos' || location.pathname === '/proyectos')
  });

  // Servicios
  const { data: servicios = [] } = useQuery<Servicio[]>({
    queryKey: ['serviciosDelPersonal', userId],
    queryFn: async () => {
      if (!userId) return [];
      const res = await api.get(`/personal/${userId}/servicios`);
      return res.data;
    },
    enabled:
      !!userId &&
      (activeTab === 'servicios' || location.pathname === '/servicios')
  });

  // Publicaciones
  const { data: publicaciones = [] } = useQuery<Publicacion[]>({
    queryKey: ['publicaciones', userId],
    queryFn: async () => {
      if (!userId) return [];
      const res = await api.get('/publicaciones', {
        params: {
          autor_id: userId,
          limit: 50
        }
      });
      return res.data;
    },
    enabled:
      !!userId &&
      (activeTab === 'publicaciones' || location.pathname === '/publicaciones')
  });

  // Blog posts
  const { data: blogPosts = [] } = useQuery<BlogPost[]>({
    queryKey: ['blogPosts', userId],
    queryFn: async () => {
      if (!userId) return [];
      const res = await api.get('/blog/posts', {
        params: {
          limit: 50,
          solo_publicados: true
        }
      });
      return (res.data || []).filter((p: BlogPost) => p.autor_id === userId);
    },
    enabled: !!userId && (activeTab === 'blog' || location.pathname === '/blog')
  });

  // Handlers
  const onSave = async () => {
    setLoading(true);
    try {
      const updated = await updatePersonal(personal.id, form);
      setPersonal(updated);
      toast({ title: 'Datos guardados' });
      setEditMode(false);
    } catch {
      toast({ variant: 'destructive', title: 'Error al guardar' });
    } finally {
      setLoading(false);
    }
  };

  const onDelete = async () => {
    if (!confirm('¿Seguro que quieres eliminar tu identidad?')) return;
    try {
      await deletePersonal(personal.id);
      toast({ title: 'Identidad eliminada' });
      clearPersonal();
      router.replace('/identidad');
    } catch {
      toast({ variant: 'destructive', title: 'Error al eliminar' });
    }
  };

  // Subida de foto
  const uploadPhoto = async (file: File) => {
    try {
      setLoading(true);
      const archivo = await uploadFile(file);
      const updated = await updatePersonal(personal.id, {
        foto_url: archivo.ruta
      });
      setPersonal(updated);
      toast({ title: 'Foto actualizada' });
    } catch {
      toast({ variant: 'destructive', title: 'Error al subir la foto' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8 p-8">
      <div className="flex flex-col items-center justify-between gap-4 md:flex-row">
        <h1 className="text-3xl font-semibold">Hola, {personal.nombre}</h1>

        {/* Avatar con foto */}
        <div className="shrink-0">
          <FileUpload
            value={files}
            onChange={(files) => {
              setFiles(files);
              if (files[0]) uploadPhoto(files[0]);
            }}
          />
        </div>
      </div>

      <Card className="w-full">
        <CardHeader>
          <CardTitle>Mis datos</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {editMode ? (
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <label htmlFor="nombre" className="text-sm font-medium">
                  Nombre
                </label>
                <Input
                  id="nombre"
                  value={form.nombre}
                  onChange={(e) => setForm({ ...form, nombre: e.target.value })}
                />
              </div>
              <div className="space-y-2">
                <label htmlFor="cargo" className="text-sm font-medium">
                  Cargo
                </label>
                <Input
                  id="cargo"
                  value={form.cargo}
                  onChange={(e) => setForm({ ...form, cargo: e.target.value })}
                />
              </div>
              <div className="space-y-2">
                <label htmlFor="email" className="text-sm font-medium">
                  Email
                </label>
                <Input
                  id="email"
                  type="email"
                  value={form.email}
                  onChange={(e) => setForm({ ...form, email: e.target.value })}
                />
              </div>
              <div className="space-y-2">
                <label htmlFor="descripcion" className="text-sm font-medium">
                  Descripción
                </label>
                <Input
                  id="descripcion"
                  value={form.descripcion || ''}
                  onChange={(e) =>
                    setForm({ ...form, descripcion: e.target.value })
                  }
                />
              </div>
              <div className="space-y-2">
                <label htmlFor="orcid" className="text-sm font-medium">
                  ORCID
                </label>
                <Input
                  id="orcid"
                  value={form.orcid || ''}
                  onChange={(e) => setForm({ ...form, orcid: e.target.value })}
                />
              </div>
              <div className="space-y-2">
                <label htmlFor="cv_url" className="text-sm font-medium">
                  URL del CV
                </label>
                <Input
                  id="cv_url"
                  value={form.cv_url || ''}
                  onChange={(e) => setForm({ ...form, cv_url: e.target.value })}
                />
              </div>
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              <p>
                <strong>Nombre:</strong> {personal.nombre}
              </p>
              <p>
                <strong>Cargo:</strong> {personal.cargo}
              </p>
              <p>
                <strong>Email:</strong> {personal.email}
              </p>
              <p>
                <strong>Descripción:</strong>{' '}
                {personal.descripcion || 'No disponible'}
              </p>
              <p>
                <strong>ORCID:</strong> {personal.orcid || 'No disponible'}
              </p>
              <p>
                <strong>Fecha alta:</strong>{' '}
                {personal.fecha_alta || 'No disponible'}
              </p>
              <p>
                <strong>CV:</strong>{' '}
                {personal.cv_url ? (
                  <a
                    href={personal.cv_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline"
                  >
                    Ver CV
                  </a>
                ) : (
                  'No disponible'
                )}
              </p>
            </div>
          )}
        </CardContent>
        <CardFooter className="flex justify-between">
          {editMode ? (
            <div className="space-x-2">
              <Button variant="outline" onClick={() => setEditMode(false)}>
                Cancelar
              </Button>
              <Button onClick={onSave} disabled={loading}>
                {loading ? 'Guardando…' : 'Guardar'}
              </Button>
            </div>
          ) : (
            <div className="space-x-2">
              <Button variant="outline" onClick={() => setEditMode(true)}>
                Editar
              </Button>
              <Button variant="destructive" onClick={onDelete}>
                Eliminar
              </Button>
            </div>
          )}
        </CardFooter>
      </Card>

      {/* ——— Pestañas para los distintos módulos ——— */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="mb-4">
          <TabsTrigger value="personal">Personal</TabsTrigger>
          <TabsTrigger value="proyectos">Proyectos</TabsTrigger>
          <TabsTrigger value="servicios">Servicios</TabsTrigger>
          <TabsTrigger value="publicaciones">Publicaciones</TabsTrigger>
          <TabsTrigger value="blog">Blog Posts</TabsTrigger>
        </TabsList>

        <TabsContent value="personal">
          <pre className="max-h-80 overflow-auto rounded bg-gray-100 p-4">
            {JSON.stringify(personal, null, 2)}
          </pre>
        </TabsContent>

        <TabsContent value="proyectos">
          <DataTable
            columns={[
              { header: 'Proyecto', accessorKey: 'nombre' },
              { header: 'Rol', accessorKey: 'rol' },
              { header: 'Fecha inicio', accessorKey: 'fecha_inicio' },
              { header: 'Fecha fin', accessorKey: 'fecha_fin' }
            ]}
            data={proyectos}
            pageCount={1}
          />
        </TabsContent>

        <TabsContent value="servicios">
          <DataTable
            columns={[
              { header: 'Servicio', accessorKey: 'nombre' },
              { header: 'Descripción', accessorKey: 'descripcion' },
              { header: 'Fecha', accessorKey: 'fecha' }
            ]}
            data={servicios}
            pageCount={1}
          />
        </TabsContent>

        <TabsContent value="publicaciones">
          <DataTable
            columns={[
              { header: 'Título', accessorKey: 'titulo' },
              { header: 'Fecha', accessorKey: 'fecha' },
              { header: 'Estado', accessorKey: 'estado' },
              { header: 'Autores', accessorKey: 'autores' }
            ]}
            data={publicaciones}
            pageCount={Math.ceil(publicaciones.length / 10)}
          />
        </TabsContent>

        <TabsContent value="blog">
          <DataTable
            columns={[
              { header: 'Título', accessorKey: 'titulo' },
              { header: 'Fecha', accessorKey: 'creado_en' },
              { header: 'Estado', accessorKey: 'estado' }
            ]}
            data={blogPosts}
            pageCount={Math.ceil(blogPosts.length / 10)}
          />
        </TabsContent>
      </Tabs>
    </div>
  );
}

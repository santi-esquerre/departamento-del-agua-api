// frontend/src/routes/RequireAuth.tsx
import { ReactNode } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '@/store/auth';

export function RequireAuth({ children }: { children: ReactNode }) {
  const token = useAuthStore((s) => s.token);
  const personal = useAuthStore((s) => s.personal);
  const loc = useLocation();

  if (!token) {
    // si no está logueado, a login
    return <Navigate to="/login" state={{ from: loc }} replace />;
  }

  if (!personal) {
    // si no eligió identidad, a identidad
    return <Navigate to="/identidad" replace />;
  }

  return <>{children}</>;
}

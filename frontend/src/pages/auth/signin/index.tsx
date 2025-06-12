// frontend/src/pages/auth/signin/index.tsx
import LogoDepto from '@/assets/logo-departamento.svg';
import UserAuthForm from './components/user-auth-form';

export default function SignInPage() {
  return (
    <div className="grid h-screen grid-rows-1 lg:grid-cols-2">
      {/* ——— Panel izquierdo: logo a pantalla completa, fondo claro ——— */}
      <div className="hidden items-center justify-center bg-white py-8 lg:flex">
        <img
          src={LogoDepto}
          alt="Logotipo Departamento del Agua"
          className="h-full w-full object-contain"
        />
      </div>

      {/* ——— Panel derecho: form centrado vertical y horizontal ——— */}
      <div className="flex h-full items-center justify-center p-4 lg:p-8">
        <div className="w-full max-w-sm space-y-6">
          <div className="space-y-2 text-center">
            <h1 className="text-2xl font-semibold">Iniciar sesión</h1>
            <p className="text-sm text-muted-foreground">
              Ingresa tu usuario y contraseña del Departamento del Agua
            </p>
          </div>
          <UserAuthForm />
        </div>
      </div>
    </div>
  );
}

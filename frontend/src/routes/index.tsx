// frontend/src/routes/index.tsx
import { Suspense, lazy } from 'react';
import { Navigate, Outlet, useRoutes } from 'react-router-dom';

// pages y layouts lazy
const SignInPage = lazy(() => import('@/pages/auth/signin'));
const IdentidadPage = lazy(() => import('@/pages/identidad'));
const NotFound = lazy(() => import('@/pages/not-found'));
const DashboardLayout = lazy(
  () => import('@/components/layout/dashboard-layout')
);
const DashboardPage = lazy(() => import('@/pages/dashboard'));
const StudentPage = lazy(() => import('@/pages/students'));
const StudentDetail = lazy(() => import('@/pages/students/StudentDetailPage'));
const FormPage = lazy(() => import('@/pages/form'));

// guard
import { RequireAuth } from './RequireAuth';

export default function AppRouter() {
  const dashboardRoutes = [
    {
      path: '/',
      element: (
        <RequireAuth>
          <Suspense>
            <DashboardLayout>
              <Outlet />
            </DashboardLayout>
          </Suspense>
        </RequireAuth>
      ),
      children: [
        { index: true, element: <DashboardPage /> },
        { path: 'student', element: <StudentPage /> },
        { path: 'student/details', element: <StudentDetail /> },
        { path: 'form', element: <FormPage /> }
        // aquí podría ir la ruta de blog, académicos, etc.
      ]
    }
  ];

  const publicRoutes = [
    { path: '/login', element: <SignInPage /> },
    { path: '/identidad', element: <IdentidadPage /> },
    { path: '/404', element: <NotFound /> },
    { path: '/dashboard', element: <Navigate to="/" replace /> },
    { path: '*', element: <Navigate to="/404" replace /> }
  ];

  return useRoutes([...dashboardRoutes, ...publicRoutes]);
}

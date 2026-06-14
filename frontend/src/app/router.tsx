import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';

import { RequireAuth } from '@/features/auth/components/RequireAuth';
import { CallbackPage } from '@/features/auth/pages/CallbackPage';
import { LoginPage } from '@/features/auth/pages/LoginPage';
import { DashboardPage } from '@/features/dashboard/pages/DashboardPage';
import { RepositoriesPage } from '@/features/repositories/pages/RepositoriesPage';
import { ReviewDetailPage } from '@/features/reviews/pages/ReviewDetailPage';
import { ReviewHistoryPage } from '@/features/reviews/pages/ReviewHistoryPage';
import { AppLayout } from '@/shared/layouts/AppLayout';
import { AuthLayout } from '@/shared/layouts/AuthLayout';

export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AuthLayout />}>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/callback" element={<CallbackPage />} />
        </Route>

        <Route
          element={
            <RequireAuth>
              <AppLayout />
            </RequireAuth>
          }
        >
          <Route path="/" element={<DashboardPage />} />
          <Route path="/repos" element={<RepositoriesPage />} />
          <Route path="/reviews" element={<ReviewHistoryPage />} />
          <Route path="/reviews/:id" element={<ReviewDetailPage />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

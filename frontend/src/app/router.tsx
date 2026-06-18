import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';

import { RequireAuth } from '@/features/auth/components/RequireAuth';
import { CallbackPage } from '@/features/auth/pages/CallbackPage';
import { LoginPage } from '@/features/auth/pages/LoginPage';
import { LandingPage } from '@/features/landing/pages/LandingPage';
import { DashboardPage } from '@/features/dashboard/pages/DashboardPage';
import { RepositoriesPage } from '@/features/repositories/pages/RepositoriesPage';
import { RepoSettingsPage } from '@/features/repositories/pages/RepoSettingsPage';
import { ReviewDetailPage } from '@/features/reviews/pages/ReviewDetailPage';
import { ReviewHistoryPage } from '@/features/reviews/pages/ReviewHistoryPage';
import { AppLayout } from '@/shared/layouts/AppLayout';
import { AuthLayout } from '@/shared/layouts/AuthLayout';

export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public landing — no redirect, always visible */}
        <Route path="/" element={<LandingPage />} />

        {/* Auth pages */}
        <Route element={<AuthLayout />}>
          <Route path="/login"    element={<LoginPage />} />
          <Route path="/callback" element={<CallbackPage />} />
        </Route>

        {/* Authenticated app */}
        <Route
          element={
            <RequireAuth>
              <AppLayout />
            </RequireAuth>
          }
        >
          <Route path="/dashboard"  element={<DashboardPage />} />
          <Route path="/repos"      element={<RepositoriesPage />} />
          <Route path="/repos/:id"  element={<RepoSettingsPage />} />
          <Route path="/reviews"    element={<ReviewHistoryPage />} />
          <Route path="/reviews/:id" element={<ReviewDetailPage />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

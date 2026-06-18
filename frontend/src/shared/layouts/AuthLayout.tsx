import { Outlet } from 'react-router-dom';

export function AuthLayout() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-muted/30 px-4 py-8 sm:px-6">
      <div className="w-full max-w-sm">
        <Outlet />
      </div>
    </div>
  );
}

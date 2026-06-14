import { Link, Outlet } from 'react-router-dom';

import { UserMenu } from '@/features/auth/components/UserMenu';

const nav = [
  { to: '/', label: 'Dashboard' },
  { to: '/repos', label: 'Repositories' },
  { to: '/reviews', label: 'Reviews' },
];

export function AppLayout() {
  return (
    <div className="min-h-screen">
      <header className="border-b border-border bg-muted/20">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
          <div className="flex items-center gap-6">
            <span className="text-lg font-semibold">PR Reviewer</span>
            <nav className="flex gap-4 text-sm text-muted-foreground">
              {nav.map((item) => (
                <Link key={item.to} to={item.to} className="hover:text-foreground">
                  {item.label}
                </Link>
              ))}
            </nav>
          </div>
          <UserMenu />
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-8">
        <Outlet />
      </main>
    </div>
  );
}

import { env } from '@/config/env';
import { LoginButton } from '@/features/auth/components/LoginButton';
import { ThemeToggle } from '@/shared/components/ThemeToggle';

export function LoginPage() {
  return (
    <div className="space-y-8 text-center animate-fade-in">
      {/* Brand mark */}
      <div>
        <img src="/logo.png" alt="ReviewGraph" className="mx-auto mb-4 h-14 w-14 rounded-2xl shadow-card" />
        <h1 className="text-2xl font-semibold tracking-tight">ReviewGraph</h1>
        <p className="mt-2 text-sm text-muted-foreground">
          Multi-agent AI code review for your GitHub pull requests.
        </p>
      </div>

      {/* Login card */}
      <div className="rounded-lg border border-border bg-card p-6 shadow-card">
        <div className="space-y-4">
          <LoginButton />
          <p className="text-xs text-muted-foreground">
            New here?{' '}
            <a
              href={env.githubAppInstallUrl}
              className="text-primary underline-offset-4 hover:underline"
              target="_blank"
              rel="noreferrer"
            >
              Install the GitHub App
            </a>{' '}
            on your org or repos first.
          </p>
        </div>
      </div>

      <p className="text-xs text-muted-foreground/60">
        By signing in you agree to our terms of service.
      </p>

      {/* Theme toggle bottom-right */}
      <div className="flex justify-center">
        <ThemeToggle />
      </div>
    </div>
  );
}

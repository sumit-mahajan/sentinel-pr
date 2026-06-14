import { Card } from '@/shared/components/Card';
import { LoginButton } from '@/features/auth/components/LoginButton';
import { env } from '@/config/env';

export function LoginPage() {
  return (
    <Card className="space-y-6 text-center">
      <div>
        <h1 className="text-2xl font-semibold">PR Reviewer</h1>
        <p className="mt-2 text-sm text-muted-foreground">
          Multi-agent AI code review for your GitHub pull requests.
        </p>
      </div>
      <LoginButton />
      <p className="text-xs text-muted-foreground">
        New here?{' '}
        <a href={env.githubAppInstallUrl} className="text-primary hover:underline" target="_blank" rel="noreferrer">
          Install the GitHub App
        </a>{' '}
        on your org or repos first.
      </p>
    </Card>
  );
}

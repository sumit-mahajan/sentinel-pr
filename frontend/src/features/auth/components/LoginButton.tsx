import { Github } from 'lucide-react';

import { env } from '@/config/env';

export function LoginButton() {
  return (
    <a
      href={`${env.VITE_API_BASE_URL}/auth/github`}
      className="inline-flex w-full items-center justify-center gap-2 rounded-md bg-foreground px-4 py-2.5 text-sm font-medium text-background transition-opacity hover:opacity-80"
    >
      <Github className="h-4 w-4" />
      Continue with GitHub
    </a>
  );
}

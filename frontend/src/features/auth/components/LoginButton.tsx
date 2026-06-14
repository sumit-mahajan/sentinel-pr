import { env } from '@/config/env';

export function LoginButton() {
  return (
    <a
      href={`${env.VITE_API_BASE_URL}/auth/github`}
      className="inline-flex w-full items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:opacity-90"
    >
      Sign in with GitHub
    </a>
  );
}

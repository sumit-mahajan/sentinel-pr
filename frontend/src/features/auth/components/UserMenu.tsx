import { useAuthStore } from '@/features/auth/store/authStore';
import { Button } from '@/shared/components/Button';

export function UserMenu() {
  const user = useAuthStore((s) => s.user);
  const clearAuth = useAuthStore((s) => s.clearAuth);

  if (!user) return null;

  return (
    <div className="flex items-center gap-2">
      {user.avatar_url && (
        <img
          src={user.avatar_url}
          alt={user.login}
          className="h-7 w-7 rounded-full ring-1 ring-border"
        />
      )}
      <span className="hidden text-sm text-muted-foreground sm:block">{user.login}</span>
      <Button variant="ghost" size="sm" onClick={clearAuth}>
        Sign out
      </Button>
    </div>
  );
}

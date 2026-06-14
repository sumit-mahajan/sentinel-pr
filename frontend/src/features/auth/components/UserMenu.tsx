import { useAuthStore } from '@/features/auth/store/authStore';
import { Button } from '@/shared/components/Button';

export function UserMenu() {
  const user = useAuthStore((s) => s.user);
  const clearAuth = useAuthStore((s) => s.clearAuth);

  if (!user) return null;

  return (
    <div className="flex items-center gap-3">
      {user.avatar_url && (
        <img src={user.avatar_url} alt={user.login} className="h-8 w-8 rounded-full" />
      )}
      <span className="text-sm">{user.login}</span>
      <Button variant="ghost" onClick={clearAuth}>
        Sign out
      </Button>
    </div>
  );
}

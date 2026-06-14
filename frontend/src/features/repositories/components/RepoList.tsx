import type { RepoDTO } from '@/shared/types/api';
import { RepoCard } from '@/features/repositories/components/RepoCard';

export function RepoList({ repos }: { repos: RepoDTO[] }) {
  return (
    <div className="grid gap-4">
      {repos.map((repo) => (
        <RepoCard key={repo.id} repo={repo} />
      ))}
    </div>
  );
}

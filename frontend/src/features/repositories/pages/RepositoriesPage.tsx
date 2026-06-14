import { useRepositories } from '@/features/repositories/hooks/useRepositories';
import { RepoList } from '@/features/repositories/components/RepoList';
import { Spinner } from '@/shared/components/Spinner';
import { EmptyState } from '@/shared/components/EmptyState';
import { env } from '@/config/env';

export function RepositoriesPage() {
  const { data, isLoading, error } = useRepositories();

  if (isLoading) return <Spinner />;
  if (error) return <EmptyState message="Failed to load repositories." />;
  if (!data?.length) {
    return (
      <EmptyState
        message={`No repositories found. Install the GitHub App at ${env.githubAppInstallUrl} and sync your installation.`}
      />
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">Repositories</h1>
        <p className="text-sm text-muted-foreground">Toggle agents and review settings per repo.</p>
      </div>
      <RepoList repos={data} />
    </div>
  );
}

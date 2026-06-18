import { useRepositories } from '@/features/repositories/hooks/useRepositories';
import { RepoList } from '@/features/repositories/components/RepoList';
import { Skeleton } from '@/shared/components/Skeleton';
import { EmptyState } from '@/shared/components/EmptyState';
import { env } from '@/config/env';

function RepoListSkeleton() {
  return (
    <div className="space-y-3">
      {Array.from({ length: 4 }).map((_, i) => (
        <Skeleton key={i} className="h-16 rounded-lg" />
      ))}
    </div>
  );
}

export function RepositoriesPage() {
  const { data, isLoading, error } = useRepositories();

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Repositories</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Click a repo to manage its review settings and agent config.
        </p>
      </div>

      {isLoading && <RepoListSkeleton />}

      {error && <EmptyState message="Failed to load repositories." />}

      {!isLoading && !error && !data?.length && (
        <EmptyState
          message={`No repositories found. Install the GitHub App to get started.`}
        />
      )}

      {!isLoading && !error && data?.length ? (
        <RepoList repos={data} />
      ) : null}

      {!isLoading && !error && !data?.length && (
        <div className="text-center">
          <a
            href={env.githubAppInstallUrl}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1.5 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-opacity hover:opacity-90"
          >
            Install GitHub App ↗
          </a>
        </div>
      )}
    </div>
  );
}

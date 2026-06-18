import { Link, useParams } from 'react-router-dom';

import { useRepository } from '@/features/repositories/hooks/useRepositories';
import { AgentConfigPanel } from '@/features/repositories/components/AgentConfigPanel';
import { Skeleton } from '@/shared/components/Skeleton';
import { EmptyState } from '@/shared/components/EmptyState';
import { cn } from '@/shared/utils/cn';

function SettingsSkeleton() {
  return (
    <div className="space-y-6">
      <Skeleton className="h-4 w-32" />
      <div className="space-y-1.5">
        <Skeleton className="h-7 w-64" />
        <Skeleton className="h-4 w-40" />
      </div>
      <Skeleton className="h-40 rounded-lg" />
    </div>
  );
}

export function RepoSettingsPage() {
  const { id = '' } = useParams();
  const { data: repo, isLoading, error } = useRepository(id);

  if (isLoading) return <SettingsSkeleton />;
  if (error || !repo) return <EmptyState message="Repository not found." />;

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Back nav */}
      <Link
        to="/repos"
        className="inline-flex items-center gap-1 text-xs text-muted-foreground underline-offset-4 hover:text-foreground hover:underline"
      >
        ← Back to Repositories
      </Link>

      {/* Header */}
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h1 className="break-words text-xl font-semibold tracking-tight sm:text-2xl">{repo.full_name}</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            {repo.language ?? 'Unknown'} · {repo.default_branch}
          </p>
        </div>
        <span
          className={cn(
            'mt-1 inline-flex items-center rounded-md border px-2.5 py-1 text-xs font-medium',
            repo.is_active
              ? 'border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-500/20 dark:bg-emerald-500/10 dark:text-emerald-400'
              : 'border-slate-200 bg-slate-100 text-slate-500 dark:border-slate-500/20 dark:bg-slate-500/10 dark:text-slate-400',
          )}
        >
          {repo.is_active ? 'Active' : 'Paused'}
        </span>
      </div>

      {/* Settings card */}
      <div className="rounded-lg border border-border bg-card shadow-card">
        <div className="border-b border-border px-5 py-4">
          <h2 className="text-sm font-semibold">Review settings</h2>
          <p className="mt-0.5 text-xs text-muted-foreground">
            Adjust agents and thresholds, then save your changes.
          </p>
        </div>
        <div className="p-5">
          <AgentConfigPanel repo={repo} />
        </div>
      </div>
    </div>
  );
}

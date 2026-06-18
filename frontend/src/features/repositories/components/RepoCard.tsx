import { ChevronRight } from 'lucide-react';
import { Link } from 'react-router-dom';

import type { RepoDTO } from '@/shared/types/api';
import { cn } from '@/shared/utils/cn';

export function RepoCard({ repo }: { repo: RepoDTO }) {
  return (
    <Link
      to={`/repos/${repo.id}`}
      className="group flex items-center justify-between gap-4 rounded-lg border border-border bg-card p-4 shadow-card transition-shadow hover:shadow-md"
    >
      <div className="min-w-0">
        <h3 className="truncate font-medium group-hover:text-primary transition-colors">
          {repo.full_name}
        </h3>
        <p className="mt-0.5 text-sm text-muted-foreground">
          {repo.language ?? 'Unknown'} · {repo.default_branch}
        </p>
      </div>

      <div className="flex shrink-0 items-center gap-3">
        <span
          className={cn(
            'inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-medium',
            repo.is_active
              ? 'border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-500/20 dark:bg-emerald-500/10 dark:text-emerald-400'
              : 'border-slate-200 bg-slate-100 text-slate-500 dark:border-slate-500/20 dark:bg-slate-500/10 dark:text-slate-400',
          )}
        >
          {repo.is_active ? 'Active' : 'Paused'}
        </span>
        <ChevronRight className="h-4 w-4 text-muted-foreground transition-transform group-hover:translate-x-0.5" />
      </div>
    </Link>
  );
}

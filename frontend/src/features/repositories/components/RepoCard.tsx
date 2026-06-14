import type { RepoDTO } from '@/shared/types/api';
import { Card } from '@/shared/components/Card';
import { AgentConfigPanel } from '@/features/repositories/components/AgentConfigPanel';

export function RepoCard({ repo }: { repo: RepoDTO }) {
  return (
    <Card className="space-y-4">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h3 className="font-medium">{repo.full_name}</h3>
          <p className="text-sm text-muted-foreground">
            {repo.language ?? 'Unknown'} · {repo.default_branch}
          </p>
        </div>
        <span
          className={`rounded-full px-2 py-0.5 text-xs ${
            repo.is_active ? 'bg-green-500/20 text-green-300' : 'bg-slate-500/20 text-slate-300'
          }`}
        >
          {repo.is_active ? 'Active' : 'Paused'}
        </span>
      </div>
      <AgentConfigPanel repo={repo} />
    </Card>
  );
}

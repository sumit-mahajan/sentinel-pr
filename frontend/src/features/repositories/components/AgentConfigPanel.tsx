import type { RepoDTO } from '@/shared/types/api';
import { useUpdateAgentConfig } from '@/features/repositories/hooks/useRepositories';

const agents = [
  { key: 'security_enabled' as const, label: 'Security' },
  { key: 'perf_enabled' as const, label: 'Performance' },
  { key: 'arch_enabled' as const, label: 'Architecture' },
  { key: 'test_enabled' as const, label: 'Tests' },
];

const severities = ['critical', 'high', 'medium', 'low', 'info'];

export function AgentConfigPanel({ repo }: { repo: RepoDTO }) {
  const mutation = useUpdateAgentConfig(repo.id);
  const config = repo.agent_config;

  return (
    <div className="space-y-3 border-t border-border pt-3">
      <div className="flex flex-wrap gap-3">
        {agents.map((agent) => (
          <label key={agent.key} className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={config[agent.key]}
              onChange={(e) => mutation.mutate({ [agent.key]: e.target.checked })}
            />
            {agent.label}
          </label>
        ))}
      </div>
      <div className="flex items-center gap-3 text-sm">
        <span className="text-muted-foreground">Min severity</span>
        <select
          className="rounded-md border border-border bg-background px-2 py-1"
          value={config.min_severity}
          onChange={(e) => mutation.mutate({ min_severity: e.target.value })}
        >
          {severities.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={repo.is_active}
            onChange={(e) => mutation.mutate({ is_active: e.target.checked })}
          />
          Reviews enabled
        </label>
      </div>
    </div>
  );
}

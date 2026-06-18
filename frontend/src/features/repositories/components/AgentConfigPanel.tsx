import { useEffect, useMemo, useState } from 'react';
import * as Switch from '@radix-ui/react-switch';
import { Loader2 } from 'lucide-react';
import { toast } from 'sonner';

import type { RepoDTO } from '@/shared/types/api';
import { useUpdateAgentConfig } from '@/features/repositories/hooks/useRepositories';
import { Button } from '@/shared/components/Button';
import { cn } from '@/shared/utils/cn';

const agents: { key: 'security_enabled' | 'perf_enabled' | 'arch_enabled' | 'test_enabled'; label: string }[] = [
  { key: 'security_enabled', label: 'Security' },
  { key: 'perf_enabled',     label: 'Performance' },
  { key: 'arch_enabled',     label: 'Architecture' },
  { key: 'test_enabled',     label: 'Tests' },
];

const severities = ['critical', 'high', 'medium', 'low', 'info'];

interface RepoSettingsForm {
  security_enabled: boolean;
  perf_enabled: boolean;
  arch_enabled: boolean;
  test_enabled: boolean;
  min_severity: string;
  is_active: boolean;
}

function formFromRepo(repo: RepoDTO): RepoSettingsForm {
  return {
    security_enabled: repo.agent_config.security_enabled,
    perf_enabled:     repo.agent_config.perf_enabled,
    arch_enabled:     repo.agent_config.arch_enabled,
    test_enabled:     repo.agent_config.test_enabled,
    min_severity:     repo.agent_config.min_severity,
    is_active:        repo.is_active,
  };
}

function AgentSwitch({
  checked,
  onCheckedChange,
  label,
  disabled,
}: {
  checked: boolean;
  onCheckedChange: (val: boolean) => void;
  label: string;
  disabled?: boolean;
}) {
  return (
    <label
      className={cn(
        'flex min-h-[44px] items-center gap-3 rounded-md p-2 transition-colors sm:min-h-0 sm:p-0',
        disabled ? 'cursor-not-allowed opacity-60' : 'cursor-pointer hover:bg-muted/50 sm:hover:bg-transparent',
      )}
    >
      <Switch.Root
        checked={checked}
        onCheckedChange={onCheckedChange}
        disabled={disabled}
        className={cn(
          'relative inline-flex h-5 w-9 shrink-0 items-center rounded-full border-2 border-transparent transition-colors',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-1',
          'disabled:cursor-not-allowed disabled:opacity-50',
          checked ? 'bg-primary' : 'bg-input',
        )}
      >
        <Switch.Thumb
          className={cn(
            'pointer-events-none block h-4 w-4 rounded-full bg-white shadow-sm transition-transform',
            checked ? 'translate-x-4' : 'translate-x-0',
          )}
        />
      </Switch.Root>
      <span className="text-sm">{label}</span>
    </label>
  );
}

export function AgentConfigPanel({ repo }: { repo: RepoDTO }) {
  const mutation = useUpdateAgentConfig(repo.id);
  const [draft, setDraft] = useState<RepoSettingsForm>(() => formFromRepo(repo));

  const saved = useMemo(() => formFromRepo(repo), [repo]);

  useEffect(() => {
    setDraft(saved);
  }, [saved]);

  const isDirty = useMemo(
    () => JSON.stringify(draft) !== JSON.stringify(saved),
    [draft, saved],
  );

  const isSaving = mutation.isPending;

  function updateDraft<K extends keyof RepoSettingsForm>(key: K, value: RepoSettingsForm[K]) {
    setDraft((prev) => ({ ...prev, [key]: value }));
  }

  function handleDiscard() {
    setDraft(saved);
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!isDirty || isSaving) return;

    mutation.mutate(draft, {
      onSuccess: () => {
        toast.success('Settings saved', {
          description: `${repo.full_name} review configuration updated.`,
        });
      },
      onError: () => {
        toast.error('Failed to save settings', {
          description: 'Please try again.',
        });
      },
    });
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Agent toggles */}
      <div>
        <p className="mb-2 text-xs font-medium uppercase tracking-widest text-muted-foreground">
          Agents
        </p>
        <div className="grid grid-cols-1 gap-1 sm:grid-cols-2 sm:gap-2 lg:grid-cols-4">
          {agents.map((agent) => (
            <AgentSwitch
              key={agent.key}
              label={agent.label}
              checked={draft[agent.key]}
              disabled={isSaving}
              onCheckedChange={(val) => updateDraft(agent.key, val)}
            />
          ))}
        </div>
      </div>

      {/* Min severity + reviews enabled */}
      <div className="flex flex-col gap-4 sm:flex-row sm:flex-wrap sm:items-center">
        <div className="flex items-center gap-3">
          <span className="text-xs font-medium uppercase tracking-widest text-muted-foreground">
            Min severity
          </span>
          <select
            className="rounded-md border border-input bg-background px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-ring disabled:cursor-not-allowed disabled:opacity-60"
            value={draft.min_severity}
            disabled={isSaving}
            onChange={(e) => updateDraft('min_severity', e.target.value)}
          >
            {severities.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>

        <AgentSwitch
          label="Reviews enabled"
          checked={draft.is_active}
          disabled={isSaving}
          onCheckedChange={(val) => updateDraft('is_active', val)}
        />
      </div>

      {/* Actions */}
      <div className="flex flex-wrap items-center gap-3 border-t border-border pt-5">
        <Button type="submit" disabled={!isDirty || isSaving}>
          {isSaving ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              Saving…
            </>
          ) : (
            'Save changes'
          )}
        </Button>
        {isDirty && !isSaving && (
          <Button type="button" variant="ghost" onClick={handleDiscard}>
            Discard
          </Button>
        )}
        {isDirty && !isSaving && (
          <span className="text-xs text-muted-foreground">Unsaved changes</span>
        )}
      </div>
    </form>
  );
}

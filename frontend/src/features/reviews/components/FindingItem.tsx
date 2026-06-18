import type { FindingDTO } from '@/shared/types/api';
import { Badge } from '@/shared/components/Badge';
import { cn } from '@/shared/utils/cn';

const severityBorderColor: Record<string, string> = {
  critical: 'border-l-red-500',
  high:     'border-l-orange-500',
  medium:   'border-l-yellow-500',
  low:      'border-l-sky-500',
  info:     'border-l-slate-400',
};

export function FindingItem({ finding }: { finding: FindingDTO }) {
  return (
    <div
      className={cn(
        'rounded-lg border border-border bg-card shadow-card',
        'border-l-2 p-3 space-y-2 sm:p-4',
        severityBorderColor[finding.severity] ?? 'border-l-slate-400',
      )}
    >
      {/* Meta row */}
      <div className="flex flex-wrap items-center gap-1.5 sm:gap-2">
        <Badge severity={finding.severity}>{finding.severity}</Badge>
        <span className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
          {finding.category}
        </span>
        <span className="hidden text-xs text-muted-foreground sm:inline">
          via {finding.agent_source}
        </span>
      </div>

      {/* Title */}
      <h4 className="break-words text-sm font-medium leading-snug">{finding.title}</h4>

      {/* File path — break long paths on mobile */}
      <p className="text-xs text-muted-foreground">
        <code className="inline-block max-w-full break-all rounded bg-muted px-1 py-0.5 font-mono text-[11px]">
          {finding.file_path}
          {finding.line_start ? `:${finding.line_start}` : ''}
          {finding.line_end && finding.line_end !== finding.line_start
            ? `–${finding.line_end}`
            : ''}
        </code>
      </p>

      {/* Description */}
      <p className="break-words text-sm text-foreground/80">{finding.description}</p>

      {/* Fix suggestion */}
      {finding.fix_suggestion && (
        <div className="rounded-md border border-border bg-muted/50 p-2.5 text-xs leading-relaxed sm:p-3">
          <span className="font-medium text-foreground">Suggested fix: </span>
          <span className="break-words text-muted-foreground">{finding.fix_suggestion}</span>
        </div>
      )}
    </div>
  );
}

import { cn } from '@/shared/utils/cn';

const severityStyles: Record<string, string> = {
  critical: 'bg-red-500/20 text-red-300 border-red-500/40',
  high: 'bg-orange-500/20 text-orange-300 border-orange-500/40',
  medium: 'bg-yellow-500/20 text-yellow-200 border-yellow-500/40',
  low: 'bg-blue-500/20 text-blue-200 border-blue-500/40',
  info: 'bg-slate-500/20 text-slate-200 border-slate-500/40',
};

export function Badge({ severity, children }: { severity: string; children: React.ReactNode }) {
  return (
    <span
      className={cn(
        'inline-flex rounded-full border px-2 py-0.5 text-xs font-medium uppercase',
        severityStyles[severity] ?? severityStyles.info,
      )}
    >
      {children}
    </span>
  );
}

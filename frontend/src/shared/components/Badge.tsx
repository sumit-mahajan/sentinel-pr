import { cn } from '@/shared/utils/cn';

const severityStyles: Record<string, string> = {
  critical: 'bg-red-50    text-red-700    border-red-200    dark:bg-red-500/10    dark:text-red-400    dark:border-red-500/20',
  high:     'bg-orange-50 text-orange-700 border-orange-200 dark:bg-orange-500/10 dark:text-orange-400 dark:border-orange-500/20',
  medium:   'bg-yellow-50 text-yellow-700 border-yellow-200 dark:bg-yellow-500/10 dark:text-yellow-400 dark:border-yellow-500/20',
  low:      'bg-sky-50    text-sky-700    border-sky-200    dark:bg-sky-500/10    dark:text-sky-400    dark:border-sky-500/20',
  info:     'bg-slate-100 text-slate-600  border-slate-200  dark:bg-slate-500/10  dark:text-slate-400  dark:border-slate-500/20',
};

export function Badge({ severity, children }: { severity: string; children: React.ReactNode }) {
  return (
    <span
      className={cn(
        'inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-medium',
        severityStyles[severity] ?? severityStyles.info,
      )}
    >
      {children}
    </span>
  );
}

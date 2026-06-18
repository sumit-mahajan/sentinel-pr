import { cn } from '@/shared/utils/cn';

export function Card({ className, children }: { className?: string; children: React.ReactNode }) {
  return (
    <div className={cn('rounded-lg border border-border bg-card shadow-card p-4', className)}>
      {children}
    </div>
  );
}

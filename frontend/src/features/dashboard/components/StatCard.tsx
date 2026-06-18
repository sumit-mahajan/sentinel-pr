import { Card } from '@/shared/components/Card';

export function StatCard({ label, value }: { label: string; value: number | string }) {
  return (
    <Card className="p-4 sm:p-5">
      <p className="text-[10px] font-medium uppercase tracking-widest text-muted-foreground sm:text-xs">
        {label}
      </p>
      <p className="mt-1.5 text-2xl font-semibold tabular-nums tracking-tight sm:mt-2 sm:text-3xl 2xl:text-4xl">
        {value}
      </p>
    </Card>
  );
}

import { Card } from '@/shared/components/Card';

export function StatCard({ label, value }: { label: string; value: number | string }) {
  return (
    <Card>
      <p className="text-sm text-muted-foreground">{label}</p>
      <p className="mt-2 text-3xl font-semibold">{value}</p>
    </Card>
  );
}

import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

interface Props {
  data: { severity: string; count: number }[];
}

export function SeverityDistributionChart({ data }: Props) {
  if (!data.some((d) => d.count > 0)) {
    return <p className="text-sm text-muted-foreground">No findings yet.</p>;
  }

  return (
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <XAxis dataKey="severity" stroke="#94a3b8" />
          <YAxis allowDecimals={false} stroke="#94a3b8" />
          <Tooltip />
          <Bar dataKey="count" fill="#3b82f6" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

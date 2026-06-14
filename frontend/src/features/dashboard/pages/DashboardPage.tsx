import { useReviews } from '@/features/reviews/hooks/useReviews';
import { RecentReviewsList } from '@/features/dashboard/components/RecentReviewsList';
import { SeverityDistributionChart } from '@/features/dashboard/components/SeverityDistributionChart';
import { StatCard } from '@/features/dashboard/components/StatCard';
import { Spinner } from '@/shared/components/Spinner';
import { EmptyState } from '@/shared/components/EmptyState';

export function DashboardPage() {
  const { data, isLoading, error } = useReviews(undefined, 1);

  if (isLoading) return <Spinner />;
  if (error) return <EmptyState message="Failed to load dashboard." />;

  const reviews = data?.items ?? [];
  const totals = reviews.reduce(
    (acc, r) => ({
      critical: acc.critical + r.critical_count,
      high: acc.high + r.high_count,
      medium: acc.medium + r.medium_count,
      low: acc.low + r.low_count,
      info: acc.info + r.info_count,
    }),
    { critical: 0, high: 0, medium: 0, low: 0, info: 0 },
  );

  const chartData = [
    { severity: 'critical', count: totals.critical },
    { severity: 'high', count: totals.high },
    { severity: 'medium', count: totals.medium },
    { severity: 'low', count: totals.low },
    { severity: 'info', count: totals.info },
  ];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-semibold">Dashboard</h1>
        <p className="text-sm text-muted-foreground">Overview of recent PR reviews.</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Reviews" value={data?.total ?? 0} />
        <StatCard label="Critical" value={totals.critical} />
        <StatCard label="High" value={totals.high} />
        <StatCard label="Total findings" value={reviews.reduce((n, r) => n + r.total_findings, 0)} />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div>
          <h2 className="mb-3 text-lg font-medium">Severity distribution</h2>
          <SeverityDistributionChart data={chartData} />
        </div>
        <div>
          <h2 className="mb-3 text-lg font-medium">Recent reviews</h2>
          {reviews.length ? <RecentReviewsList reviews={reviews.slice(0, 5)} /> : <EmptyState message="No reviews yet." />}
        </div>
      </div>
    </div>
  );
}

import { useReviews } from '@/features/reviews/hooks/useReviews';
import { RecentReviewsList } from '@/features/dashboard/components/RecentReviewsList';
import { SeverityDistributionChart } from '@/features/dashboard/components/SeverityDistributionChart';
import { StatCard } from '@/features/dashboard/components/StatCard';
import { Skeleton } from '@/shared/components/Skeleton';
import { EmptyState } from '@/shared/components/EmptyState';

function DashboardSkeleton() {
  return (
    <div className="space-y-8">
      <div className="space-y-1.5">
        <Skeleton className="h-7 w-36" />
        <Skeleton className="h-4 w-52" />
      </div>
      <div className="grid grid-cols-2 gap-3 sm:gap-4 lg:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <Skeleton key={i} className="h-24 rounded-lg" />
        ))}
      </div>
      <div className="grid gap-6 lg:grid-cols-2">
        <Skeleton className="h-64 rounded-lg" />
        <div className="space-y-3">
          {Array.from({ length: 4 }).map((_, i) => (
            <Skeleton key={i} className="h-20 rounded-lg" />
          ))}
        </div>
      </div>
    </div>
  );
}

export function DashboardPage() {
  const { data, isLoading, error } = useReviews(undefined, 1);

  if (isLoading) return <DashboardSkeleton />;
  if (error) return <EmptyState message="Failed to load dashboard." />;

  const reviews = data?.items ?? [];
  const totals = reviews.reduce(
    (acc, r) => ({
      critical: acc.critical + r.critical_count,
      high:     acc.high     + r.high_count,
      medium:   acc.medium   + r.medium_count,
      low:      acc.low      + r.low_count,
      info:     acc.info     + r.info_count,
    }),
    { critical: 0, high: 0, medium: 0, low: 0, info: 0 },
  );

  const chartData = [
    { severity: 'critical', count: totals.critical },
    { severity: 'high',     count: totals.high },
    { severity: 'medium',   count: totals.medium },
    { severity: 'low',      count: totals.low },
    { severity: 'info',     count: totals.info },
  ];

  return (
    <div className="space-y-8 animate-fade-in">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Dashboard</h1>
        <p className="mt-1 text-sm text-muted-foreground">Overview of recent PR reviews.</p>
      </div>

      <div className="grid grid-cols-2 gap-3 sm:gap-4 lg:grid-cols-4">
        <StatCard label="Reviews"        value={data?.total ?? 0} />
        <StatCard label="Critical"       value={totals.critical} />
        <StatCard label="High"           value={totals.high} />
        <StatCard label="Total findings" value={reviews.reduce((n, r) => n + r.total_findings, 0)} />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div>
          <h2 className="mb-3 text-sm font-semibold uppercase tracking-widest text-muted-foreground">
            Severity distribution
          </h2>
          <SeverityDistributionChart data={chartData} />
        </div>
        <div>
          <h2 className="mb-3 text-sm font-semibold uppercase tracking-widest text-muted-foreground">
            Recent reviews
          </h2>
          {reviews.length
            ? <RecentReviewsList reviews={reviews.slice(0, 5)} />
            : <EmptyState message="No reviews yet." />
          }
        </div>
      </div>
    </div>
  );
}

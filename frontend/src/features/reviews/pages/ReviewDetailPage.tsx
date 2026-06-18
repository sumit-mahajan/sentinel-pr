import { Link, useParams } from 'react-router-dom';

import { useReviewDetail } from '@/features/reviews/hooks/useReviews';
import { FindingItem } from '@/features/reviews/components/FindingItem';
import { Badge } from '@/shared/components/Badge';
import { Skeleton } from '@/shared/components/Skeleton';
import { EmptyState } from '@/shared/components/EmptyState';
import { formatDate } from '@/shared/utils/formatDate';

function ReviewDetailSkeleton() {
  return (
    <div className="space-y-6">
      <Skeleton className="h-4 w-36" />
      <div className="space-y-1.5">
        <Skeleton className="h-7 w-48" />
        <Skeleton className="h-4 w-64" />
      </div>
      <div className="flex gap-2">
        {Array.from({ length: 3 }).map((_, i) => <Skeleton key={i} className="h-6 w-20 rounded-md" />)}
      </div>
      <Skeleton className="h-24 rounded-lg" />
      <div className="space-y-3">
        {Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-28 rounded-lg" />)}
      </div>
    </div>
  );
}

export function ReviewDetailPage() {
  const { id = '' } = useParams();
  const { data, isLoading, error } = useReviewDetail(id);

  if (isLoading) return <ReviewDetailSkeleton />;
  if (error || !data) return <EmptyState message="Review not found." />;

  const agentCounts = data.findings.reduce<Record<string, number>>((acc, f) => {
    acc[f.agent_source] = (acc[f.agent_source] ?? 0) + 1;
    return acc;
  }, {});

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Back + header */}
      <div>
        <Link
          to="/reviews"
          className="inline-flex items-center gap-1 text-xs text-muted-foreground underline-offset-4 hover:text-foreground hover:underline"
        >
          ← Back to reviews
        </Link>
        <h1 className="mt-2 text-xl font-semibold tracking-tight sm:text-2xl">PR #{data.pr_number}</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          {formatDate(data.created_at)} ·{' '}
          <a
            href={data.pr_url}
            target="_blank"
            rel="noreferrer"
            className="text-primary underline-offset-4 hover:underline"
          >
            View on GitHub ↗
          </a>
        </p>
      </div>

      {/* Severity summary */}
      <div className="flex flex-wrap gap-2">
        {data.critical_count > 0 && <Badge severity="critical">{data.critical_count} critical</Badge>}
        {data.high_count > 0 && <Badge severity="high">{data.high_count} high</Badge>}
        {data.medium_count > 0 && <Badge severity="medium">{data.medium_count} medium</Badge>}
        {data.low_count > 0 && <Badge severity="low">{data.low_count} low</Badge>}
        {data.info_count > 0 && <Badge severity="info">{data.info_count} info</Badge>}
      </div>

      {/* AI summary */}
      {data.summary && (
        <div className="rounded-lg border border-border bg-muted/40 p-3 text-sm leading-relaxed text-foreground/90 whitespace-pre-wrap break-words sm:p-4">
          {data.summary}
        </div>
      )}

      {/* Agent breakdown */}
      {Object.keys(agentCounts).length > 0 && (
        <div>
          <h2 className="mb-2 text-sm font-medium uppercase tracking-widest text-muted-foreground">
            Agent breakdown
          </h2>
          <div className="flex flex-wrap gap-2">
            {Object.entries(agentCounts).map(([agent, count]) => (
              <span
                key={agent}
                className="rounded-md border border-border bg-muted/50 px-2.5 py-1 text-xs font-medium"
              >
                {agent}: {count}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Langfuse trace */}
      {data.langfuse_trace_id && (
        <p className="text-xs text-muted-foreground">
          Trace:{' '}
          <code className="rounded bg-muted px-1 py-0.5 font-mono">{data.langfuse_trace_id}</code>
        </p>
      )}

      {/* Findings */}
      <div>
        <h2 className="mb-3 text-sm font-medium uppercase tracking-widest text-muted-foreground">
          Findings ({data.findings.length})
        </h2>
        {data.findings.length > 0 ? (
          <div className="space-y-3">
            {data.findings.map((finding) => (
              <FindingItem key={finding.id} finding={finding} />
            ))}
          </div>
        ) : (
          <EmptyState message="No findings for this review." />
        )}
      </div>
    </div>
  );
}

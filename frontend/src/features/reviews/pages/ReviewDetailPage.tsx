import { Link, useParams } from 'react-router-dom';

import { useReviewDetail } from '@/features/reviews/hooks/useReviews';
import { FindingItem } from '@/features/reviews/components/FindingItem';
import { Badge } from '@/shared/components/Badge';
import { Spinner } from '@/shared/components/Spinner';
import { EmptyState } from '@/shared/components/EmptyState';
import { formatDate } from '@/shared/utils/formatDate';

export function ReviewDetailPage() {
  const { id = '' } = useParams();
  const { data, isLoading, error } = useReviewDetail(id);

  if (isLoading) return <Spinner />;
  if (error || !data) return <EmptyState message="Review not found." />;

  const agentCounts = data.findings.reduce<Record<string, number>>((acc, f) => {
    acc[f.agent_source] = (acc[f.agent_source] ?? 0) + 1;
    return acc;
  }, {});

  return (
    <div className="space-y-6">
      <div>
        <Link to="/reviews" className="text-sm text-primary hover:underline">
          ← Back to reviews
        </Link>
        <h1 className="mt-2 text-2xl font-semibold">PR #{data.pr_number}</h1>
        <p className="text-sm text-muted-foreground">
          {formatDate(data.created_at)} ·{' '}
          <a href={data.pr_url} target="_blank" rel="noreferrer" className="text-primary hover:underline">
            View on GitHub
          </a>
        </p>
      </div>

      {data.summary && (
        <div className="rounded-lg border border-border bg-muted/20 p-4 text-sm whitespace-pre-wrap">
          {data.summary}
        </div>
      )}

      <div className="flex flex-wrap gap-2">
        {data.critical_count > 0 && <Badge severity="critical">{data.critical_count} critical</Badge>}
        {data.high_count > 0 && <Badge severity="high">{data.high_count} high</Badge>}
        {data.medium_count > 0 && <Badge severity="medium">{data.medium_count} medium</Badge>}
        {data.low_count > 0 && <Badge severity="low">{data.low_count} low</Badge>}
        {data.info_count > 0 && <Badge severity="info">{data.info_count} info</Badge>}
      </div>

      <div>
        <h2 className="mb-2 text-lg font-medium">Agent breakdown</h2>
        <div className="flex flex-wrap gap-2 text-sm text-muted-foreground">
          {Object.entries(agentCounts).map(([agent, count]) => (
            <span key={agent} className="rounded-md bg-muted px-2 py-1">
              {agent}: {count}
            </span>
          ))}
        </div>
      </div>

      {data.langfuse_trace_id && (
        <p className="text-sm text-muted-foreground">
          Langfuse trace: <code>{data.langfuse_trace_id}</code>
        </p>
      )}

      <div className="space-y-3">
        <h2 className="text-lg font-medium">Findings ({data.findings.length})</h2>
        {data.findings.map((finding) => (
          <FindingItem key={finding.id} finding={finding} />
        ))}
      </div>
    </div>
  );
}

import { Link } from 'react-router-dom';

import type { ReviewSummaryDTO } from '@/shared/types/api';
import { Badge } from '@/shared/components/Badge';
import { formatDate } from '@/shared/utils/formatDate';

function repoFromPrUrl(url: string): string {
  try {
    const parts = new URL(url).pathname.split('/').filter(Boolean);
    if (parts.length >= 2) return `${parts[0]}/${parts[1]}`;
    return '';
  } catch {
    return '';
  }
}

export function ReviewCard({ review }: { review: ReviewSummaryDTO }) {
  const repoName = repoFromPrUrl(review.pr_url);

  return (
    <Link
      to={`/reviews/${review.id}`}
      className="group block rounded-lg border border-border bg-card p-3 shadow-card transition-shadow hover:shadow-md sm:p-4"
    >
      {/* Top row: text info + badges */}
      <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between sm:gap-4">
        <div className="min-w-0">
          {repoName && (
            <p className="mb-0.5 truncate text-xs font-medium text-muted-foreground">
              {repoName}
            </p>
          )}
          <p className="font-medium transition-colors group-hover:text-primary">
            PR #{review.pr_number}
          </p>
          <p className="mt-1 text-xs text-muted-foreground">{formatDate(review.created_at)}</p>
          <p className="mt-1 text-xs text-muted-foreground">
            {review.total_findings} finding{review.total_findings !== 1 ? 's' : ''}
            {review.agents_run.length > 0 && ` · ${review.agents_run.join(', ')}`}
          </p>
        </div>

        {/* Badges — align left on mobile, right on sm+ */}
        <div className="flex flex-wrap gap-1 sm:shrink-0 sm:justify-end">
          {review.critical_count > 0 && <Badge severity="critical">{review.critical_count} crit</Badge>}
          {review.high_count > 0 && <Badge severity="high">{review.high_count} high</Badge>}
          {review.medium_count > 0 && <Badge severity="medium">{review.medium_count} med</Badge>}
        </div>
      </div>
    </Link>
  );
}

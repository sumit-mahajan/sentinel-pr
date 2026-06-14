import type { ReviewSummaryDTO } from '@/shared/types/api';
import { Badge } from '@/shared/components/Badge';
import { Card } from '@/shared/components/Card';
import { formatDate } from '@/shared/utils/formatDate';
import { Link } from 'react-router-dom';

export function ReviewCard({ review }: { review: ReviewSummaryDTO }) {
  return (
    <Card>
      <div className="flex items-start justify-between gap-4">
        <div>
          <Link to={`/reviews/${review.id}`} className="font-medium hover:text-primary">
            PR #{review.pr_number}
          </Link>
          <p className="mt-1 text-sm text-muted-foreground">{formatDate(review.created_at)}</p>
          <p className="mt-2 text-xs text-muted-foreground">
            {review.total_findings} findings · {review.agents_run.join(', ') || 'no agents'}
          </p>
        </div>
        <div className="flex flex-wrap gap-1">
          {review.critical_count > 0 && <Badge severity="critical">{review.critical_count} crit</Badge>}
          {review.high_count > 0 && <Badge severity="high">{review.high_count} high</Badge>}
          {review.medium_count > 0 && <Badge severity="medium">{review.medium_count} med</Badge>}
        </div>
      </div>
    </Card>
  );
}

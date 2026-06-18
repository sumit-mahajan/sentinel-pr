import { useReviews } from '@/features/reviews/hooks/useReviews';
import { ReviewCard } from '@/features/reviews/components/ReviewCard';
import { Skeleton } from '@/shared/components/Skeleton';
import { EmptyState } from '@/shared/components/EmptyState';

function ReviewListSkeleton() {
  return (
    <div className="space-y-3">
      {Array.from({ length: 5 }).map((_, i) => (
        <Skeleton key={i} className="h-24 rounded-lg" />
      ))}
    </div>
  );
}

export function ReviewHistoryPage() {
  const { data, isLoading, error } = useReviews();

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Review history</h1>
        {data && (
          <p className="mt-1 text-sm text-muted-foreground">
            {data.total} review{data.total !== 1 ? 's' : ''} total
          </p>
        )}
      </div>

      {isLoading && <ReviewListSkeleton />}

      {error && <EmptyState message="Failed to load reviews." />}

      {!isLoading && !error && !data?.items.length && (
        <EmptyState message="No reviews yet. Open a PR on an installed repo to trigger a review." />
      )}

      {!isLoading && !error && data?.items.length ? (
        <div className="grid gap-3">
          {data.items.map((review, i) => (
            <div
              key={review.id}
              className="animate-fade-in"
              style={{ animationDelay: `${i * 40}ms` }}
            >
              <ReviewCard review={review} />
            </div>
          ))}
        </div>
      ) : null}
    </div>
  );
}

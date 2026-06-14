import { useReviews } from '@/features/reviews/hooks/useReviews';
import { ReviewCard } from '@/features/reviews/components/ReviewCard';
import { Spinner } from '@/shared/components/Spinner';
import { EmptyState } from '@/shared/components/EmptyState';

export function ReviewHistoryPage() {
  const { data, isLoading, error } = useReviews();

  if (isLoading) return <Spinner />;
  if (error) return <EmptyState message="Failed to load reviews." />;
  if (!data?.items.length) return <EmptyState message="No reviews yet. Open a PR on an installed repo to trigger a review." />;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">Review history</h1>
        <p className="text-sm text-muted-foreground">{data.total} reviews total</p>
      </div>
      <div className="grid gap-4">
        {data.items.map((review) => (
          <ReviewCard key={review.id} review={review} />
        ))}
      </div>
    </div>
  );
}

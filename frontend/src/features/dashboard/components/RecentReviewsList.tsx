import type { ReviewSummaryDTO } from '@/shared/types/api';
import { ReviewCard } from '@/features/reviews/components/ReviewCard';

export function RecentReviewsList({ reviews }: { reviews: ReviewSummaryDTO[] }) {
  return (
    <div className="grid gap-3">
      {reviews.map((review) => (
        <ReviewCard key={review.id} review={review} />
      ))}
    </div>
  );
}

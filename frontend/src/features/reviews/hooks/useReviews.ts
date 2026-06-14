import { useQuery } from '@tanstack/react-query';

import { reviewsApi } from '@/features/reviews/api/reviewsApi';

export function useReviews(repoId?: string, page = 1) {
  return useQuery({
    queryKey: ['reviews', repoId ?? 'all', page],
    queryFn: async () => (await reviewsApi.list({ repo_id: repoId, page })).data,
  });
}

export function useReviewDetail(reviewId: string) {
  return useQuery({
    queryKey: ['reviews', reviewId],
    queryFn: async () => (await reviewsApi.getById(reviewId)).data,
    enabled: Boolean(reviewId),
  });
}

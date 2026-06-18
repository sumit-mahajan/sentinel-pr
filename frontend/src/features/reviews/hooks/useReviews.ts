import { useQuery, useQueryClient } from '@tanstack/react-query';

import { reviewsApi } from '@/features/reviews/api/reviewsApi';

// Review list: 2 min (new PRs could arrive)
const LIST_STALE  = 2 * 60 * 1000;
// Review detail: immutable once created — cache for 10 min
const DETAIL_STALE = 10 * 60 * 1000;

export function useReviews(repoId?: string, page = 1) {
  return useQuery({
    queryKey: ['reviews', repoId ?? 'all', page],
    queryFn: async () => (await reviewsApi.list({ repo_id: repoId, page })).data,
    staleTime: LIST_STALE,
  });
}

export function useReviewDetail(reviewId: string) {
  return useQuery({
    queryKey: ['reviews', reviewId],
    queryFn: async () => (await reviewsApi.getById(reviewId)).data,
    enabled: Boolean(reviewId),
    staleTime: DETAIL_STALE,
  });
}

/** Call on nav-link hover to pre-load the reviews list before the user arrives */
export function usePrefetchReviews() {
  const queryClient = useQueryClient();
  return () =>
    queryClient.prefetchQuery({
      queryKey: ['reviews', 'all', 1],
      queryFn: async () => (await reviewsApi.list({ page: 1 })).data,
      staleTime: LIST_STALE,
    });
}

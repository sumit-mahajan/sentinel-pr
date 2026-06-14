import { apiClient } from '@/shared/utils/apiClient';
import type { PaginatedResponse, ReviewDetailDTO, ReviewSummaryDTO } from '@/shared/types/api';

export const reviewsApi = {
  list: (params?: { repo_id?: string; page?: number; limit?: number }) =>
    apiClient.get<PaginatedResponse<ReviewSummaryDTO>>('/reviews', { params }),
  getById: (id: string) => apiClient.get<ReviewDetailDTO>(`/reviews/${id}`),
};

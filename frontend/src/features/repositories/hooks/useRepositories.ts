import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { repositoriesApi } from '@/features/repositories/api/repositoriesApi';
import type { UpdateAgentConfigRequest } from '@/shared/types/api';

// Repos change rarely — keep as fresh for 5 minutes
const REPOS_STALE = 5 * 60 * 1000;

export function useRepositories() {
  return useQuery({
    queryKey: ['repos'],
    queryFn: async () => (await repositoriesApi.list()).data,
    staleTime: REPOS_STALE,
  });
}

export function useRepository(id: string) {
  const query = useRepositories();
  return {
    ...query,
    data: query.data?.find((r) => r.id === id),
  };
}

/** Call on nav-link hover to pre-load repos before the user arrives */
export function usePrefetchRepositories() {
  const queryClient = useQueryClient();
  return () =>
    queryClient.prefetchQuery({
      queryKey: ['repos'],
      queryFn: async () => (await repositoriesApi.list()).data,
      staleTime: REPOS_STALE,
    });
}

export function useAgentConfig(repoId: string) {
  return useQuery({
    queryKey: ['repos', repoId, 'config'],
    queryFn: async () => (await repositoriesApi.getConfig(repoId)).data,
    enabled: Boolean(repoId),
    staleTime: REPOS_STALE,
  });
}

export function useUpdateAgentConfig(repoId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (body: UpdateAgentConfigRequest) =>
      repositoriesApi.updateConfig(repoId, body).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['repos'] });
      queryClient.invalidateQueries({ queryKey: ['repos', repoId, 'config'] });
    },
  });
}

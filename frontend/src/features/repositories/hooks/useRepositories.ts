import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { repositoriesApi } from '@/features/repositories/api/repositoriesApi';
import type { UpdateAgentConfigRequest } from '@/shared/types/api';

export function useRepositories() {
  return useQuery({
    queryKey: ['repos'],
    queryFn: async () => (await repositoriesApi.list()).data,
  });
}

export function useAgentConfig(repoId: string) {
  return useQuery({
    queryKey: ['repos', repoId, 'config'],
    queryFn: async () => (await repositoriesApi.getConfig(repoId)).data,
    enabled: Boolean(repoId),
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

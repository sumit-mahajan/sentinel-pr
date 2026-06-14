import { apiClient } from '@/shared/utils/apiClient';
import type { AgentConfigDTO, RepoDTO, UpdateAgentConfigRequest } from '@/shared/types/api';

export const repositoriesApi = {
  list: () => apiClient.get<RepoDTO[]>('/repos'),
  getConfig: (repoId: string) => apiClient.get<AgentConfigDTO>(`/repos/${repoId}/config`),
  updateConfig: (repoId: string, body: UpdateAgentConfigRequest) =>
    apiClient.patch<AgentConfigDTO>(`/repos/${repoId}/config`, body),
};

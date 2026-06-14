export interface UserDTO {
  id: string;
  github_id: number;
  login: string;
  avatar_url: string | null;
}

export interface AuthTokenDTO {
  access_token: string;
  token_type: 'bearer';
  user: UserDTO;
}

export interface AgentConfigDTO {
  repository_id: string;
  security_enabled: boolean;
  perf_enabled: boolean;
  arch_enabled: boolean;
  test_enabled: boolean;
  min_severity: string;
}

export interface UpdateAgentConfigRequest {
  security_enabled?: boolean;
  perf_enabled?: boolean;
  arch_enabled?: boolean;
  test_enabled?: boolean;
  min_severity?: string;
  is_active?: boolean;
}

export interface RepoDTO {
  id: string;
  github_id: number;
  full_name: string;
  default_branch: string;
  is_active: boolean;
  language: string | null;
  agent_config: AgentConfigDTO;
}

export interface FindingDTO {
  id: string;
  severity: string;
  category: string;
  agent_source: string;
  file_path: string;
  line_start: number | null;
  line_end: number | null;
  title: string;
  description: string;
  fix_suggestion: string | null;
}

export interface ReviewSummaryDTO {
  id: string;
  pr_number: number;
  pr_url: string;
  head_sha: string;
  total_findings: number;
  critical_count: number;
  high_count: number;
  medium_count: number;
  low_count: number;
  info_count: number;
  agents_run: string[];
  posted_to_github: boolean;
  created_at: string;
}

export interface ReviewDetailDTO extends ReviewSummaryDTO {
  summary: string | null;
  langfuse_trace_id: string | null;
  findings: FindingDTO[];
}

export interface JobStatusDTO {
  id: string;
  pr_number: number;
  pr_url: string;
  head_sha: string;
  status: string;
  attempt_count: number;
  error_message: string | null;
  enqueued_at: string;
  started_at: string | null;
  completed_at: string | null;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  has_next: boolean;
}

export interface ApiError {
  error: {
    code: string;
    message: string;
    details: Record<string, unknown>;
  };
}

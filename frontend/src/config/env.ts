const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? '/api/v1';
const githubAppSlug = import.meta.env.VITE_GITHUB_APP_SLUG ?? '';

export const env = {
  VITE_API_BASE_URL: apiBaseUrl,
  VITE_GITHUB_APP_SLUG: githubAppSlug,
  githubAppInstallUrl: githubAppSlug
    ? `https://github.com/apps/${githubAppSlug}/installations/new`
    : 'https://github.com/apps',
} as const;

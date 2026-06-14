import { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';

import { useAuthStore } from '@/features/auth/store/authStore';
import { apiClient } from '@/shared/utils/apiClient';
import type { AuthTokenDTO } from '@/shared/types/api';
import { Spinner } from '@/shared/components/Spinner';

export function CallbackPage() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const setAuth = useAuthStore((s) => s.setAuth);

  useEffect(() => {
    const code = params.get('code');
    const state = params.get('state');
    if (!code || !state) {
      navigate('/login');
      return;
    }

    apiClient
      .get<AuthTokenDTO>('/auth/callback', { params: { code, state } })
      .then((res) => {
        setAuth(res.data.access_token, res.data.user);
        navigate('/');
      })
      .catch(() => navigate('/login'));
  }, [params, navigate, setAuth]);

  return <Spinner />;
}

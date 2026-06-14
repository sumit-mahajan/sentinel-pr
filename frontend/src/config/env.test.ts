import { describe, expect, it } from 'vitest';

import { env } from '@/config/env';

describe('env', () => {
  it('exposes API base URL', () => {
    expect(env.VITE_API_BASE_URL).toBeTruthy();
  });
});

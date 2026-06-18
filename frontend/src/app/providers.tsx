import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { Toaster } from 'sonner';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime:            60 * 1000,       // 1 min — show cached data immediately, revalidate quietly
      gcTime:               15 * 60 * 1000,  // 15 min — keep data in memory between page visits
      retry:                1,
      refetchOnWindowFocus: false,           // don't re-fetch just because the user alt-tabbed back
      refetchOnReconnect:   true,            // do re-fetch when network comes back
    },
  },
});

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <Toaster richColors position="top-right" />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}

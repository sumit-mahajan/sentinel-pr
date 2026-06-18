import { Github } from 'lucide-react';
import { Link } from 'react-router-dom';

import { env } from '@/config/env';
import { useAuthStore } from '@/features/auth/store/authStore';
import { ThemeToggle } from '@/shared/components/ThemeToggle';
import { cn } from '@/shared/utils/cn';

/* ── Shared container class ───────────────────────────────────────────── */
const CONTAINER = 'mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8 2xl:max-w-[1440px]';

const features = [
  {
    icon: (
      <svg className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z" />
      </svg>
    ),
    label: 'Security',
    desc: 'OWASP Top 10, hardcoded secrets, injection flaws, insecure patterns — caught before merge.',
  },
  {
    icon: (
      <svg className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75Z" />
      </svg>
    ),
    label: 'Performance',
    desc: 'N+1 queries, blocking I/O, algorithmic regressions, unnecessary re-renders.',
  },
  {
    icon: (
      <svg className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12.75V12A2.25 2.25 0 0 1 4.5 9.75h15A2.25 2.25 0 0 1 21.75 12v.75m-8.69-6.44-2.12-2.12a1.5 1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44Z" />
      </svg>
    ),
    label: 'Architecture',
    desc: 'Layer violations, tight coupling, circular dependencies, module boundary breaches.',
  },
  {
    icon: (
      <svg className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" d="m6.75 7.5 3 2.25-3 2.25m4.5 0h3m-9 8.25h13.5A2.25 2.25 0 0 0 21 18V6a2.25 2.25 0 0 0-2.25-2.25H5.25A2.25 2.25 0 0 0 3 6v12a2.25 2.25 0 0 0 2.25 2.25Z" />
      </svg>
    ),
    label: 'Test coverage',
    desc: 'Missing tests for changed functions, weak assertions, test-to-code ratio regressions.',
  },
];

const steps = [
  { n: '01', title: 'Install the GitHub App', desc: 'One-click install on any org or repo. No tokens to manage.' },
  { n: '02', title: 'Open a pull request',    desc: 'ReviewGraph triggers automatically on open, push, or reopen.' },
  { n: '03', title: 'Review in seconds',      desc: 'Line-level comments appear directly in the PR with severity ratings and fix suggestions.' },
];

export function LandingPage() {
  const isSignedIn = useAuthStore((s) => Boolean(s.token));

  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground">

      {/* ── Nav ─────────────────────────────────────────────────────── */}
      <header className="sticky top-0 z-10 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80">
        <div className={cn(CONTAINER, 'flex h-14 items-center justify-between')}>
          <div className="flex items-center gap-2">
            <img src="/logo.png" alt="ReviewGraph" className="h-7 w-7 rounded-lg" />
            <span className="text-sm font-semibold">ReviewGraph</span>
          </div>
          <div className="flex items-center gap-2">
            {!isSignedIn && (
              <a
                href={env.githubAppInstallUrl}
                target="_blank"
                rel="noreferrer"
                className="hidden text-sm text-muted-foreground underline-offset-4 hover:text-foreground hover:underline sm:block"
              >
                Install App
              </a>
            )}
            <ThemeToggle />
            {isSignedIn ? (
              <Link
                to="/dashboard"
                className="inline-flex items-center gap-1.5 rounded-md bg-primary px-3 py-1.5 text-sm font-medium text-primary-foreground transition-opacity hover:opacity-90"
              >
                Go to Dashboard →
              </Link>
            ) : (
              <Link
                to="/login"
                className="inline-flex items-center gap-1.5 rounded-md border border-input bg-background px-3 py-1.5 text-sm font-medium transition-colors hover:bg-accent"
              >
                Sign in
              </Link>
            )}
          </div>
        </div>
      </header>

      {/* ── Hero ─────────────────────────────────────────────────────── */}
      <section className="animate-fade-in">
        <div className={cn(CONTAINER, 'flex flex-col items-center pb-16 pt-14 text-center sm:pt-20 lg:pb-24 lg:pt-28 2xl:pt-36')}>
          <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-border bg-muted/50 px-3 py-1 text-xs text-muted-foreground">
            <span className="h-1.5 w-1.5 rounded-full bg-primary" />
            Multi-agent · Gemini 2.5 Flash · LangGraph
          </div>

          <h1 className="max-w-3xl text-3xl font-bold tracking-tight sm:text-4xl lg:text-5xl xl:text-6xl">
            AI code review that actually{' '}
            <span className="text-primary">finds the bugs</span>
          </h1>

          <p className="mt-5 max-w-xl text-base text-muted-foreground sm:text-lg xl:max-w-2xl xl:text-xl">
            Four specialist AI agents review every pull request for security vulnerabilities,
            performance issues, architecture violations, and missing tests — before your team does.
          </p>

          <div className="mt-8 flex flex-wrap justify-center gap-3">
            {isSignedIn ? (
              <Link
                to="/dashboard"
                className="inline-flex items-center gap-2 rounded-md bg-primary px-5 py-2.5 text-sm font-semibold text-primary-foreground shadow-sm transition-opacity hover:opacity-90 lg:px-6 lg:py-3 lg:text-base"
              >
                Go to Dashboard →
              </Link>
            ) : (
              <>
                <a
                  href={`${env.VITE_API_BASE_URL}/auth/github`}
                  className="inline-flex items-center gap-2 rounded-md bg-primary px-5 py-2.5 text-sm font-semibold text-primary-foreground shadow-sm transition-opacity hover:opacity-90 lg:px-6 lg:py-3 lg:text-base"
                >
                  <Github className="h-4 w-4 lg:h-5 lg:w-5" />
                  Start for free
                </a>
                <a
                  href={env.githubAppInstallUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-2 rounded-md border border-input bg-background px-5 py-2.5 text-sm font-medium transition-colors hover:bg-accent lg:px-6 lg:py-3 lg:text-base"
                >
                  Install GitHub App ↗
                </a>
              </>
            )}
          </div>
        </div>
      </section>

      {/* ── Feature grid ─────────────────────────────────────────────── */}
      <section className="border-t border-border bg-muted/20 py-12 sm:py-16 lg:py-20">
        <div className={CONTAINER}>
          <p className="mb-1 text-center text-xs font-semibold uppercase tracking-widest text-muted-foreground">
            What gets reviewed
          </p>
          <h2 className="mb-8 text-center text-2xl font-semibold tracking-tight sm:mb-10 lg:text-3xl">
            Four agents. One complete review.
          </h2>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4 lg:gap-6">
            {features.map((f, i) => (
              <div
                key={f.label}
                className="animate-fade-in rounded-lg border border-border bg-card p-5 shadow-card lg:p-6"
                style={{ animationDelay: `${i * 60}ms` }}
              >
                <div className="mb-3 flex h-9 w-9 items-center justify-center rounded-md bg-primary/10 text-primary lg:h-10 lg:w-10">
                  {f.icon}
                </div>
                <h3 className="mb-1.5 font-semibold">{f.label}</h3>
                <p className="text-sm leading-relaxed text-muted-foreground">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── How it works ─────────────────────────────────────────────── */}
      <section className="py-12 sm:py-16 lg:py-20">
        <div className={CONTAINER}>
          <p className="mb-1 text-center text-xs font-semibold uppercase tracking-widest text-muted-foreground">
            How it works
          </p>
          <h2 className="mb-8 text-center text-2xl font-semibold tracking-tight sm:mb-10 lg:text-3xl">
            Set up in under two minutes
          </h2>
          <div className="grid gap-6 sm:grid-cols-3 lg:gap-10">
            {steps.map((s, i) => (
              <div
                key={s.n}
                className={cn('relative flex gap-4 animate-fade-in')}
                style={{ animationDelay: `${i * 80}ms` }}
              >
                {i < steps.length - 1 && (
                  <span className="absolute left-5 top-10 hidden h-full w-px bg-border sm:block" />
                )}
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-border bg-muted text-xs font-bold tabular-nums text-muted-foreground">
                  {s.n}
                </div>
                <div className="pt-1">
                  <h3 className="mb-1 font-semibold">{s.title}</h3>
                  <p className="text-sm text-muted-foreground">{s.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA banner ───────────────────────────────────────────────── */}
      <section className="border-t border-border bg-muted/20 py-12 sm:py-16 lg:py-20">
        <div className={cn(CONTAINER, 'text-center')}>
          <h2 className="mb-3 text-2xl font-semibold tracking-tight lg:text-3xl">
            Ready to ship safer code?
          </h2>
          <p className="mb-7 text-sm text-muted-foreground lg:text-base">
            Free while in beta. No credit card required.
          </p>
          <a
            href={`${env.VITE_API_BASE_URL}/auth/github`}
            className="inline-flex items-center gap-2 rounded-md bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground shadow-sm transition-opacity hover:opacity-90 lg:px-8 lg:py-3.5 lg:text-base"
          >
            <Github className="h-4 w-4" />
            Get started with GitHub
          </a>
        </div>
      </section>

      {/* ── Footer ───────────────────────────────────────────────────── */}
      <footer className="border-t border-border py-8">
        <div className={cn(CONTAINER, 'flex flex-col items-center justify-between gap-3 text-xs text-muted-foreground sm:flex-row')}>
          <div className="flex items-center gap-2">
            <img src="/logo.png" alt="" className="h-4 w-4 rounded" />
            <span>ReviewGraph</span>
          </div>
          <span>© {new Date().getFullYear()} ReviewGraph. All rights reserved.</span>
          <div className="flex gap-4">
            <a href={env.githubAppInstallUrl} target="_blank" rel="noreferrer" className="hover:text-foreground">
              GitHub App
            </a>
            <Link to="/login" className="hover:text-foreground">
              Sign in
            </Link>
          </div>
        </div>
      </footer>
    </div>
  );
}

import { useEffect, useState } from "react";
import { Link, Outlet, useLocation } from "react-router-dom";
import { Menu, X } from "lucide-react";

import { UserMenu } from "@/features/auth/components/UserMenu";
import { ThemeToggle } from "@/shared/components/ThemeToggle";
import { usePrefetchRepositories } from "@/features/repositories/hooks/useRepositories";
import { usePrefetchReviews } from "@/features/reviews/hooks/useReviews";
import { cn } from "@/shared/utils/cn";

const nav = [
  { to: "/dashboard", label: "Dashboard", prefetch: "reviews" as const },
  { to: "/repos", label: "Repositories", prefetch: "repos" as const },
  { to: "/reviews", label: "Reviews", prefetch: "reviews" as const },
];

export function AppLayout() {
  const { pathname } = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);

  const prefetchRepos = usePrefetchRepositories();
  const prefetchReviews = usePrefetchReviews();

  const prefetchFns = { repos: prefetchRepos, reviews: prefetchReviews };

  // Close mobile nav whenever the route changes
  useEffect(() => {
    setMobileOpen(false);
  }, [pathname]);

  // Eagerly prefetch the most likely next page data on first render
  useEffect(() => {
    // After 800ms (enough for initial render to settle), prefetch both datasets
    const t = setTimeout(() => {
      prefetchRepos();
      prefetchReviews();
    }, 800);
    return () => clearTimeout(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-20 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80">
        {/* Main bar */}
        <div className="mx-auto flex h-14 max-w-7xl items-center justify-between px-4 sm:px-6 2xl:max-w-[1440px]">
          {/* Left: logo + desktop nav */}
          <div className="flex items-center gap-4 sm:gap-5">
            <Link
              to="/"
              className="flex shrink-0 items-center gap-2 text-sm font-semibold tracking-tight"
            >
              <img
                src="/logo.png"
                alt="ReviewGraph"
                className="h-6 w-6 rounded-md"
              />
              <span>ReviewGraph</span>
            </Link>

            {/* Desktop nav — hidden on mobile */}
            <nav className="hidden items-center gap-0.5 md:flex">
              {nav.map(({ to, label, prefetch }) => {
                const isActive =
                  pathname === to || pathname.startsWith(to + "/");
                return (
                  <Link
                    key={to}
                    to={to}
                    onMouseEnter={() => prefetchFns[prefetch]()}
                    className={cn(
                      "rounded-md px-3 py-1.5 text-sm transition-colors",
                      isActive
                        ? "bg-accent font-medium text-foreground"
                        : "text-muted-foreground hover:bg-accent/60 hover:text-foreground",
                    )}
                  >
                    {label}
                  </Link>
                );
              })}
            </nav>
          </div>

          {/* Right: theme + user + hamburger */}
          <div className="flex items-center gap-1">
            <ThemeToggle />
            <UserMenu />
            {/* Hamburger — mobile only */}
            <button
              className="ml-1 inline-flex h-9 w-9 items-center justify-center rounded-md text-muted-foreground transition-colors hover:bg-accent hover:text-foreground md:hidden"
              onClick={() => setMobileOpen((o) => !o)}
              aria-label={mobileOpen ? "Close navigation" : "Open navigation"}
            >
              {mobileOpen ? (
                <X className="h-4 w-4" />
              ) : (
                <Menu className="h-4 w-4" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile nav panel */}
        {mobileOpen && (
          <div className="animate-fade-in-fast border-t border-border bg-background/98 px-4 pb-3 pt-2 md:hidden">
            <nav className="flex flex-col gap-0.5">
              {nav.map(({ to, label, prefetch }) => {
                const isActive =
                  pathname === to || pathname.startsWith(to + "/");
                return (
                  <Link
                    key={to}
                    to={to}
                    onMouseEnter={() => prefetchFns[prefetch]()}
                    className={cn(
                      "rounded-md px-3 py-3 text-sm font-medium transition-colors",
                      isActive
                        ? "bg-accent text-foreground"
                        : "text-muted-foreground hover:bg-accent hover:text-foreground",
                    )}
                  >
                    {label}
                  </Link>
                );
              })}
            </nav>
          </div>
        )}
      </header>

      <main className="mx-auto max-w-7xl px-4 py-6 sm:px-6 sm:py-8 lg:px-8 lg:py-10 2xl:max-w-[1440px] animate-fade-in">
        <Outlet />
      </main>
    </div>
  );
}

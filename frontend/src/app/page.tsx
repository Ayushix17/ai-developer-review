import { ReviewWorkbench } from "@/components/review-workbench";

export default function Home() {
  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(14,165,233,0.14),_transparent_32%),linear-gradient(180deg,#070b14_0%,#0a1020_100%)]">
      <div className="mx-auto flex min-h-screen w-full max-w-7xl flex-col px-4 py-5 sm:px-6 lg:px-8">
        <header className="flex flex-wrap items-center justify-between gap-4 border-b border-white/10 pb-5">
          <div>
            <p className="text-xs uppercase tracking-[0.3em] text-sky-300">AI code review platform</p>
            <h1 className="mt-2 text-2xl font-semibold text-slate-50">
              AI Developer Review
            </h1>
          </div>
          <div className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-300">
            Next.js frontend, FastAPI backend, PostgreSQL storage
          </div>
        </header>

        <div className="flex-1 py-5">
          <ReviewWorkbench />
        </div>
      </div>
    </main>
  );
}

'use client';

import { useEffect, useMemo, useState } from "react";
import type {
  AnalysisDetail,
  AnalysisListItem,
  AnalyzeResponse,
  Finding,
} from "@/lib/types";
import { apiRequest, buildApiUrl, getApiBaseUrl } from "@/lib/api";

type TabKey = "analyze" | "history" | "settings";

function formatMoney(value: number) {
  return `$${value.toFixed(6)}`;
}

function formatTimestamp(value: string) {
  return new Intl.DateTimeFormat("en-US", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

function severityClass(severity: string) {
  switch (severity.toLowerCase()) {
    case "blocker":
      return "border-rose-500/40 bg-rose-500/10 text-rose-200";
    case "warn":
      return "border-amber-500/40 bg-amber-500/10 text-amber-200";
    default:
      return "border-sky-500/40 bg-sky-500/10 text-sky-200";
  }
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl border border-white/10 bg-white/5 px-3 py-2">
      <p className="text-[11px] uppercase tracking-wide text-slate-400">{label}</p>
      <p className="mt-1 text-sm font-semibold text-slate-50">{value}</p>
    </div>
  );
}

function SettingItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl border border-white/10 bg-slate-950/70 p-4">
      <p className="text-[11px] uppercase tracking-wide text-slate-400">{label}</p>
      <p className="mt-2 break-words font-mono text-sm text-slate-100">{value}</p>
    </div>
  );
}

function StatusCard({
  label,
  value,
  tone,
}: {
  label: string;
  value: string;
  tone: "unknown" | "healthy" | "error";
}) {
  const toneClass =
    tone === "healthy"
      ? "border-emerald-500/30 bg-emerald-500/10 text-emerald-200"
      : tone === "error"
        ? "border-rose-500/30 bg-rose-500/10 text-rose-200"
        : "border-white/10 bg-white/5 text-slate-200";

  return (
    <div className={`rounded-xl border px-4 py-3 ${toneClass}`}>
      <p className="text-[11px] uppercase tracking-wide text-slate-300">{label}</p>
      <p className="mt-2 text-sm font-medium">{value}</p>
    </div>
  );
}

function FindingRow({ finding }: { finding: Finding }) {
  return (
    <article className="rounded-xl border border-white/10 bg-white/[0.03] p-4">
      <div className="flex flex-wrap items-center gap-2">
        <span
          className={`rounded-full border px-2 py-1 text-[11px] font-semibold uppercase tracking-wide ${severityClass(
            finding.severity,
          )}`}
        >
          {finding.severity}
        </span>
        <span className="rounded-full border border-white/10 bg-white/5 px-2 py-1 text-[11px] uppercase tracking-wide text-slate-300">
          {finding.category}
        </span>
        {finding.line_number ? (
          <span className="text-xs text-slate-400">Line {finding.line_number}</span>
        ) : null}
      </div>
      <h3 className="mt-3 text-sm font-semibold text-slate-50">{finding.title}</h3>
      <p className="mt-2 text-sm leading-6 text-slate-300">{finding.description}</p>
      {finding.suggestion ? (
        <pre className="mt-3 overflow-x-auto rounded-lg border border-white/10 bg-slate-950/70 p-3 text-xs leading-6 text-slate-200">
          {finding.suggestion}
        </pre>
      ) : null}
    </article>
  );
}

export function ReviewWorkbench() {
  const [tab, setTab] = useState<TabKey>("analyze");
  const [language, setLanguage] = useState("python");
  const [code, setCode] = useState(`import os\n\n\ndef greet(name):\n    print(f"Hello, {name}")\n`);
  const [context, setContext] = useState("");
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [analysisError, setAnalysisError] = useState<string | null>(null);
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [history, setHistory] = useState<AnalysisListItem[]>([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [historyError, setHistoryError] = useState<string | null>(null);
  const [selectedAnalysis, setSelectedAnalysis] = useState<AnalysisDetail | null>(null);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [healthState, setHealthState] = useState<"unknown" | "healthy" | "error">("unknown");
  const [healthLabel, setHealthLabel] = useState("Checking backend...");

  const apiBaseUrl = useMemo(() => getApiBaseUrl(), []);

  useEffect(() => {
    let cancelled = false;

    fetch(buildApiUrl("/health"))
      .then(async (response) => {
        if (!response.ok) {
          throw new Error("Backend unavailable");
        }
        return response.json();
      })
      .then(() => {
        if (!cancelled) {
          setHealthState("healthy");
          setHealthLabel("Backend connected");
        }
      })
      .catch(() => {
        if (!cancelled) {
          setHealthState("error");
          setHealthLabel("Backend not reachable");
        }
      });

    return () => {
      cancelled = true;
    };
  }, []);

  async function loadAnalysisDetail(id: number) {
    setSelectedId(id);
    try {
      const detail = await apiRequest<AnalysisDetail>(`/analyses/${id}`);
      setSelectedAnalysis(detail);
    } catch (error) {
      setHistoryError(error instanceof Error ? error.message : "Could not load analysis.");
    }
  }

  async function loadHistory() {
    setHistoryLoading(true);
    setHistoryError(null);
    try {
      const rows = await apiRequest<AnalysisListItem[]>("/analyses");
      setHistory(rows);
      if (rows.length && selectedId === null) {
        void loadAnalysisDetail(rows[0].id);
      }
    } catch (error) {
      setHistoryError(error instanceof Error ? error.message : "Could not load history.");
    } finally {
      setHistoryLoading(false);
    }
  }

  async function runAnalysis() {
    if (!code.trim()) {
      setAnalysisError("Paste code before running a review.");
      return;
    }

    setAnalysisLoading(true);
    setAnalysisError(null);
    try {
      const data = await apiRequest<AnalyzeResponse>("/analyze", {
        method: "POST",
        body: JSON.stringify({
          code,
          language,
          source_type: "pasted_code",
          context: context.trim() || null,
        }),
      });
      setResult(data);
      setTab("analyze");
      if (history.length) {
        void loadHistory();
      }
    } catch (error) {
      setAnalysisError(error instanceof Error ? error.message : "Review failed.");
    } finally {
      setAnalysisLoading(false);
    }
  }

  return (
    <div className="grid gap-5 xl:grid-cols-[minmax(0,1.15fr)_minmax(360px,0.85fr)]">
      <section className="rounded-2xl border border-white/10 bg-white/5 p-5 shadow-2xl shadow-black/20 backdrop-blur">
        <div className="flex flex-wrap items-center gap-3">
          {(["analyze", "history", "settings"] as TabKey[]).map((item) => (
            <button
              key={item}
              type="button"
              onClick={() => {
                setTab(item);
                if (item === "history") {
                  void loadHistory();
                }
              }}
              className={`rounded-full px-4 py-2 text-sm font-medium transition ${
                tab === item
                  ? "bg-sky-400 text-slate-950"
                  : "border border-white/10 bg-white/5 text-slate-300 hover:bg-white/10"
              }`}
            >
              {item[0].toUpperCase() + item.slice(1)}
            </button>
          ))}
          <div className="ml-auto rounded-full border border-white/10 bg-emerald-400/10 px-3 py-1 text-xs font-medium text-emerald-200">
            {healthLabel}
          </div>
        </div>

        {tab === "analyze" ? (
          <div className="mt-5 grid gap-4">
            <div className="grid gap-3 sm:grid-cols-3">
              <label className="grid gap-2">
                <span className="text-xs uppercase tracking-wide text-slate-400">Language</span>
                <select
                  value={language}
                  onChange={(event) => setLanguage(event.target.value)}
                  className="rounded-xl border border-white/10 bg-slate-950/70 px-3 py-3 text-sm text-slate-100 outline-none transition focus:border-sky-400"
                >
                  <option value="python">Python</option>
                  <option value="javascript">JavaScript</option>
                  <option value="typescript">TypeScript</option>
                </select>
              </label>
              <label className="grid gap-2 sm:col-span-2">
                <span className="text-xs uppercase tracking-wide text-slate-400">Context</span>
                <input
                  value={context}
                  onChange={(event) => setContext(event.target.value)}
                  placeholder="Coding standards, repo notes, review focus"
                  className="rounded-xl border border-white/10 bg-slate-950/70 px-3 py-3 text-sm text-slate-100 outline-none transition placeholder:text-slate-500 focus:border-sky-400"
                />
              </label>
            </div>

            <label className="grid gap-2">
              <span className="text-xs uppercase tracking-wide text-slate-400">Code</span>
              <textarea
                value={code}
                onChange={(event) => setCode(event.target.value)}
                className="min-h-[420px] rounded-2xl border border-white/10 bg-slate-950/80 px-4 py-4 font-mono text-sm leading-7 text-slate-100 outline-none transition placeholder:text-slate-500 focus:border-sky-400"
                placeholder="Paste code or a diff here"
              />
            </label>

            <div className="flex flex-wrap items-center gap-3">
              <button
                type="button"
                onClick={() => void runAnalysis()}
                disabled={analysisLoading}
                className="rounded-full bg-sky-400 px-5 py-2.5 text-sm font-semibold text-slate-950 transition hover:bg-sky-300 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {analysisLoading ? "Running review..." : "Run review"}
              </button>
              <span className="text-xs text-slate-400">Base URL: {apiBaseUrl}</span>
            </div>

            {analysisError ? (
              <p className="rounded-xl border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
                {analysisError}
              </p>
            ) : null}

            {result ? (
              <div className="rounded-2xl border border-white/10 bg-slate-950/70 p-5">
                <div className="flex flex-wrap items-start gap-4">
                  <div className="min-w-0 flex-1">
                    <p className="text-xs uppercase tracking-wide text-slate-400">Latest result</p>
                    <h2 className="mt-1 text-lg font-semibold text-slate-50">{result.summary}</h2>
                  </div>
                  <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
                    <Metric label="Findings" value={String(result.findings.length)} />
                    <Metric label="Latency" value={`${result.latency_ms} ms`} />
                    <Metric label="Tokens" value={String(result.tokens_used)} />
                    <Metric label="Cost" value={formatMoney(result.cost_usd)} />
                  </div>
                </div>
                <div className="mt-5 grid gap-4">
                  {result.findings.length === 0 ? (
                    <p className="rounded-xl border border-emerald-500/20 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-200">
                      No issues found by the current rules.
                    </p>
                  ) : (
                    result.findings.map((finding, index) => (
                      <FindingRow key={`${finding.title}-${index}`} finding={finding} />
                    ))
                  )}
                </div>
              </div>
            ) : null}
          </div>
        ) : null}

        {tab === "history" ? (
          <div className="mt-5 grid gap-4">
            <div className="flex items-center justify-between gap-3">
              <div>
                <h2 className="text-lg font-semibold text-slate-50">Analysis history</h2>
                <p className="text-sm text-slate-400">Saved runs from the backend database.</p>
              </div>
              <button
                type="button"
                onClick={() => void loadHistory()}
                className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-200 transition hover:bg-white/10"
              >
                Refresh
              </button>
            </div>

            {historyError ? (
              <p className="rounded-xl border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
                {historyError}
              </p>
            ) : null}

            <div className="grid gap-3">
              {historyLoading ? (
                <div className="rounded-xl border border-white/10 bg-white/5 p-4 text-sm text-slate-400">
                  Loading history...
                </div>
              ) : history.length === 0 ? (
                <div className="rounded-xl border border-white/10 bg-white/5 p-4 text-sm text-slate-400">
                  No saved analyses yet.
                </div>
              ) : (
                history.map((item) => (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => void loadAnalysisDetail(item.id)}
                    className={`rounded-2xl border p-4 text-left transition ${
                      selectedId === item.id
                        ? "border-sky-400/40 bg-sky-400/10"
                        : "border-white/10 bg-white/5 hover:bg-white/10"
                    }`}
                  >
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="font-mono text-sm text-slate-50">#{item.id}</span>
                      <span className="rounded-full border border-white/10 px-2 py-1 text-[11px] uppercase tracking-wide text-slate-300">
                        {item.language}
                      </span>
                      <span className="rounded-full border border-white/10 px-2 py-1 text-[11px] uppercase tracking-wide text-slate-300">
                        {item.source_type}
                      </span>
                    </div>
                    <p className="mt-3 text-sm text-slate-100">{item.summary}</p>
                    <div className="mt-3 flex flex-wrap gap-4 text-xs text-slate-400">
                      <span>{formatTimestamp(item.created_at)}</span>
                      <span>{item.latency_ms} ms</span>
                      <span>{formatMoney(item.cost_usd)}</span>
                    </div>
                  </button>
                ))
              )}
            </div>
          </div>
        ) : null}

        {tab === "settings" ? (
          <div className="mt-5 grid gap-4">
            <div>
              <h2 className="text-lg font-semibold text-slate-50">Deployment settings</h2>
              <p className="mt-1 text-sm text-slate-400">
                Vercel routes the frontend to the backend service under <span className="font-mono">/api</span>.
              </p>
            </div>

            <div className="grid gap-3 sm:grid-cols-2">
              <SettingItem label="API base URL" value={apiBaseUrl} />
              <SettingItem label="Health endpoint" value={buildApiUrl("/health")} />
              <SettingItem label="Backend status" value={healthLabel} />
              <SettingItem label="GitHub ingestion" value="POST /webhook/github" />
            </div>

            <div className="rounded-2xl border border-white/10 bg-white/5 p-4 text-sm leading-6 text-slate-300">
              Set <span className="font-mono">NEXT_PUBLIC_API_BASE_URL</span> to a local backend URL
              when developing without Vercel services. In production, the default <span className="font-mono">/api</span> path is used.
            </div>
          </div>
        ) : null}
      </section>

      <aside className="grid gap-5">
        <section className="rounded-2xl border border-white/10 bg-slate-950/80 p-5">
          <p className="text-xs uppercase tracking-[0.3em] text-sky-300">AI code review platform</p>
          <h1 className="mt-3 text-3xl font-semibold leading-tight text-slate-50">
            Fast code review for GitHub PRs and pasted snippets.
          </h1>
          <p className="mt-4 max-w-xl text-sm leading-6 text-slate-300">
            Static analysis catches obvious issues. The backend then layers LLM review on top and stores the result for later inspection.
          </p>
          <div className="mt-5 grid gap-3 sm:grid-cols-2">
            <StatusCard label="Backend" value={healthLabel} tone={healthState} />
            <StatusCard label="Mode" value="Next.js + FastAPI" tone="healthy" />
          </div>
        </section>

        <section className="rounded-2xl border border-white/10 bg-white/5 p-5">
          <div className="flex items-center justify-between gap-3">
            <h2 className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-300">
              Selected analysis
            </h2>
            {selectedAnalysis ? (
              <span className="text-xs text-slate-400">#{selectedAnalysis.analysis_id}</span>
            ) : null}
          </div>

          {selectedAnalysis ? (
            <div className="mt-4 grid gap-4">
              <div className="grid gap-2 text-sm text-slate-300">
                <span>
                  <strong className="text-slate-50">Language:</strong> {selectedAnalysis.language}
                </span>
                <span>
                  <strong className="text-slate-50">Source:</strong> {selectedAnalysis.source_type}
                </span>
                <span>
                  <strong className="text-slate-50">Created:</strong> {formatTimestamp(selectedAnalysis.created_at)}
                </span>
              </div>
              <pre className="max-h-[320px] overflow-auto rounded-xl border border-white/10 bg-slate-950/80 p-4 font-mono text-xs leading-6 text-slate-200">
                {selectedAnalysis.input_code}
              </pre>
              <div className="grid gap-3">
                {selectedAnalysis.findings.map((finding, index) => (
                  <FindingRow key={`${finding.title}-${index}`} finding={finding} />
                ))}
              </div>
            </div>
          ) : (
            <p className="mt-4 text-sm leading-6 text-slate-400">
              Select an analysis from history to inspect the stored code and findings.
            </p>
          )}
        </section>
      </aside>
    </div>
  );
}

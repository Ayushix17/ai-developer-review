export type Finding = {
  severity: string;
  title: string;
  description: string;
  line_number?: number | null;
  suggestion?: string | null;
  category: string;
};

export type AnalyzeResponse = {
  analysis_id: number;
  summary: string;
  findings: Finding[];
  tokens_used: number;
  latency_ms: number;
  cost_usd: number;
};

export type AnalysisListItem = {
  id: number;
  language: string;
  source_type: string;
  summary: string;
  cost_usd: number;
  latency_ms: number;
  created_at: string;
};

export type AnalysisDetail = AnalyzeResponse & {
  language: string;
  source_type: string;
  input_code: string;
  context?: string | null;
  created_at: string;
};

export type ByokProvider = "google" | "cloudflare" | "openrouter";

export interface ByokCredentials {
  api_key?: string;
  account_id?: string;
  api_token?: string;
}

export interface ByokEnvelope {
  enabled: boolean;
  provider: ByokProvider;
  credentials: ByokCredentials;
}

export interface BriefRequest {
  topic: string;
  depth: number;
  user_id: string;
  summary_length: number;
  follow_up: boolean;
  byok?: ByokEnvelope;
}

export interface SourceSummary {
  url: string;
  title: string;
  summary: string;
  key_points: string[];
  relevance_score: number;
  credibility_score: number;
  source_type: string;
}

export interface FinalBrief {
  topic: string;
  depth: number;
  user_id: string;
  follow_up: boolean;
  summary_length?: number;
  executive_summary: string;
  research_questions: string[];
  key_findings: string[];
  detailed_analysis: string;
  sources: SourceSummary[];
  created_at: string;
  processing_time_seconds?: number;
}

export interface StreamMessage {
  type: "log" | "result" | "complete" | "error";
  message?: string;
  data?: FinalBrief;
  success?: boolean;
}

export type AppState = "idle" | "collecting" | "loading" | "result" | "error";

export interface FormData {
  topic: string;
  depth: number;
  summaryLength: number;
  byok: ByokEnvelope;
}

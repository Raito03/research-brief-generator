export interface BriefRequest {
  topic: string;
  depth: number;
  user_id: string;
  summary_length: number;
  follow_up: boolean;
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
  type: 'log' | 'result' | 'complete' | 'error';
  message?: string;
  data?: FinalBrief;
  success?: boolean;
}

export type AppState = 'idle' | 'collecting' | 'loading' | 'result' | 'error';

export interface FormData {
  topic: string;
  depth: number;
  summaryLength: number;
}

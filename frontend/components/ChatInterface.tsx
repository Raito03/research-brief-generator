"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  AppState,
  BriefRequest,
  ByokCredentials,
  ByokEnvelope,
  FinalBrief,
  FormData,
} from "@/types";
import { ParameterCollection } from "./ParameterCollection";
import { LoadingDisplay } from "./LoadingDisplay";
import { ResultDisplay } from "./ResultDisplay";

const DEFAULT_BYOK: ByokEnvelope = {
  enabled: false,
  provider: "google",
  credentials: {},
};

function createDefaultFormData(): FormData {
  return {
    topic: "",
    depth: 3,
    summaryLength: 300,
    byok: DEFAULT_BYOK,
  };
}

function normalizeValue(value?: string): string | undefined {
  const trimmed = value?.trim();
  return trimmed ? trimmed : undefined;
}

function getScopedCredentials(
  byok?: ByokEnvelope,
): ByokCredentials | undefined {
  if (!byok?.enabled) {
    return undefined;
  }

  if (byok.provider === "cloudflare") {
    const account_id = normalizeValue(byok.credentials.account_id);
    const api_token = normalizeValue(byok.credentials.api_token);

    if (!account_id || !api_token) {
      return undefined;
    }

    return { account_id, api_token };
  }

  const api_key = normalizeValue(byok.credentials.api_key);

  if (!api_key) {
    return undefined;
  }

  return { api_key };
}

function getRequestByok(byok?: ByokEnvelope): BriefRequest["byok"] {
  const credentials = getScopedCredentials(byok);

  if (!byok?.enabled || !credentials) {
    return undefined;
  }

  return {
    enabled: true,
    provider: byok.provider,
    credentials,
  };
}

export function ChatInterface() {
  const [appState, setAppState] = useState<AppState>("idle");
  const [formData, setFormData] = useState<FormData>(createDefaultFormData());
  const [logs, setLogs] = useState<string[]>([]);
  const [result, setResult] = useState<FinalBrief | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = () => {
    setAppState("loading");
    setLogs([]);
    setError(null);
    startStreamingRequest();
  };

  const startStreamingRequest = async () => {
    try {
      const { streamResearchBrief } = await import("@/lib/api");
      const byok = getRequestByok(formData.byok);
      const request: BriefRequest = {
        topic: formData.topic,
        depth: formData.depth,
        user_id: `user_${Date.now()}`,
        summary_length: formData.summaryLength,
        follow_up: false,
        ...(byok ? { byok } : {}),
      };

      for await (const message of streamResearchBrief(request)) {
        if (message.type === "log" && typeof message.message === "string") {
          const logMessage = message.message;
          setLogs((prev) => [...prev, logMessage]);
        } else if (message.type === "result" && message.data) {
          setResult(message.data);
        } else if (message.type === "complete") {
          setAppState("result");
        } else if (message.type === "error") {
          setError(message.message || "An error occurred");
          setAppState("error");
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to connect to API");
      setAppState("error");
    }
  };

  const handleReset = () => {
    setAppState("idle");
    setFormData(createDefaultFormData());
    setLogs([]);
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 md:p-8">
      <div className="w-full max-w-4xl">
        <AnimatePresence mode="wait">
          {(appState === "idle" || appState === "collecting") && (
            <motion.div
              key="input"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.4, ease: [0.25, 0.1, 0.25, 1] }}
            >
              <ParameterCollection
                formData={formData}
                setFormData={setFormData}
                onSubmit={handleSubmit}
              />
            </motion.div>
          )}

          {appState === "loading" && (
            <motion.div
              key="loading"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ duration: 0.4, ease: [0.25, 0.1, 0.25, 1] }}
            >
              <LoadingDisplay logs={logs} />
            </motion.div>
          )}

          {appState === "result" && result && (
            <motion.div
              key="result"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, ease: [0.25, 0.1, 0.25, 1] }}
            >
              <ResultDisplay brief={result} onReset={handleReset} />
            </motion.div>
          )}

          {appState === "error" && (
            <motion.div
              key="error"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-center"
            >
              <div className="bg-[#FAF8F5] border border-[#E8E5DD] rounded-2xl p-8">
                <h2 className="text-2xl font-serif font-medium text-[#1A1A1A] mb-4">
                  Something went wrong
                </h2>
                <p className="text-[#6B6B6B] mb-6">{error}</p>
                <button
                  type="button"
                  onClick={handleReset}
                  className="px-6 py-3 bg-[#D4A853] text-white rounded-lg font-medium hover:bg-[#B8923D] transition-colors"
                >
                  Try Again
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

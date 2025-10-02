'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AppState, FormData, FinalBrief } from '@/types';
import { ParameterCollection } from './ParameterCollection';
import { LoadingDisplay } from './LoadingDisplay';
import { ResultDisplay } from './ResultDisplay';

export function ChatInterface() {
  const [appState, setAppState] = useState<AppState>('idle');
  const [formData, setFormData] = useState<FormData>({
    topic: '',
    depth: 3,
    summaryLength: 300,
  });
  const [logs, setLogs] = useState<string[]>([]);
  const [result, setResult] = useState<FinalBrief | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = () => {
    setAppState('loading');
    setLogs([]);
    setError(null);
    startStreamingRequest();
  };

  const startStreamingRequest = async () => {
    try {
      const { streamResearchBrief } = await import('@/lib/api');

      const request = {
        topic: formData.topic,
        depth: formData.depth,
        user_id: `user_${Date.now()}`,
        summary_length: formData.summaryLength,
        follow_up: false,
      };

      for await (const message of streamResearchBrief(request)) {
        if (message.type === 'log' && message.message) {
          setLogs((prev) => [...prev, message.message!]);
        } else if (message.type === 'result' && message.data) {
          setResult(message.data);
        } else if (message.type === 'complete') {
          setAppState('result');
        } else if (message.type === 'error') {
          setError(message.message || 'An error occurred');
          setAppState('error');
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to connect to API');
      setAppState('error');
    }
  };

  const handleReset = () => {
    setAppState('idle');
    setFormData({
      topic: '',
      depth: 3,
      summaryLength: 300,
    });
    setLogs([]);
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 md:p-8">
      <div className="w-full max-w-4xl">
        <AnimatePresence mode="wait">
          {(appState === 'idle' || appState === 'collecting') && (
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

          {appState === 'loading' && (
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

          {appState === 'result' && result && (
            <motion.div
              key="result"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, ease: [0.25, 0.1, 0.25, 1] }}
            >
              <ResultDisplay brief={result} onReset={handleReset} />
            </motion.div>
          )}

          {appState === 'error' && (
            <motion.div
              key="error"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-center"
            >
              <div className="bg-american-blue/20 border border-ube/30 rounded-2xl p-8">
                <h2 className="text-2xl font-semibold text-ube mb-4">
                  Something went wrong
                </h2>
                <p className="text-cadet-grey mb-6">{error}</p>
                <button
                  onClick={handleReset}
                  className="px-6 py-3 bg-ube text-chinese-black rounded-xl font-medium hover:bg-ube/90 transition-colors"
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

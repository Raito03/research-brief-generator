'use client';

import { useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface Props {
  logs: string[];
}

export function LoadingDisplay({ logs }: Props) {
  const logsEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  return (
    <div className="space-y-8">
      <div className="flex flex-col items-center justify-center py-12">
        <motion.div
          className="relative w-24 h-24 mb-8"
          animate={{
            rotate: 360,
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: 'linear',
          }}
        >
          <motion.div
            className="absolute inset-0 rounded-full border-4 border-ube/20"
            animate={{
              scale: [1, 1.1, 1],
              opacity: [0.5, 1, 0.5],
            }}
            transition={{
              duration: 1.5,
              repeat: Infinity,
              ease: 'easeInOut',
            }}
          />
          <motion.div
            className="absolute inset-0 rounded-full border-4 border-transparent border-t-ube"
            style={{ borderTopWidth: 4 }}
          />
        </motion.div>

        <motion.h2
          className="text-2xl font-semibold text-cadet-grey mb-2"
          animate={{ opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          Researching...
        </motion.h2>
        <p className="text-cool-grey">
          Gathering insights from multiple sources
        </p>
      </div>

      <div className="bg-american-blue/10 backdrop-blur-sm border border-ube/20 rounded-2xl p-6 max-h-96 overflow-y-auto">
        <div className="space-y-2">
          <AnimatePresence mode="popLayout">
            {logs.slice(-10).map((log, index) => {
              const actualIndex = logs.length - 10 + index;
              const isLatest = actualIndex === logs.length - 1;

              return (
                <motion.div
                  key={actualIndex}
                  initial={{ opacity: 0, y: 10, x: -10 }}
                  animate={{
                    opacity: isLatest ? 1 : 0.6,
                    y: 0,
                    x: 0,
                    scale: isLatest ? 1 : 0.98,
                  }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{
                    duration: 0.3,
                    ease: [0.25, 0.1, 0.25, 1],
                  }}
                  className={`px-4 py-3 rounded-lg transition-all ${
                    isLatest
                      ? 'bg-ube/20 border border-ube/40'
                      : 'bg-american-blue/20'
                  }`}
                >
                  <p
                    className={`text-sm font-mono ${
                      isLatest ? 'text-cadet-grey' : 'text-cool-grey/70'
                    }`}
                  >
                    {log}
                  </p>
                </motion.div>
              );
            })}
          </AnimatePresence>
          <div ref={logsEndRef} />
        </div>

        {logs.length === 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-8"
          >
            <p className="text-cool-grey">Initializing research workflow...</p>
          </motion.div>
        )}
      </div>

      {logs.length > 10 && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center text-cool-grey/60 text-sm"
        >
          Showing latest 10 of {logs.length} messages
        </motion.p>
      )}
    </div>
  );
}

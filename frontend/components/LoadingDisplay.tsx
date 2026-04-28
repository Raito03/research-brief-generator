'use client';

import { motion, AnimatePresence } from 'framer-motion';

interface Props {
  logs: string[];
}

export function LoadingDisplay({ logs }: Props) {
  const latestLog = logs.length > 0 ? logs[logs.length - 1] : 'Initializing research workflow...';

  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center p-8">
      <div className="max-w-2xl w-full text-center space-y-12">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-4"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-cadet-grey font-serif tracking-tight">
            Synthesizing Research
          </h2>
          <p className="text-cool-grey font-sans text-lg">
            Extracting and analyzing sources
          </p>
        </motion.div>

        <div className="h-24 flex items-center justify-center">
          <AnimatePresence mode="wait">
            <motion.div
              key={latestLog}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.4, ease: "easeInOut" }}
              className="text-ube font-serif text-xl md:text-2xl italic"
            >
              {latestLog}
            </motion.div>
          </AnimatePresence>
        </div>
        
        <motion.div 
          className="w-full max-w-xs mx-auto h-px bg-gradient-to-r from-transparent via-ube/30 to-transparent"
          animate={{ opacity: [0.3, 0.7, 0.3] }}
          transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
        />
      </div>
    </div>
  );
}

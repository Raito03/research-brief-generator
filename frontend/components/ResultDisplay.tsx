'use client';

import { motion } from 'framer-motion';
import { FinalBrief } from '@/types';

interface Props {
  brief: FinalBrief;
  onReset: () => void;
}

export function ResultDisplay({ brief, onReset }: Props) {
  return (
    <div className="max-w-3xl mx-auto py-16 px-6 md:px-8 font-serif">
      <motion.header 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: [0.25, 0.1, 0.25, 1] }}
        className="mb-20 border-b border-[#E8E5DD] pb-12"
      >
        <h1 className="text-4xl md:text-6xl font-medium text-[#1A1A1A] mb-6 leading-tight tracking-tight">
          {brief.topic}
        </h1>
        <div className="flex flex-col sm:flex-row sm:items-center gap-4 text-[#6B6B6B] font-sans text-sm tracking-widest uppercase">
          <span>Research Brief</span>
          <span className="hidden sm:inline text-[#D4A853]">•</span>
          <span>{new Date(brief.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}</span>
          <span className="hidden sm:inline text-[#D4A853]">•</span>
          <span>{brief.processing_time_seconds?.toFixed(1)}s</span>
        </div>
      </motion.header>

      <motion.section 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1, ease: [0.25, 0.1, 0.25, 1] }}
        className="mb-20"
      >
        <h2 className="text-2xl font-medium text-[#1A1A1A] mb-8 font-sans uppercase tracking-widest text-sm">Executive Summary</h2>
        <p className="text-xl md:text-2xl leading-relaxed text-[#1A1A1A]/90 font-serif">
          {brief.executive_summary}
        </p>
      </motion.section>

      <motion.section 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2, ease: [0.25, 0.1, 0.25, 1] }}
        className="mb-20"
      >
        <h2 className="text-2xl font-medium text-[#1A1A1A] mb-8 font-sans uppercase tracking-widest text-sm">Key Findings</h2>
        <ul className="space-y-6 list-none p-0">
          {brief.key_findings.map((finding, idx) => (
            <li key={`finding-${idx}`} className="flex gap-6 text-lg md:text-xl leading-relaxed text-[#1A1A1A]/90">
              <span className="text-[#D4A853] font-medium select-none">—</span>
              <span>{finding}</span>
            </li>
          ))}
        </ul>
      </motion.section>

      <motion.section 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.3, ease: [0.25, 0.1, 0.25, 1] }}
        className="mb-20"
      >
        <h2 className="text-2xl font-medium text-[#1A1A1A] mb-8 font-sans uppercase tracking-widest text-sm">Detailed Analysis</h2>
        <div className="text-lg md:text-xl leading-relaxed text-[#1A1A1A]/90 whitespace-pre-wrap font-serif space-y-6">
          {brief.detailed_analysis}
        </div>
      </motion.section>

      {brief.research_questions && brief.research_questions.length > 0 && (
        <motion.section 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4, ease: [0.25, 0.1, 0.25, 1] }}
          className="mb-20"
        >
          <h2 className="text-2xl font-medium text-[#1A1A1A] mb-8 font-sans uppercase tracking-widest text-sm">Research Questions</h2>
          <ul className="space-y-6 list-none p-0">
            {brief.research_questions.map((question, idx) => (
              <li key={`question-${idx}`} className="flex gap-6 text-lg md:text-xl leading-relaxed text-[#1A1A1A]/90">
                <span className="text-[#D4A853] font-medium select-none">?</span>
                <span className="italic">{question}</span>
              </li>
            ))}
          </ul>
        </motion.section>
      )}

      {brief.sources && brief.sources.length > 0 && (
        <motion.section 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.5, ease: [0.25, 0.1, 0.25, 1] }}
          className="mb-20"
        >
          <h2 className="text-2xl font-medium text-[#1A1A1A] mb-8 font-sans uppercase tracking-widest text-sm">Sources</h2>
          <div className="space-y-12">
            {brief.sources.map((source, idx) => (
              <div key={`source-${idx}`} className="group">
                <a
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xl md:text-2xl text-[#2D7D8A] hover:text-[#1A1A1A] font-medium mb-3 block transition-colors"
                >
                  {source.title}
                </a>
                <p className="text-[#6B6B6B] text-base md:text-lg mb-4 font-sans leading-relaxed">
                  {source.summary}
                </p>
                <div className="flex flex-wrap gap-6 text-xs font-sans tracking-widest uppercase text-[#6B6B6B]/60">
                  <span>Relevance: {(source.relevance_score * 100).toFixed(0)}%</span>
                  <span>Credibility: {(source.credibility_score * 100).toFixed(0)}%</span>
                  <span>Type: {source.source_type}</span>
                </div>
              </div>
            ))}
          </div>
        </motion.section>
      )}

      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.6 }}
        className="mt-32 pt-12 border-t border-[#E8E5DD] text-center"
      >
        <button
          type="button"
          onClick={onReset}
          className="font-sans text-sm font-medium tracking-widest uppercase text-[#2D7D8A] hover:text-[#1A1A1A] transition-colors py-4 px-8"
        >
          ← Start New Research
        </button>
      </motion.div>
    </div>
  );
}

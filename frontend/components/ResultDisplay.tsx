'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { FinalBrief } from '@/types';

interface Props {
  brief: FinalBrief;
  onReset: () => void;
}

type Section = 'executive' | 'detailed' | 'findings' | 'questions' | 'sources';

export function ResultDisplay({ brief, onReset }: Props) {
  const [expandedSection, setExpandedSection] = useState<Section>('executive');

  const toggleSection = (section: Section) => {
    setExpandedSection(expandedSection === section ? 'executive' : section);
  };

  const sections = [
    {
      id: 'executive' as Section,
      title: 'Executive Summary',
      content: brief.executive_summary,
    },
    {
      id: 'detailed' as Section,
      title: 'Detailed Analysis',
      content: brief.detailed_analysis,
    },
    {
      id: 'findings' as Section,
      title: 'Key Findings',
      items: brief.key_findings,
    },
    {
      id: 'questions' as Section,
      title: 'Research Questions',
      items: brief.research_questions,
    },
    {
      id: 'sources' as Section,
      title: 'Sources',
      sources: brief.sources,
    },
  ];

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between mb-8"
      >
        <div>
          <h1 className="text-3xl md:text-4xl font-bold text-cadet-grey mb-2">
            {brief.topic}
          </h1>
          <p className="text-cool-grey">
            Research completed in {brief.processing_time_seconds?.toFixed(1)}s
          </p>
        </div>
        <motion.button
          onClick={onReset}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="px-6 py-3 bg-american-blue text-cadet-grey rounded-xl font-medium hover:bg-american-blue/80 transition-colors"
        >
          New Search
        </motion.button>
      </motion.div>

      <div className="space-y-4">
        {sections.map((section, index) => (
          <motion.div
            key={section.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-american-blue/10 backdrop-blur-sm border border-ube/20 rounded-2xl overflow-hidden"
          >
            <button
              onClick={() => toggleSection(section.id)}
              className="w-full px-6 py-4 flex items-center justify-between hover:bg-ube/5 transition-colors"
            >
              <h2 className="text-xl font-semibold text-cadet-grey">
                {section.title}
              </h2>
              <motion.div
                animate={{ rotate: expandedSection === section.id ? 180 : 0 }}
                transition={{ duration: 0.3 }}
                className="text-ube text-2xl"
              >
                ↓
              </motion.div>
            </button>

            <motion.div
              initial={false}
              animate={{
                height: expandedSection === section.id ? 'auto' : 0,
                opacity: expandedSection === section.id ? 1 : 0,
              }}
              transition={{ duration: 0.3, ease: [0.25, 0.1, 0.25, 1] }}
              className="overflow-hidden"
            >
              <div className="px-6 pb-6">
                {section.content && (
                  <motion.p
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.1 }}
                    className="text-cadet-grey leading-relaxed whitespace-pre-wrap"
                  >
                    {section.content}
                  </motion.p>
                )}

                {section.items && (
                  <motion.ul
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.1 }}
                    className="space-y-3"
                  >
                    {section.items.map((item, i) => (
                      <motion.li
                        key={i}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.1 + i * 0.05 }}
                        className="flex items-start gap-3"
                      >
                        <span className="text-ube mt-1 flex-shrink-0">•</span>
                        <span className="text-cadet-grey">{item}</span>
                      </motion.li>
                    ))}
                  </motion.ul>
                )}

                {section.sources && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.1 }}
                    className="space-y-4"
                  >
                    {section.sources.map((source, i) => (
                      <motion.div
                        key={i}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.1 + i * 0.05 }}
                        className="bg-chinese-black/40 border border-ube/10 rounded-xl p-4"
                      >
                        <a
                          href={source.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-ube hover:text-ube/80 font-medium mb-2 block"
                        >
                          {source.title}
                        </a>
                        <p className="text-cool-grey text-sm mb-3">
                          {source.summary}
                        </p>
                        <div className="flex flex-wrap gap-4 text-xs">
                          <span className="text-cool-grey">
                            Relevance:{' '}
                            <span className="text-cadet-grey">
                              {(source.relevance_score * 100).toFixed(0)}%
                            </span>
                          </span>
                          <span className="text-cool-grey">
                            Credibility:{' '}
                            <span className="text-cadet-grey">
                              {(source.credibility_score * 100).toFixed(0)}%
                            </span>
                          </span>
                          <span className="text-cool-grey">
                            Type:{' '}
                            <span className="text-cadet-grey capitalize">
                              {source.source_type}
                            </span>
                          </span>
                        </div>
                        {source.key_points.length > 0 && (
                          <div className="mt-3 pt-3 border-t border-ube/10">
                            <p className="text-cool-grey text-xs mb-2">
                              Key Points:
                            </p>
                            <ul className="space-y-1">
                              {source.key_points.map((point, j) => (
                                <li
                                  key={j}
                                  className="text-cadet-grey text-xs flex items-start gap-2"
                                >
                                  <span className="text-ube">→</span>
                                  <span>{point}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </motion.div>
                    ))}
                  </motion.div>
                )}
              </div>
            </motion.div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

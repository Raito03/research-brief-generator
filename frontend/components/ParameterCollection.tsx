'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FormData } from '@/types';

interface Props {
  formData: FormData;
  setFormData: (data: FormData) => void;
  onSubmit: () => void;
}

type Step = 'topic' | 'depth' | 'length' | 'confirm';

export function ParameterCollection({ formData, setFormData, onSubmit }: Props) {
  const [currentStep, setCurrentStep] = useState<Step>('topic');
  const [topicInput, setTopicInput] = useState(formData.topic);

  const handleTopicSubmit = () => {
    if (topicInput.trim().length >= 5) {
      setFormData({ ...formData, topic: topicInput.trim() });
      setCurrentStep('depth');
    }
  };

  const handleDepthSelect = (depth: number) => {
    setFormData({ ...formData, depth });
    setCurrentStep('length');
  };

  const handleLengthSelect = (length: number) => {
    setFormData({ ...formData, summaryLength: length });
    setCurrentStep('confirm');
  };

  const handleBack = () => {
    if (currentStep === 'depth') setCurrentStep('topic');
    else if (currentStep === 'length') setCurrentStep('depth');
    else if (currentStep === 'confirm') setCurrentStep('length');
  };

  const depthOptions = [
    { value: 1, label: 'Quick', desc: 'Basic overview (2-3 sources)' },
    { value: 2, label: 'Light', desc: 'Standard research (3-4 sources)' },
    { value: 3, label: 'Balanced', desc: 'Comprehensive (4-6 sources)' },
    { value: 4, label: 'Detailed', desc: 'In-depth analysis (6-8 sources)' },
    { value: 5, label: 'Thorough', desc: 'Exhaustive (8-10 sources)' },
  ];

  const lengthOptions = [
    { value: 100, label: 'Brief', desc: '~100 words' },
    { value: 300, label: 'Standard', desc: '~300 words' },
    { value: 600, label: 'Extended', desc: '~600 words' },
    { value: 1000, label: 'Comprehensive', desc: '~1000 words' },
  ];

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-8 gap-8">
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-6"
      >
        <h1 className="text-5xl md:text-6xl font-bold text-cadet-grey mb-4 font-serif tracking-tight">
          Research Assistant
        </h1>
        <p className="text-cool-grey text-lg font-sans">
          Deep content extraction and editorial synthesis.
        </p>
      </motion.div>

      <div className="w-full max-w-2xl">
        <AnimatePresence mode="wait">
        {currentStep === 'topic' && (
          <motion.div
            key="topic"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
            className="space-y-6"
          >
            <h2 className="text-2xl font-semibold text-cadet-grey text-center mb-6 font-serif">
              What would you like to research?
            </h2>

            <div className="gap-4">
              <input
                type="text"
                value={topicInput}
                onChange={(e) => setTopicInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleTopicSubmit()}
                placeholder="e.g., Artificial Intelligence"
                className="focus:outline-none focus:ring-0 focus:border-transparent focus:ring-0 w-full bg-transparent border-b-2 border-ube/30 px-2 py-4 text-cadet-grey placeholder-cool-grey/50 transition-all text-center text-2xl font-serif"
                autoFocus
              />
              
              <p className="text-sm text-cool-grey/60 text-center mt-4 font-sans">
                {topicInput.length}/200 characters (min 5)
              </p>
            </div>

            <div className="flex justify-center pt-8">
              <motion.button
                type="button"
                onClick={handleTopicSubmit}
                disabled={topicInput.trim().length < 5}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="w-40 mx-auto block bg-ube text-chinese-black font-semibold py-3 rounded-none disabled:opacity-40 disabled:cursor-not-allowed transition-all hover:bg-ube/90 font-sans tracking-wide uppercase text-sm"
              >
                Continue
              </motion.button>
            </div>
          </motion.div>
        )}

          {currentStep === 'depth' && (
            <motion.div
              key="depth"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className="space-y-6"
            >
              <button
                type="button"
                onClick={handleBack}
                className="text-ube hover:text-ube/80 transition-colors text-sm font-medium font-sans uppercase tracking-wider"
              >
                ← Back
              </button>

              <div className="text-center">
                <h2 className="text-cadet-grey text-2xl mb-8 font-serif">
                  How deep should the research be?
                </h2>

                <div className="grid gap-4">
                  {depthOptions.map((option) => (
                    <motion.button
                      type="button"
                      key={option.value}
                      onClick={() => handleDepthSelect(option.value)}
                      whileHover={{ x: 4 }}
                      whileTap={{ scale: 0.98 }}
                      className={`w-full text-left px-6 py-4 transition-all border-l-4 ${
                        formData.depth === option.value
                          ? 'border-ube bg-ube/5'
                          : 'border-transparent hover:border-ube/40 hover:bg-ube/5'
                      }`}
                    >
                       <div className="flex items-center justify-between gap-3">
                        <div className="min-w-0 space-y-1 pr-2">
                          <div className="font-semibold text-cadet-grey text-xl font-serif">
                            {option.label}
                          </div>
                          <div className="text-cool-grey/80 text-sm font-sans">
                            {option.desc}
                          </div>
                        </div>
                        <div className="shrink-0 text-ube font-bold text-2xl font-serif">
                          {option.value}
                        </div>
                      </div>
                    </motion.button>
                  ))}
                </div>
              </div>
            </motion.div>
          )}

          {currentStep === 'length' && (
            <motion.div
              key="length"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className="space-y-6"
            >
              <button
                type="button"
                onClick={handleBack}
                className="text-ube hover:text-ube/80 transition-colors text-sm font-medium font-sans uppercase tracking-wider mb-4"
              >
                ← Back
              </button>

              <div className="text-center">
                <h2 className="text-cadet-grey text-2xl mb-8 font-serif">
                  Preferred summary length?
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {lengthOptions.map((option) => (
                    <motion.button
                      type="button"
                      key={option.value}
                      onClick={() => handleLengthSelect(option.value)}
                      whileHover={{ y: -2 }}
                      whileTap={{ scale: 0.98 }}
                      className={`p-6 text-left transition-all border-l-4 ${
                        formData.summaryLength === option.value
                          ? 'border-ube bg-ube/5'
                          : 'border-transparent hover:border-ube/40 hover:bg-ube/5'
                      }`}
                    >
                      <div className="text-cadet-grey font-semibold mb-2 text-xl font-serif">
                        {option.label}
                      </div>
                      <div className="text-cool-grey text-sm font-sans">{option.desc}</div>
                    </motion.button>
                  ))}
                </div>
              </div>
            </motion.div>
          )}

          {currentStep === 'confirm' && (
            <motion.div
              key="confirm"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className="space-y-6"
            >
              <button
                type="button"
                onClick={handleBack}
                className="text-ube hover:text-ube/80 transition-colors text-sm font-medium font-sans uppercase tracking-wider mb-4"
              >
                ← Back
              </button>

              <div className="text-center">
                <h2 className="text-cadet-grey text-2xl mb-8 font-serif">
                  Ready to generate your research brief
                </h2>

                <div className="space-y-4 mb-12 text-left max-w-md mx-auto">
                  <div className="flex justify-between items-center py-4 border-b border-ube/20">
                    <span className="text-cool-grey font-sans">Topic</span>
                    <span className="text-cadet-grey font-medium font-serif text-lg">
                      {formData.topic}
                    </span>
                  </div>
                  <div className="flex justify-between items-center py-4 border-b border-ube/20">
                    <span className="text-cool-grey font-sans">Research Depth</span>
                    <span className="text-cadet-grey font-medium font-serif text-lg">
                      Level {formData.depth}
                    </span>
                  </div>
                  <div className="flex justify-between items-center py-4 border-b border-ube/20">
                    <span className="text-cool-grey font-sans">Summary Length</span>
                    <span className="text-cadet-grey font-medium font-serif text-lg">
                      ~{formData.summaryLength} words
                    </span>
                  </div>
                </div>

                <motion.button
                  type="button"
                  onClick={onSubmit}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full max-w-md mx-auto block bg-ube text-chinese-black font-semibold py-4 rounded-none transition-all hover:bg-ube/90 font-sans tracking-wide uppercase text-sm"
                >
                  Generate Research Brief
                </motion.button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

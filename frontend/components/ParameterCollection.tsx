'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FormData } from '@/types';
import { TypeAnimation } from 'react-type-animation';

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
    <div className="min-h-screen flex flex-col items-center justify-center p-8 gap-5">
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-3"
      >
        <h1 className="text-4xl md:text-5xl font-bold text-cadet-grey mb-4">
          <TypeAnimation
            sequence={[
              'Welcome to Lyra', 1000, 'Your AI Research Assistant', 2000
            ]}
            wrapper="span"
            cursor={true}
            repeat={Infinity}
            style={{ display: 'inline-block' }}
          />
          
        </h1>
        <p className="text-cool-grey text-lg">
          Get comprehensive insights in seconds
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
            className="space-y-3"
          >
            {/* Question */}
            <h2 className="text-2xl font-semibold text-cadet-grey text-center mb-4">
              What would you like to research?
            </h2>

            {/* Input Field */}
            <div className="gap-4">
              <input
                type="text"
                value={topicInput}
                onChange={(e) => setTopicInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleTopicSubmit()}
                placeholder="e.g., Artificial Intelligence"
                className="focus:outline-none focus:ring-0 focus:border-transparent focus:ring-0 w-full bg-chinese-black/50 border border-ube/30 rounded-full px-2 py-2 text-cadet-grey placeholder-cool-grey/50 transition-all text-center text-lg"
                autoFocus
              />
              
              {/* Character Counter */}
              <p className="text-sm text-cool-grey/60 text-center">
                {topicInput.length}/200 characters (min 5)
              </p>
            </div>

            {/* Continue Button */}
            <div className="flex justify-center pt-4">
              <motion.button
                onClick={handleTopicSubmit}
                disabled={topicInput.trim().length < 5}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="w-32 mx-auto block bg-ube text-chinese-black font-semibold py-2 rounded-xl disabled:opacity-40 disabled:cursor-not-allowed transition-all hover:bg-ube/90"
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
              className="space-y-2"
            >
              {/* Back Button */}
              <button
                onClick={handleBack}
                className="text-ube hover:text-ube/80 transition-colors text-sm font-medium"
              >
                ← Back
              </button>

              <div className="gap-3 text-center bg-american-blue/10 backdrop-blur-sm border border-ube/20 rounded-2xl p-2">
                <h2 className="text-cadet-grey text-xl mb-2">
                  How deep should the research be?
                </h2>

                <div className="grid gap-2">
                  {depthOptions.map((option) => (
                    <motion.button
                      key={option.value}
                      onClick={() => handleDepthSelect(option.value)}
                      whileHover={{ scale: 1.02, x: 4 }}
                      whileTap={{ scale: 0.98 }}
                      className={`w-full text-left px-3 py-3 rounded-xl border-2 transition-all ${
                        formData.depth === option.value
                          ? 'bg-ube/20 border-ube'
                          : 'bg-american-blue/20 border-ube/20 hover:border-ube/40'
                      }`}
                    >
                       <div className="flex items-center justify-between gap-3 px-3 py-3">
                        <div className="min-w-0 space-y-1 pr-2">
                          <div className="font-semibold text-cadet-grey text-lg">
                            {option.label}
                          </div>
                          <div className="text-cool-grey/60 text-sm">
                            {option.desc}
                          </div>
                        </div>
                        <div className="shrink-0 text-ube font-bold text-2xl">
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
                onClick={handleBack}
                className="text-cool-grey hover:text-ube transition-colors mb-4"
              >
                ← Back
              </button>

              <div className="bg-american-blue/10 backdrop-blur-sm border border-ube/20 rounded-2xl p-3">
                <h2 className="text-cadet-grey text-xl mb-3">
                  Preferred summary length?
                </h2>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {lengthOptions.map((option) => (
                    <motion.button
                      key={option.value}
                      onClick={() => handleLengthSelect(option.value)}
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      className={`p-3 rounded-xl border transition-all ${
                        formData.summaryLength === option.value
                          ? 'bg-ube/20 border-ube'
                          : 'bg-american-blue/20 border-ube/20 hover:border-ube/40'
                      }`}
                    >
                      <div className="text-cadet-grey font-semibold mb-1">
                        {option.label}
                      </div>
                      <div className="text-cool-grey text-sm">{option.desc}</div>
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
              className="space-y-3"
            >
              <button
                onClick={handleBack}
                className="text-cool-grey hover:text-ube transition-colors mb-4"
              >
                ← Back
              </button>

              <div className="bg-american-blue/10 backdrop-blur-sm border border-ube/20 rounded-2xl p-8">
                <h2 className="text-cadet-grey text-xl mb-3">
                  Ready to generate your research brief
                </h2>

                <div className="space-y-2 mb-8">
                  <div className="flex justify-between items-center py-3 border-b border-ube/20">
                    <span className="text-cool-grey">Topic</span>
                    <span className="text-cadet-grey font-medium">
                      {formData.topic}
                    </span>
                  </div>
                  <div className="flex justify-between items-center py-3 border-b border-ube/20">
                    <span className="text-cool-grey">Research Depth</span>
                    <span className="text-cadet-grey font-medium">
                      Level {formData.depth}
                    </span>
                  </div>
                  <div className="flex justify-between items-center py-3">
                    <span className="text-cool-grey">Summary Length</span>
                    <span className="text-cadet-grey font-medium">
                      ~{formData.summaryLength} words
                    </span>
                  </div>
                </div>

                <motion.button
                  onClick={onSubmit}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full bg-ube text-chinese-black font-semibold py-4 rounded-xl transition-all hover:bg-ube/90"
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

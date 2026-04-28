"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ByokEnvelope, FormData } from "@/types";

interface Props {
  formData: FormData;
  setFormData: (data: FormData) => void;
  onSubmit: () => void;
}

type Step = "topic" | "depth" | "length" | "confirm";

const DEFAULT_BYOK: ByokEnvelope = {
  enabled: false,
  provider: "google",
  credentials: {},
};

function hasByokCredentials(byok: ByokEnvelope): boolean {
  if (!byok.enabled) {
    return true;
  }

  if (byok.provider === "cloudflare") {
    return Boolean(
      byok.credentials.account_id?.trim() && byok.credentials.api_token?.trim(),
    );
  }

  return Boolean(byok.credentials.api_key?.trim());
}

export function ParameterCollection({
  formData,
  setFormData,
  onSubmit,
}: Props) {
  const [currentStep, setCurrentStep] = useState<Step>("topic");
  const [topicInput, setTopicInput] = useState(formData.topic);
  const [showAdvancedOptions, setShowAdvancedOptions] = useState(
    Boolean(formData.byok?.enabled),
  );

  const byok = formData.byok ?? DEFAULT_BYOK;
  const isByokValid = hasByokCredentials(byok);

  const handleTopicSubmit = () => {
    if (topicInput.trim().length >= 5) {
      setFormData({ ...formData, topic: topicInput.trim(), byok });
      setCurrentStep("depth");
    }
  };

  const handleDepthSelect = (depth: number) => {
    setFormData({ ...formData, depth, byok });
    setCurrentStep("length");
  };

  const handleLengthSelect = (length: number) => {
    setFormData({ ...formData, summaryLength: length, byok });
    setCurrentStep("confirm");
  };

  const handleBack = () => {
    if (currentStep === "depth") setCurrentStep("topic");
    else if (currentStep === "length") setCurrentStep("depth");
    else if (currentStep === "confirm") setCurrentStep("length");
  };

  const updateByok = (nextByok: ByokEnvelope) => {
    setFormData({ ...formData, byok: nextByok });
  };

  const handleByokEnabledChange = (enabled: boolean) => {
    updateByok({
      ...byok,
      enabled,
    });
  };

  const handleProviderChange = (provider: ByokEnvelope["provider"]) => {
    updateByok({
      enabled: byok.enabled,
      provider,
      credentials: {},
    });
  };

  const handleCredentialChange = (
    field: "api_key" | "account_id" | "api_token",
    value: string,
  ) => {
    updateByok({
      ...byok,
      credentials: {
        ...byok.credentials,
        [field]: value,
      },
    });
  };

  const depthOptions = [
    { value: 1, label: "Quick", desc: "Basic overview (2-3 sources)" },
    { value: 2, label: "Light", desc: "Standard research (3-4 sources)" },
    { value: 3, label: "Balanced", desc: "Comprehensive (4-6 sources)" },
    { value: 4, label: "Detailed", desc: "In-depth analysis (6-8 sources)" },
    { value: 5, label: "Thorough", desc: "Exhaustive (8-10 sources)" },
  ];

  const lengthOptions = [
    { value: 100, label: "Brief", desc: "~100 words" },
    { value: 300, label: "Standard", desc: "~300 words" },
    { value: 600, label: "Extended", desc: "~600 words" },
    { value: 1000, label: "Comprehensive", desc: "~1000 words" },
  ];

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-8 gap-8">
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-6"
      >
        <h1 className="text-5xl md:text-6xl font-bold text-[#1A1A1A] mb-4 font-serif tracking-tight">
          Research Assistant
        </h1>
        <p className="text-[#6B6B6B] text-lg font-sans">
          Deep content extraction and editorial synthesis.
        </p>
      </motion.div>

      <div className="w-full max-w-2xl">
        <AnimatePresence mode="wait">
          {currentStep === "topic" && (
            <motion.div
              key="topic"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className="space-y-6"
            >
              <h2 className="text-2xl font-medium text-[#1A1A1A] text-center mb-6 font-serif">
                What would you like to research?
              </h2>

              <div className="gap-4">
                <input
                  type="text"
                  value={topicInput}
                  onChange={(e) => setTopicInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleTopicSubmit()}
                  placeholder="e.g., Artificial Intelligence"
                  className="focus:outline-none focus:ring-0 focus:border-transparent focus:ring-0 w-full bg-transparent border-b-2 border-[#E8E5DD] px-2 py-4 text-[#1A1A1A] placeholder-[#9A9A9A]/50 transition-all text-center text-2xl font-serif"
                  autoFocus
                />

                <p className="text-sm text-[#9A9A9A] text-center mt-4 font-sans">
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
                  className="w-40 mx-auto block bg-[#D4A853] text-white font-medium py-3 rounded-none disabled:opacity-40 disabled:cursor-not-allowed transition-all hover:bg-[#B8923D] font-sans tracking-wide uppercase text-sm"
                >
                  Continue
                </motion.button>
              </div>
            </motion.div>
          )}

          {currentStep === "depth" && (
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
                className="text-[#2D7D8A] hover:text-[#2D7D8A]/80 transition-colors text-sm font-medium font-sans uppercase tracking-wider"
              >
                ← Back
              </button>

              <div className="text-center">
                <h2 className="text-[#1A1A1A] text-2xl mb-8 font-serif">
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
                          ? "border-[#D4A853] bg-[#D4A853]/5"
                          : "border-transparent hover:border-[#D4A853]/40 hover:bg-[#D4A853]/5"
                      }`}
                    >
                      <div className="flex items-center justify-between gap-3">
                        <div className="min-w-0 space-y-1 pr-2">
                          <div className="font-medium text-[#1A1A1A] text-xl font-serif">
                            {option.label}
                          </div>
                          <div className="text-[#6B6B6B]/80 text-sm font-sans">
                            {option.desc}
                          </div>
                        </div>
                        <div className="shrink-0 text-[#D4A853] font-medium text-2xl font-serif">
                          {option.value}
                        </div>
                      </div>
                    </motion.button>
                  ))}
                </div>
              </div>
            </motion.div>
          )}

          {currentStep === "length" && (
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
                className="text-[#2D7D8A] hover:text-[#2D7D8A]/80 transition-colors text-sm font-medium font-sans uppercase tracking-wider mb-4"
              >
                ← Back
              </button>

              <div className="text-center">
                <h2 className="text-[#1A1A1A] text-2xl mb-8 font-serif">
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
                          ? "border-[#D4A853] bg-[#D4A853]/5"
                          : "border-transparent hover:border-[#D4A853]/40 hover:bg-[#D4A853]/5"
                      }`}
                    >
                      <div className="text-[#1A1A1A] font-medium mb-2 text-xl font-serif">
                        {option.label}
                      </div>
                      <div className="text-[#6B6B6B] text-sm font-sans">
                        {option.desc}
                      </div>
                    </motion.button>
                  ))}
                </div>
              </div>
            </motion.div>
          )}

          {currentStep === "confirm" && (
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
                className="text-[#2D7D8A] hover:text-[#2D7D8A]/80 transition-colors text-sm font-medium font-sans uppercase tracking-wider mb-4"
              >
                ← Back
              </button>

              <div className="text-center">
                <h2 className="text-[#1A1A1A] text-2xl mb-8 font-serif">
                  Ready to generate your research brief
                </h2>

                <div className="space-y-4 mb-6 text-left max-w-md mx-auto">
                  <div className="flex justify-between items-center py-4 border-b border-[#E8E5DD]">
                    <span className="text-[#6B6B6B] font-sans">Topic</span>
                    <span className="text-[#1A1A1A] font-medium font-serif text-lg">
                      {formData.topic}
                    </span>
                  </div>
                  <div className="flex justify-between items-center py-4 border-b border-[#E8E5DD]">
                    <span className="text-[#6B6B6B] font-sans">
                      Research Depth
                    </span>
                    <span className="text-[#1A1A1A] font-medium font-serif text-lg">
                      Level {formData.depth}
                    </span>
                  </div>
                  <div className="flex justify-between items-center py-4 border-b border-[#E8E5DD]">
                    <span className="text-[#6B6B6B] font-sans">
                      Summary Length
                    </span>
                    <span className="text-[#1A1A1A] font-medium font-serif text-lg">
                      ~{formData.summaryLength} words
                    </span>
                  </div>
                </div>

                <div className="max-w-md mx-auto mb-10 text-left">
                  <button
                    type="button"
                    onClick={() => setShowAdvancedOptions((open) => !open)}
                    aria-expanded={showAdvancedOptions}
                    className="w-full flex items-center justify-between border-t border-b border-[#E8E5DD] py-4 text-[#1A1A1A] transition-colors hover:text-[#2D7D8A]"
                  >
                    <span className="font-serif text-lg">
                      Advanced request options
                    </span>
                    <span className="text-xs font-sans uppercase tracking-[0.2em] text-[#6B6B6B]">
                      {showAdvancedOptions ? "Hide" : "Show"}
                    </span>
                  </button>

                  {showAdvancedOptions && (
                    <div className="border-b border-[#E8E5DD] px-1 py-5 space-y-5">
                      <p className="text-sm leading-6 text-[#6B6B6B] font-sans">
                        Use a provider credential for this request only. Nothing
                        is stored beyond the current brief.
                      </p>

                      <label className="flex items-center justify-between gap-4 text-[#1A1A1A] cursor-pointer">
                        <span className="font-serif text-lg">
                          Bring your own key
                        </span>
                        <input
                          type="checkbox"
                          aria-label="Bring your own key"
                          checked={byok.enabled}
                          onChange={(e) =>
                            handleByokEnabledChange(e.target.checked)
                          }
                          className="h-4 w-4 accent-[#D4A853]"
                        />
                      </label>

                      {byok.enabled && (
                        <div className="space-y-4 border-l border-[#E8E5DD] pl-4">
                          <div className="space-y-2">
                            <label
                              htmlFor="byok-provider"
                              className="block text-xs font-sans uppercase tracking-[0.2em] text-[#6B6B6B]"
                            >
                              Provider
                            </label>
                            <select
                              id="byok-provider"
                              aria-label="Provider"
                              value={byok.provider}
                              onChange={(e) =>
                                handleProviderChange(
                                  e.target.value as ByokEnvelope["provider"],
                                )
                              }
                              className="w-full bg-transparent border-b border-[#E8E5DD] px-0 py-3 text-[#1A1A1A] font-serif text-lg focus:outline-none"
                            >
                              <option value="google">Google Gemini</option>
                              <option value="cloudflare">
                                Cloudflare Workers AI
                              </option>
                              <option value="openrouter">OpenRouter</option>
                            </select>
                          </div>

                          {byok.provider === "cloudflare" ? (
                            <>
                              <div className="space-y-2">
                                <label
                                  htmlFor="byok-account-id"
                                  className="block text-xs font-sans uppercase tracking-[0.2em] text-[#6B6B6B]"
                                >
                                  Account ID
                                </label>
                                <input
                                  id="byok-account-id"
                                  aria-label="Account ID"
                                  type="text"
                                  value={byok.credentials.account_id ?? ""}
                                  onChange={(e) =>
                                    handleCredentialChange(
                                      "account_id",
                                      e.target.value,
                                    )
                                  }
                                  className="w-full bg-transparent border-b border-[#E8E5DD] px-0 py-3 text-[#1A1A1A] font-serif text-lg focus:outline-none"
                                  autoComplete="off"
                                />
                              </div>
                              <div className="space-y-2">
                                <label
                                  htmlFor="byok-api-token"
                                  className="block text-xs font-sans uppercase tracking-[0.2em] text-[#6B6B6B]"
                                >
                                  API Token
                                </label>

                                <input
                                  id="byok-api-token"
                                  aria-label="API Token"
                                  type="password"
                                  value={byok.credentials.api_token ?? ""}
                                  onChange={(e) =>
                                    handleCredentialChange(
                                      "api_token",
                                      e.target.value,
                                    )
                                  }
                                  className="w-full bg-transparent border-b border-[#E8E5DD] px-0 py-3 text-[#1A1A1A] font-serif text-lg focus:outline-none"
                                  autoComplete="off"
                                />
                              </div>
                            </>
                          ) : (
                            <div className="space-y-2">
                              <label
                                htmlFor="byok-api-key"
                                className="block text-xs font-sans uppercase tracking-[0.2em] text-[#6B6B6B]"
                              >
                                API Key
                              </label>
                              <input
                                id="byok-api-key"
                                aria-label="API key"
                                type="password"
                                value={byok.credentials.api_key ?? ""}
                                onChange={(e) =>
                                  handleCredentialChange(
                                    "api_key",
                                    e.target.value,
                                  )
                                }
                                className="w-full bg-transparent border-b border-[#E8E5DD] px-0 py-3 text-[#1A1A1A] font-serif text-lg focus:outline-none"
                                autoComplete="off"
                              />
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  )}
                </div>

                <motion.button
                  type="button"
                  onClick={onSubmit}
                  disabled={!isByokValid}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full max-w-md mx-auto block bg-[#D4A853] text-white font-medium py-4 rounded-none transition-all hover:bg-[#B8923D] font-sans tracking-wide uppercase text-sm disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  Generate Research Brief
                </motion.button>

                {!isByokValid && (
                  <p className="mt-4 text-sm text-[#6B6B6B] font-sans">
                    Complete the selected provider credentials to continue.
                  </p>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

import React from "react";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { ChatInterface } from "../ChatInterface";
import type { FormData } from "@/types";

jest.mock("framer-motion", () => ({
  AnimatePresence: ({ children }: { children: React.ReactNode }) => (
    <>{children}</>
  ),
  motion: new Proxy(
    {},
    {
      get: (_, tag: string) => {
        const Component = React.forwardRef<
          HTMLElement,
          React.PropsWithChildren<Record<string, unknown>>
        >(({ children, ...props }, ref) => {
          const domProps = { ...props };
          delete domProps.whileHover;
          delete domProps.whileTap;
          delete domProps.initial;
          delete domProps.animate;
          delete domProps.exit;
          delete domProps.transition;

          return React.createElement(
            tag,
            { ...domProps, ref },
            children as React.ReactNode,
          );
        });
        Component.displayName = "Motion" + tag;
        return Component;
      },
    },
  ),
}));

const streamResearchBrief = jest.fn();

jest.mock("@/lib/api", () => ({
  streamResearchBrief: (...args: unknown[]) => streamResearchBrief(...args),
}));

interface MockParameterCollectionProps {
  formData: FormData;
  setFormData: (data: FormData) => void;
  onSubmit: () => void;
}

jest.mock("../ParameterCollection", () => ({
  ParameterCollection: ({
    formData,
    setFormData,
    onSubmit,
  }: MockParameterCollectionProps) => (
    <div>
      <div data-testid="form-data">{JSON.stringify(formData)}</div>
      <button
        type="button"
        onClick={() =>
          setFormData({
            topic: "Artificial Intelligence",
            depth: 3,
            summaryLength: 300,
            byok: {
              enabled: false,
              provider: "google",
              credentials: {},
            },
          })
        }
      >
        Use default request data
      </button>
      <button
        type="button"
        onClick={() =>
          setFormData({
            topic: "Climate tech investment trends",
            depth: 3,
            summaryLength: 300,
            byok: {
              enabled: true,
              provider: "openrouter",
              credentials: {
                api_key: "sk-openrouter",
              },
            },
          })
        }
      >
        Use BYOK request data
      </button>
      <button type="button" onClick={onSubmit}>
        Submit request
      </button>
    </div>
  ),
}));

jest.mock("../LoadingDisplay", () => ({
  LoadingDisplay: () => <div>Loading…</div>,
}));

jest.mock("../ResultDisplay", () => ({
  ResultDisplay: ({ onReset }: { onReset: () => void }) => (
    <button type="button" onClick={onReset}>
      Start New Research
    </button>
  ),
}));

const mockBrief = {
  topic: "Test Topic",
  depth: 3,
  user_id: "user",
  follow_up: false,
  executive_summary: "Executive summary text.",
  research_questions: ["Q1?"],
  key_findings: ["Finding 1"],
  detailed_analysis: "Detailed text.",
  sources: [],
  created_at: "2026-04-09T00:00:00Z",
};

describe("ChatInterface", () => {
  beforeEach(() => {
    streamResearchBrief.mockReset();
  });

  it("submits the default request shape without byok when advanced BYOK is not enabled", async () => {
    streamResearchBrief.mockImplementation(async function* emptyStream() {});

    render(<ChatInterface />);

    fireEvent.click(
      screen.getByRole("button", { name: /use default request data/i }),
    );
    fireEvent.click(screen.getByRole("button", { name: /submit request/i }));

    await waitFor(() => expect(streamResearchBrief).toHaveBeenCalledTimes(1));

    const request = streamResearchBrief.mock.calls[0][0];

    expect(request).toEqual(
      expect.objectContaining({
        topic: "Artificial Intelligence",
        depth: 3,
        summary_length: 300,
        follow_up: false,
        user_id: expect.stringMatching(/^user_\d+$/),
      }),
    );
    expect(request).not.toHaveProperty("byok");
  });

  it("includes a request-scoped byok envelope when advanced BYOK is enabled", async () => {
    streamResearchBrief.mockImplementation(async function* emptyStream() {});

    render(<ChatInterface />);

    fireEvent.click(
      screen.getByRole("button", { name: /use byok request data/i }),
    );
    fireEvent.click(screen.getByRole("button", { name: /submit request/i }));

    await waitFor(() => expect(streamResearchBrief).toHaveBeenCalledTimes(1));

    expect(streamResearchBrief.mock.calls[0][0]).toEqual(
      expect.objectContaining({
        topic: "Climate tech investment trends",
        byok: {
          enabled: true,
          provider: "openrouter",
          credentials: {
            api_key: "sk-openrouter",
          },
        },
      }),
    );
  });

  it("clears in-memory byok data after reset", async () => {
    streamResearchBrief.mockImplementation(async function* resultStream() {
      yield { type: "result", data: mockBrief };
      yield { type: "complete" };
    });

    render(<ChatInterface />);

    fireEvent.click(
      screen.getByRole("button", { name: /use byok request data/i }),
    );
    fireEvent.click(screen.getByRole("button", { name: /submit request/i }));

    await screen.findByRole("button", { name: /start new research/i });
    fireEvent.click(
      screen.getByRole("button", { name: /start new research/i }),
    );

    await waitFor(() => {
      expect(screen.getByTestId("form-data")).toHaveTextContent(
        JSON.stringify({
          topic: "",
          depth: 3,
          summaryLength: 300,
          byok: {
            enabled: false,
            provider: "google",
            credentials: {},
          },
        }),
      );
    });
  });
});

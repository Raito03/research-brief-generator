import React, { useState } from "react";
import { fireEvent, render, screen } from "@testing-library/react";
import { ParameterCollection } from "../ParameterCollection";
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

const defaultFormData: FormData = {
  topic: "",
  depth: 3,
  summaryLength: 300,
  byok: {
    enabled: false,
    provider: "google",
    credentials: {},
  },
};

function Harness() {
  const [formData, setFormData] = useState<FormData>(defaultFormData);

  return (
    <ParameterCollection
      formData={formData}
      setFormData={(nextFormData) => setFormData(nextFormData)}
      onSubmit={() => {}}
    />
  );
}

describe("ParameterCollection", () => {
  it("shows a restrained advanced BYOK section in confirmation with provider-specific credential fields", async () => {
    render(<Harness />);

    fireEvent.change(screen.getByPlaceholderText(/artificial intelligence/i), {
      target: { value: "Carbon border adjustment mechanism" },
    });
    fireEvent.click(screen.getByRole("button", { name: /continue/i }));
    fireEvent.click(await screen.findByRole("button", { name: /balanced/i }));
    fireEvent.click(await screen.findByRole("button", { name: /standard/i }));

    await screen.findByText(/ready to generate your research brief/i);

    fireEvent.click(
      screen.getByRole("button", { name: /advanced request options/i }),
    );

    expect(screen.getByLabelText(/bring your own key/i)).toBeInTheDocument();
    fireEvent.click(screen.getByLabelText(/bring your own key/i));

    expect(screen.getByLabelText(/provider/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/api key/i)).toBeInTheDocument();

    fireEvent.change(screen.getByLabelText(/provider/i), {
      target: { value: "cloudflare" },
    });

    expect(screen.getByLabelText(/account id/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/api token/i)).toBeInTheDocument();
    expect(screen.queryByLabelText(/^api key$/i)).not.toBeInTheDocument();
  });
});

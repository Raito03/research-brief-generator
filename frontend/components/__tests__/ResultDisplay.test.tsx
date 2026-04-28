import { render, screen } from '@testing-library/react';
import { ResultDisplay } from '../ResultDisplay';

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
  created_at: "2026-04-09T00:00:00Z"
};

describe('ResultDisplay', () => {
  it('renders all content continuously without accordion buttons', () => {
    render(<ResultDisplay brief={mockBrief} onReset={() => {}} />);
    
    // Both sections should be visible immediately without clicking
    expect(screen.getByText('Executive summary text.')).toBeInTheDocument();
    expect(screen.getByText('Detailed text.')).toBeInTheDocument();
    
    // There should be no "toggle" buttons used for accordions
    const buttons = screen.queryAllByRole('button');
    // Only the 'Start New Research' button should exist
    expect(buttons).toHaveLength(1);
    expect(buttons[0]).toHaveTextContent('Start New Research');
  });
});

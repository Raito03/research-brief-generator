# AI Research Brief Generator - Frontend

A sleek, minimalist Next.js frontend for the AI Research Brief Generator with real-time streaming logs and fluid animations.

## Features

- **Conversational UI**: Step-by-step parameter collection for intuitive user experience
- **Real-time Streaming**: Live log updates showing research progress with carousel animations
- **Animated Accordions**: Beautiful expandable sections for research results
- **Dark Theme**: Custom color palette (Chinese Black, Cadet Grey, American Blue, Ube, Cool Grey)
- **Responsive Design**: Optimized for both mobile and desktop
- **Smooth Animations**: Powered by Framer Motion for fluid micro-interactions

## Tech Stack

- **Framework**: Next.js 15+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Typography**: Lexend font family

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Backend API running on port 8000

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:3000`

### Environment Variables

Create a `.env.local` file in the root:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For production, update this to your deployed backend API URL.

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout with Lexend font
│   ├── page.tsx            # Home page
│   └── globals.css         # Global styles and theme
├── components/
│   ├── ChatInterface.tsx   # Main interface orchestrator
│   ├── ParameterCollection.tsx  # Step-by-step input flow
│   ├── LoadingDisplay.tsx  # Streaming logs with loader
│   └── ResultDisplay.tsx   # Animated accordion results
├── lib/
│   └── api.ts              # API client with SSE streaming
└── types/
    └── index.ts            # TypeScript type definitions
```

## Usage Flow

1. **Topic Input**: User enters research topic (min 5 characters)
2. **Depth Selection**: Choose research depth level (1-5)
3. **Length Selection**: Select preferred summary length (100-1000 words)
4. **Confirmation**: Review parameters before submission
5. **Loading**: Watch real-time logs with animated carousel effect
6. **Results**: Explore research brief in expandable sections

## Design Philosophy

- **Minimalism**: Clean interface with essential elements only
- **Fluidity**: All transitions use smooth easing functions
- **Clarity**: Clear visual hierarchy with consistent spacing
- **Responsiveness**: Touch-optimized for mobile, spacious for desktop
- **Accessibility**: Focus states and keyboard navigation support

## Customization

### Colors

Edit `app/globals.css` to customize the color palette:

```css
:root {
  --chinese-black: #0A1123;
  --cadet-grey: #959BB5;
  --american-blue: #3A3E6C;
  --ube: #8387C3;
  --cool-grey: #8A8CAC;
}
```

### Typography

Change font in `app/layout.tsx`:

```typescript
import { YourFont } from "next/font/google";

const yourFont = YourFont({
  variable: "--font-your-font",
  subsets: ["latin"],
});
```

## Building for Production

```bash
npm run build
npm start
```

## API Integration

The frontend connects to the backend streaming endpoint:

```
POST /brief/stream
```

Expected SSE message format:

```json
{
  "type": "log" | "result" | "complete" | "error",
  "message": "Log message",
  "data": { ...briefData }
}
```

## Performance

- **First Load JS**: ~155 KB
- **Build Time**: ~7 seconds
- **Static Generation**: All pages pre-rendered

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## License

Same as parent project

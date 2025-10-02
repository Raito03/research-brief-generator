# Frontend Setup Guide

## Quick Start

The frontend is a modern Next.js application located in the `frontend/` directory.

### 1. Start the Backend API

First, ensure your Python backend is running:

```bash
# From the project root
python app/api.py
```

The API should be running on `http://localhost:8000`

### 2. Start the Frontend

In a new terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000`

## What You'll See

### Step 1: Topic Input
- Clean, centered interface with minimalist design
- Enter your research topic (minimum 5 characters)
- Character counter shows progress

### Step 2: Research Depth
- Select depth level 1-5
- Each level shows what to expect (number of sources)
- Hover animations on selection cards

### Step 3: Summary Length
- Choose preferred word count: 100, 300, 600, or 1000 words
- Grid layout for easy selection
- Visual feedback on selection

### Step 4: Confirmation
- Review all parameters before submission
- Option to go back and change any parameter
- Generate button triggers the research

### Step 5: Loading with Streaming Logs
- Animated loader with rotating ring
- Real-time log messages from backend appear below
- Top-down carousel effect: newest logs highlighted, older ones fade
- Shows progress through workflow stages

### Step 6: Results Display
- Executive Summary expanded by default
- Other sections collapsed (click to expand)
- Smooth accordion animations
- Source cards with credibility scores
- "New Search" button to start over

## Design Features

### Color Palette
- **Chinese Black (#0A1123)**: Main background
- **Cadet Grey (#959BB5)**: Primary text
- **American Blue (#3A3E6C)**: Secondary elements
- **Ube (#8387C3)**: Accent color (buttons, highlights)
- **Cool Grey (#8A8CAC)**: Muted text

### Typography
- **Font**: Lexend (from Google Fonts)
- Clean, modern, highly readable
- Fallbacks: Helvetica Neue, Open Sans

### Animations
- Framer Motion for all transitions
- Smooth easing: cubic-bezier(0.25, 0.1, 0.25, 1)
- Micro-interactions on hover and click
- Page transitions between states

## Mobile Responsiveness

The interface adapts to different screen sizes:

- **Mobile (< 768px)**: Single column, touch-optimized
- **Tablet (768px - 1024px)**: Comfortable spacing
- **Desktop (> 1024px)**: Maximum width with centered layout

## API Connection

The frontend connects to your backend's streaming endpoint:

```
POST http://localhost:8000/brief/stream
```

Request format:
```json
{
  "topic": "Your research topic",
  "depth": 3,
  "user_id": "user_1234567890",
  "summary_length": 300,
  "follow_up": false
}
```

## Development Tips

### Hot Reload
Next.js automatically reloads when you save files. No need to restart the server.

### Debugging
- Open browser DevTools (F12)
- Check Console for errors
- Network tab shows API requests
- React DevTools for component inspection

### Customization
- Colors: `frontend/app/globals.css`
- Components: `frontend/components/`
- API URL: `frontend/.env.local`

## Building for Production

```bash
cd frontend
npm run build
npm start
```

Production build is optimized and minified.

## Troubleshooting

### Frontend won't start
- Check Node.js version (18+)
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again

### Can't connect to API
- Verify backend is running on port 8000
- Check `.env.local` has correct API URL
- Look for CORS errors in browser console

### Logs not streaming
- Backend must be running
- Check `/brief/stream` endpoint exists
- Verify SSE format in backend response

### Styling issues
- Clear browser cache
- Check Tailwind CSS is configured
- Verify `globals.css` is imported

## Next Steps

1. Customize the color scheme to match your brand
2. Add user authentication for personalized experiences
3. Implement result saving/bookmarking
4. Add export functionality (PDF, Markdown)
5. Create shareable links for research briefs

## Support

For issues or questions:
- Check browser console for errors
- Review `frontend/README.md` for detailed docs
- Test API endpoint directly with curl/Postman
- Verify backend logs show incoming requests

---

**Enjoy your sleek AI research assistant!** 🚀

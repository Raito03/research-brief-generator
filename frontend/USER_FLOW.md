# User Flow Documentation

## Visual Journey Through the AI Research Assistant

### 🎯 State Flow Diagram

```
┌─────────────┐
│    IDLE     │ ← Initial state when user lands
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ COLLECTING  │ ← User inputs parameters step-by-step
│             │   • Topic (min 5 chars)
│             │   • Depth (1-5)
│             │   • Length (100-1000 words)
│             │   • Confirm
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   LOADING   │ ← API streaming in progress
│             │   • Animated loader
│             │   • Real-time log carousel
│             │   • Latest logs highlighted
└──────┬──────┘
       │
       ├────────────┐
       │            │
       ▼            ▼
┌─────────────┐  ┌─────────────┐
│   RESULT    │  │    ERROR    │
│             │  │             │
│ • Executive │  │ • Error msg │
│ • Analysis  │  │ • Try again │
│ • Sources   │  │             │
│ • Findings  │  │             │
└──────┬──────┘  └──────┬──────┘
       │                 │
       └────────┬────────┘
                │
                ▼
           ┌─────────────┐
           │  New Search │ ← Reset to IDLE
           └─────────────┘
```

## Step-by-Step User Experience

### 1️⃣ Landing (IDLE)

**What User Sees:**
- Clean, centered interface
- Dark gradient background with subtle animation
- Title: "AI Research Assistant"
- Subtitle: "Get comprehensive insights in seconds"

**No Actions Required Yet** - User immediately sees the topic input

---

### 2️⃣ Topic Input (COLLECTING - Step 1)

**UI Elements:**
```
┌────────────────────────────────────────────┐
│  What would you like to research?          │
│                                            │
│  ┌────────────────────────────────────┐  │
│  │ [Your topic here...              ] │  │
│  └────────────────────────────────────┘  │
│  5/200 characters (min 5)                 │
│                                            │
│  ┌────────────────────────────────────┐  │
│  │          Continue          │  │
│  └────────────────────────────────────┘  │
└────────────────────────────────────────────┘
```

**Interactions:**
- Type in text input (auto-focused)
- See character counter update live
- Continue button disabled until 5+ chars
- Press Enter or click Continue
- Smooth slide-out animation to next step

---

### 3️⃣ Depth Selection (COLLECTING - Step 2)

**UI Elements:**
```
┌────────────────────────────────────────────┐
│  ← Back                                    │
│                                            │
│  How deep should the research be?          │
│                                            │
│  ┌────────────────────────────────────┐  │
│  │ Quick         2-3 sources        1 │ ◄─ Hover: slides right
│  └────────────────────────────────────┘  │
│  ┌────────────────────────────────────┐  │
│  │ Light         3-4 sources        2 │  │
│  └────────────────────────────────────┘  │
│  ┌────────────────────────────────────┐  │
│  │ Balanced      4-6 sources        3 │ ◄─ Selected (highlighted)
│  └────────────────────────────────────┘  │
│  ┌────────────────────────────────────┐  │
│  │ Detailed      6-8 sources        4 │  │
│  └────────────────────────────────────┘  │
│  ┌────────────────────────────────────┐  │
│  │ Thorough      8-10 sources       5 │  │
│  └────────────────────────────────────┘  │
└────────────────────────────────────────────┘
```

**Interactions:**
- Click any option to select
- Instant transition to next step
- Back button returns to topic input
- Hover animations on each card

---

### 4️⃣ Length Selection (COLLECTING - Step 3)

**UI Elements:**
```
┌────────────────────────────────────────────┐
│  ← Back                                    │
│                                            │
│  Preferred summary length?                 │
│                                            │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │ Brief   │  │Standard │  │Extended │  │ ◄─ Grid layout
│  │~100 wds │  │~300 wds │  │~600 wds │  │
│  └─────────┘  └─────────┘  └─────────┘  │
│                                            │
│  ┌─────────────────────────────────────┐  │
│  │      Comprehensive (~1000 wds)      │  │
│  └─────────────────────────────────────┘  │
└────────────────────────────────────────────┘
```

**Interactions:**
- Click to select length
- Scale animation on hover
- Instant transition to confirmation
- Back returns to depth selection

---

### 5️⃣ Confirmation (COLLECTING - Step 4)

**UI Elements:**
```
┌────────────────────────────────────────────┐
│  ← Back                                    │
│                                            │
│  Ready to generate your research brief     │
│                                            │
│  Topic          AI in Healthcare           │
│  ─────────────────────────────────────────│
│  Research Depth        Level 3             │
│  ─────────────────────────────────────────│
│  Summary Length      ~300 words            │
│                                            │
│  ┌────────────────────────────────────┐  │
│  │   Generate Research Brief    │  │
│  └────────────────────────────────────┘  │
└────────────────────────────────────────────┘
```

**Interactions:**
- Review all parameters
- Back to change anything
- Click Generate → Transition to LOADING
- Smooth scale-out animation

---

### 6️⃣ Loading with Streaming (LOADING)

**UI Elements:**
```
┌────────────────────────────────────────────┐
│                                            │
│              ⭕ (rotating ring)             │
│                                            │
│            Researching...                  │
│  Gathering insights from multiple sources  │
│                                            │
│  ┌────────────────────────────────────┐  │
│  │ 📋 PLANNING: Creating research plan│ ◄─ Latest (bright)
│  │ ✅ Generated plan with 6 queries   │ ◄─ Previous (faded)
│  │ 🔎 Query 1: 'AI healthcare...'    │ ◄─ Older (more faded)
│  │ ✅ FOUND: Research paper...       │  │
│  │ 📝 SUMMARIZING: Using Grok AI     │  │
│  │ ... (scrolls up automatically)     │  │
│  └────────────────────────────────────┘  │
│                                            │
│  Showing latest 10 of 47 messages          │
└────────────────────────────────────────────┘
```

**Animations:**
- Loader rotates continuously
- Pulse effect on loader ring
- New logs slide in from bottom
- Previous logs fade and move up
- Latest log has bright border
- Auto-scroll follows new messages

**Log Categories:**
- 📋 Planning phase
- 🔎 Search queries
- ✅ Success messages
- 📝 Summarization
- 🎯 Synthesis
- ❌ Errors (if any)

---

### 7️⃣ Results Display (RESULT)

**UI Elements:**
```
┌────────────────────────────────────────────┐
│  AI in Healthcare           [New Search]   │
│  Research completed in 42.3s               │
│                                            │
│  ┌────────────────────────────────────┐  │
│  │ Executive Summary              ▼  │ ◄─ EXPANDED
│  ├────────────────────────────────────┤  │
│  │ This comprehensive research brief  │  │
│  │ examines AI in healthcare and...   │  │
│  │ [full summary text visible]        │  │
│  └────────────────────────────────────┘  │
│                                            │
│  ┌────────────────────────────────────┐  │
│  │ Detailed Analysis              ▶  │ ◄─ Collapsed
│  └────────────────────────────────────┘  │
│                                            │
│  ┌────────────────────────────────────┐  │
│  │ Key Findings                   ▶  │ ◄─ Collapsed
│  └────────────────────────────────────┘  │
│                                            │
│  ┌────────────────────────────────────┐  │
│  │ Research Questions             ▶  │ ◄─ Collapsed
│  └────────────────────────────────────┘  │
│                                            │
│  ┌────────────────────────────────────┐  │
│  │ Sources (8)                    ▶  │ ◄─ Collapsed
│  └────────────────────────────────────┘  │
└────────────────────────────────────────────┘
```

**Interactions:**
- Click any section header to expand/collapse
- Smooth height animation
- Arrow rotates 180° when expanding
- Executive Summary expanded by default
- Scroll to view long content
- Click "New Search" to reset

**Expanded Section Examples:**

**Key Findings:**
```
┌────────────────────────────────────────┐
│ Key Findings                       ▼  │
├────────────────────────────────────────┤
│ • AI diagnostics improving accuracy    │
│ • Regulatory challenges remain         │
│ • Cost reduction in imaging analysis   │
│ • Privacy concerns being addressed     │
│ • Growing adoption in hospitals        │
└────────────────────────────────────────┘
```

**Sources:**
```
┌────────────────────────────────────────┐
│ Sources (8)                        ▼  │
├────────────────────────────────────────┤
│ ┌──────────────────────────────────┐ │
│ │ AI in Medical Imaging: 2024      │ │
│ │ This source discusses emerging...│ │
│ │ Relevance: 92%  Credibility: 88% │ │
│ │ Key Points:                       │ │
│ │ → Improved diagnostic accuracy    │ │
│ │ → Reduced processing time         │ │
│ └──────────────────────────────────┘ │
│ [more sources...]                     │
└────────────────────────────────────────┘
```

---

### 8️⃣ Error State (ERROR)

**UI Elements:**
```
┌────────────────────────────────────────────┐
│                                            │
│                                            │
│         Something went wrong               │
│                                            │
│  Failed to connect to API. Please check   │
│  that the backend server is running.      │
│                                            │
│  ┌────────────────────────────────────┐  │
│  │          Try Again         │  │
│  └────────────────────────────────────┘  │
│                                            │
└────────────────────────────────────────────┘
```

**Interactions:**
- Click "Try Again" → Returns to IDLE
- Clear error message displayed
- Friendly, non-technical language

---

## Animation Timing Reference

### Transitions
- **Page transitions**: 400ms cubic-bezier(0.25, 0.1, 0.25, 1)
- **Accordion expand**: 300ms cubic-bezier(0.25, 0.1, 0.25, 1)
- **Button hover**: 200ms ease-out
- **Log carousel**: 300ms ease-in-out

### Micro-interactions
- **Button press**: scale(0.98)
- **Button hover**: scale(1.02)
- **Card hover**: translateX(4px)
- **Loader rotation**: 2s linear infinite
- **Loader pulse**: 1.5s ease-in-out infinite

### Entrance Animations
- **Staggered items**: 100ms delay per item
- **Initial page load**: 400ms fade + slide
- **New log message**: 300ms slide from bottom

---

## Responsive Breakpoints

### Mobile (< 768px)
- Single column layout
- Larger touch targets (min 48px)
- Compact spacing
- Bottom-aligned buttons
- Reduced animation complexity

### Tablet (768px - 1024px)
- 2-column grid for length selection
- Comfortable spacing
- Full animations enabled

### Desktop (> 1024px)
- 4-column grid for length selection
- Maximum width: 896px (56rem)
- Centered layout
- Enhanced animations
- Hover states more prominent

---

## Accessibility Features

### Keyboard Navigation
- Tab through all interactive elements
- Enter to submit forms
- Arrow keys for depth selection
- Escape to close expanded sections

### Screen Readers
- Semantic HTML structure
- ARIA labels on interactive elements
- Status announcements for loading
- Clear section headings

### Visual
- High contrast text (WCAG AA compliant)
- Focus indicators on all interactive elements
- No critical info conveyed by color alone
- Sufficient spacing for readability

---

## Tips for Best Experience

1. **Use descriptive topics** - Be specific for better results
2. **Choose appropriate depth** - Level 3 is optimal for most queries
3. **Watch the logs** - See the AI's research process in real-time
4. **Explore all sections** - Each contains unique insights
5. **Check source credibility** - Scores help assess reliability

---

**Designed for clarity, built for speed, optimized for insight.** ✨

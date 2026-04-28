# Frontend Aesthetic Redesign - Scientific/Research Direction

## Overview

Redesign the frontend to feel like a well-printed academic research journal - authoritative, clean, focused on content.

## Visual Direction

**Vibe:** "A carefully typeset research paper you'd find in a university library"

---

## Typography

### Headings
- **Font:** Serif (Playfair Display or similar)
- **Weight:** 500-600 (not bold, sophisticated)
- **Purpose:** Conveys authority and intelligence
- **Usage:** Page titles, section headings, brief titles

### Body
- **Font:** Clean sans-serif (Inter, system-ui fallback)
- **Weight:** 400 (regular)
- **Purpose:** Maximum readability
- **Usage:** All body text, form labels, results

### Monospace
- **Usage:** Source citations, URLs, any data-heavy text
- **Style:** Small, muted color

---

## Color Palette

### Primary Colors (Warm, Paper-Ink Feel)
| Role | Color | Hex |
|------|-------|-----|
| Background | Warm off-white | `#FAF8F5` |
| Background Alt | Cream | `#F5F2EB` |
| Text Primary | Deep charcoal | `#1A1A1A` |
| Text Secondary | Warm gray | `#6B6B6B` |
| Text Muted | Light gray | `#9A9A9A` |

### Accent (Subtle, Strategic)
| Role | Color | Hex |
|------|-------|-----|
| Accent Primary | Amber gold | `#D4A853` |
| Accent Hover | Deep amber | `#B8923D` |
| Links | Teal | `#2D7D8A` |

### UI Elements (Minimal)
| Role | Color | Hex |
|------|-------|-----|
| Borders | Light warm gray | `#E8E5DD` |
| Dividers | Subtle | `#F0EDE6` |
| Input BG | White | `#FFFFFF` |
| Card BG | White | `#FFFFFF` |

---

## Layout Principles

### Whitespace
- **Generous margins** - Signal confidence, not desperation to fill space
- **Relaxed line-height** - 1.6-1.7 for body text (readability)
- **Section spacing** - Clear separation between functional areas

### Hierarchy
1. **Very clear** - Reader shouldn't wonder what matters
2. **Size contrast** - Substantial but not dramatic
3. **One focal point per section**

### Components
- **Minimal containers** - No card borders unless needed
- **Subtle shadows only** - Like paper lying on a desk
- **No gradients** - Flat, clean colors only

---

## Animations

**Philosophy:** Like turning a page - deliberate, smooth, not flashy.

### What to Keep
- Subtle fade-in on load (200-300ms)
- Gentle slide for accordion expand
- Smooth transitions on hover

### What to Remove
- Any "pop" or bounce effects
- Excessive motion
- Background animations
- Glowing borders

---

## Component Guidelines

### Chat Input
- Clean input line, no heavy borders
- Subtle focus state (thin border color change)
- Clear button, not "call to action" styling

### Parameter Form
- Minimal accordion - clean sections
- Clear labels (sentence case, not ALL CAPS)
- Few options = inline or compact dropdown

### Results Display
- Clear hierarchy: title → summary → sources
- Citations look like academic references
- Expandable sections smooth, not dramatic

### Loading State
- Minimal indicator (subtle pulse or line)
- "Researching..." text, not elaborate animation

---

## Dark Mode (Future)

If implemented:
| Role | Color |
|------|-------|
| Background | Deep warm black `#1A1815` |
| Text | Soft cream `#E8E5DD` |
| Accent | Muted amber |

But focus on light mode first.

---

## Summary

This aesthetic says: *"This is a serious research tool. The design gets out of your way so you can focus on insights."*

Not: "Look at me!"  
But: "Here's what you need."

---

## Implementation Notes

- Start with globals.css (colors, typography)
- Update page.tsx layout
- Refine component styles one at a time
- Test readability with actual content

## Acceptance Criteria

- [ ] Feels like a research journal, not a tech product
- [ ] Typography is clear and authoritative
- [ ] Colors are warm, not cold/techy
- [ ] Animation is subtle and deliberate
- [ ] Content (research briefs) are the focus
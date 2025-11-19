# Design Guidelines: Diário do Contador - Volunteer Activity Tracker

## Design Approach

**System Selected**: Material Design principles adapted for form-heavy utility application
**Rationale**: This is a utility-focused application where efficiency, clarity, and mobile usability are paramount. The design prioritizes rapid data entry, clear form structure, and minimal cognitive load for volunteers who will use this repeatedly.

## Core Design Principles

1. **Mobile-First**: All layouts optimized for phone use (volunteers filling forms on-the-go)
2. **Form Efficiency**: Minimize taps/inputs, maximize auto-fill and smart defaults
3. **Clear Hierarchy**: Strong visual distinction between sections and input types
4. **Positive Reinforcement**: Dashboard celebrates volunteer contributions without distraction

---

## Typography

**Font Family**: 
- Primary: Inter or Roboto (clean, highly legible for forms)
- Fallback: system-ui, -apple-system, sans-serif

**Scale**:
- Page Titles: text-2xl (24px) font-semibold
- Section Headers: text-lg (18px) font-medium
- Form Labels: text-sm (14px) font-medium
- Input Text: text-base (16px) regular
- Helper Text: text-xs (12px) regular
- Dashboard Stats: text-3xl (30px) font-bold for numbers

**Line Height**: Generous spacing (leading-relaxed) for readability in forms

---

## Layout System

**Spacing Units**: Tailwind units of 2, 4, 6, and 8 for consistency
- Component padding: p-4 or p-6
- Section margins: mb-6 or mb-8
- Input spacing: space-y-4
- Tight groupings: gap-2

**Container Structure**:
- Max width: max-w-2xl (forms work best in narrower containers)
- Mobile: Full width with px-4 padding
- Desktop: Centered container with px-6

**Grid System**:
- Mobile: Single column (grid-cols-1)
- Tablet/Desktop: 2 columns for patient age/gender inputs (grid-cols-2)
- Dashboard metrics: 3 columns on desktop (grid-cols-1 md:grid-cols-3)

---

## Component Library

### Navigation
- **Header**: Sticky top bar with logo/app name, volunteer name, logout button
- Simple horizontal layout, h-16, shadow for elevation
- Mobile: Hamburger menu if needed (keep minimal - likely just Dashboard/New Entry/Logout)

### Forms & Inputs

**Text Inputs**:
- Full width with rounded corners (rounded-md)
- Padding: px-4 py-3
- Border width: border-2 with focus ring
- Labels above inputs with mb-2

**Numeric Inputs** (for hours, patient counts):
- Smaller width: w-20 or w-24
- Large touch targets (min-h-12)
- Step controls visible on mobile

**Select/Dropdown** (Período: Manhã/Tarde/Noite):
- Native select element styled consistently
- Large tap target: h-12

**Checkboxes** (Local de Atendimento):
- Grid layout: grid-cols-2 md:grid-cols-3
- Each checkbox with label in a card-like container (p-3, rounded)
- Large touch targets with padding

**Autocomplete** (Livros):
- Search input with dropdown suggestions
- Results shown in elevated card below input
- Each result shows: Title (font-medium), Author, Editora (text-sm)
- "+ Add New Book" option at bottom of results

**Textarea** (Relato Qualitativo):
- Full width, min height: min-h-32
- Rounded corners, padding: p-4
- Character counter if needed (text-xs)

**Patient Age/Gender Grid**:
```
Structure per age range:
[Age Label: "0-3 anos"]
[F: ___ | M: ___]

Layout: 
- Mobile: Single column, stacked rows
- Desktop: 2 or 3 columns of age ranges
- Each gender input: w-16, inline
```

### Buttons

**Primary Action** (Submit, Save):
- Full width on mobile (w-full md:w-auto)
- Height: h-12
- Rounded: rounded-lg
- Font: font-semibold

**Secondary Actions** (Cancel, Back):
- Same sizing, different visual weight
- Outlined style

**Button Placement**:
- Sticky bottom bar on mobile for primary action
- Standard placement (bottom-right or center) on desktop

### Cards

**Dashboard Stats Cards**:
- Rounded corners: rounded-xl
- Padding: p-6
- Shadow for depth: shadow-md
- Content: Large number (text-3xl), small label below (text-sm)

**Medal/Achievement Display**:
- Centered card with icon/illustration placeholder
- Congratulatory message
- Appears after form submission

### Data Display

**Bar Chart** (Volunteer Hours):
- Simple horizontal bars
- Label on left, colored bar, number on right
- Responsive: stacks on mobile
- Use CSS for bars (height based on data percentage)

**Table** (if showing history):
- Responsive: card layout on mobile
- Zebra striping for rows
- Sticky header on desktop

---

## Page Layouts

### Login Page
- Centered card: max-w-md
- Logo/title at top
- Simple 2-field form (username, password)
- Single prominent login button
- Minimal, focused design

### Dashboard (Volunteer Home)
- Top: Welcome message with volunteer name
- Metrics grid: Total hours (month/year), activities count, books read
- Medal/badge display if milestones reached
- Primary CTA: "Nova Atuação" button (prominent, centered)
- Secondary: Recent activities list (simple cards)

### Form Page (Diário Entry)
- Progress indicator optional (step 1/3 if multi-page)
- Clear section headers with icons
- Section 1: Data & Período (pre-filled date, period select)
- Section 2: Duração (numeric input, clear label "horas")
- Section 3: Pacientes (age/gender grid)
- Section 4: Local de Atendimento (checkbox grid)
- Section 5: Livros (autocomplete search + manual entry toggle)
- Section 6: Relato (textarea)
- Bottom: Save button (sticky on mobile)
- Auto-save indication (small "Saved" text)

### Confirmation/Success Page
- Centered card with success icon
- "Atuação registrada!" message
- Medal display if applicable
- Summary of entry (hours, patients served)
- CTA: "Ver Dashboard" or "Nova Atuação"

---

## Interaction Patterns

**Auto-complete Behavior**:
- Show suggestions after 2 characters typed
- Highlight matching text
- Arrow keys to navigate, Enter to select
- ESC to close dropdown

**Form Validation**:
- Inline validation on blur
- Error messages below inputs (text-sm, red tone)
- Success states subtle (green accent)
- Required field indicators (asterisk)

**Loading States**:
- Button shows "Salvando..." during submission
- Subtle spinner on autocomplete while searching
- No full-page overlays

**Empty States**:
- Dashboard with no activities: Friendly message, large CTA to create first entry
- Autocomplete no results: Offer to add new book
- Simple illustrations or icons

---

## Accessibility

- All form inputs have visible labels (never placeholder-only)
- Focus states clearly visible (ring-2 with offset)
- Color contrast meets WCAG AA standards
- Touch targets minimum 44x44px
- Semantic HTML (proper heading hierarchy)
- ARIA labels for icon-only buttons
- Keyboard navigation fully supported

---

## Images

**Dashboard Medal/Badge**: Illustrated badge/medal graphic (SVG or PNG) displayed in a centered card when volunteer reaches milestones. Keep cheerful and achievement-oriented.

**Empty State Illustrations**: Small, simple illustrations for empty dashboard or no results found (optional but recommended for warmth).

**No Hero Image**: This is a utility app - skip hero sections entirely. Focus on functional clarity.

---

## Mobile Optimization

- Sticky header (minimal height)
- Sticky bottom action bar for primary buttons
- Large tap targets throughout
- Vertical rhythm optimized for scrolling
- Avoid horizontal scrolling
- Native form inputs when possible (date picker, number input)
- Minimize pinch-to-zoom needs

---

## Performance Notes

- No animations except: subtle fade-ins on success messages, smooth autocomplete dropdown
- Lazy load dashboard charts
- Optimize form for quick fills (tab order logical)
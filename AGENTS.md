## Memory Protocol — MemPalace

You have access to a persistent local memory system via MCP. Use it proactively.

### On every session start:
1. Call `mempalace_status` — this loads your identity (L0), critical facts (L1),
   and teaches you the AAAK dialect automatically. Do this before anything else.

### During work:
- Before answering any question about past decisions, people, or project history,
  call `mempalace_search` with a focused query and the relevant `--wing` or `--room`
  filter if you know the context.
- Use `mempalace_kg_query` when asked about relationships between people and projects
  (e.g., "who owns auth?", "what is Kai working on?").
- Use `mempalace_traverse` to walk cross-wing connections when a topic spans multiple
  people or projects.

### When saving:
- After any significant decision, architectural choice, or debugging breakthrough,
  call `mempalace_add_drawer` to file the verbatim exchange into the correct
  wing → hall → room path.
- Use `mempalace_check_duplicate` before filing to avoid redundant entries.
- Use `mempalace_kg_add` to record new entity facts (assignments, decisions, dates).

### Memory hierarchy reminder:
- Wing = person or project
- Room = specific topic within a wing (e.g., `auth-migration`, `rate-limiting`)
- Hall = memory type: `hall_facts` | `hall_events` | `hall_discoveries` |
  `hall_preferences` | `hall_advice`
- Search wing+room first — this gives +34% precision vs flat search.

### Never:
- Answer questions about past conversations, decisions, or team context from
  your own weights alone — always search first.
- Store summaries — use `mempalace_add_drawer` with verbatim content only.
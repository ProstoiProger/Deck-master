# Domain card: AI assistants and LLM systems

Named models and tools change quickly; verify them against current releases (as of 2026-10).

- **Typical decks**: AI-track hackathons, product demos, internal pilots.
- **Audience asks first**: does it hallucinate, where does the data go, what does it cost, what happens when it fails.
- **Evidence expected**: a fixed evaluation set (20 to 100 cases) with pass rate against a simple baseline, failure
  categories, latency and cost per request, human review rate.
- **Vocabulary**: "grounded in documents", "refuses when unsure"; avoid "AI magic" and unexplained model names.
- **Slides that matter**: `solution` with a screenshot, `architecture` (retrieval or tools, model, guardrails),
  `demo` with one handled failure, `comparison` (against baseline), `impact` (limits and safety).
- **Risks**: privacy, prompt injection from documents, hallucination, bias, licensing of data and models.
- **Visuals**: conversation screenshots with synthetic data, architecture with guardrails highlighted.
- **Sources**: your evaluation file; provider pricing pages (check the date).

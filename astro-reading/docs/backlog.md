# Backlog

Planned work, roughly in priority order. Each item is small enough to be done and tested on its own.

1. **Qdrant knowledge base.** Implement `KnowledgeBase` on top of Qdrant with embeddings, and a `--knowledge-backend` option to choose it. Keep the in-memory version for tests.
2. **Knowledge ingestion script.** Read reference files, split them into passages and load them into Qdrant. Source files stay out of git.
3. **Choose among several places.** GeoNames can return many matches for a name. Show the top results and let the user pick, instead of using only the most populous one.
4. **Birth time validation against the time zone.** Detect local times that did not exist or were ambiguous because of daylight saving changes, and warn the user.
5. **Retries and clearer service errors.** Retry on timeouts and rate limits with backoff, and give a distinct message for each case without leaking input.
6. **PDF export.** Add `--format pdf` next to Markdown.
7. **Language option.** Add `--language` and pass it to the writer instead of the fixed default.
8. **Load `.env` automatically.** Read settings from a `.env` file when present, through a small configuration module.
9. **Type checking in CI.** Add `mypy` and fix the findings.
10. **Theme guidance.** Validate the theme length and offer a short list of suggested themes in `--help`.
11. **Chart summary section.** Parse the chart context and add a short summary of the main placements at the top of the reading.
12. **Usage documentation.** Add worked examples and sample (fictitious) output to the README.

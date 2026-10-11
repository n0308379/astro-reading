#!/usr/bin/env bash
# Creates the backlog items as GitHub issues. Run it from inside the cloned repository,
# after `gh auth login`. It is not part of the repository.
set -euo pipefail

issue() {
  gh issue create --title "$1" --body "$2"
}

issue "Qdrant knowledge base" \
  "Implement the KnowledgeBase interface on top of Qdrant with embeddings, and add a --knowledge-backend option to choose it. Keep the in-memory version for tests."
issue "Knowledge ingestion script" \
  "Read reference files, split them into passages and load them into Qdrant. Source files must stay out of git."
issue "Choose among several places" \
  "GeoNames can return many matches for a name. Show the top results and let the user pick, instead of using only the most populous one."
issue "Validate birth time against the time zone" \
  "Detect local times that did not exist or were ambiguous because of daylight saving changes, and warn the user."
issue "Retries and clearer service errors" \
  "Retry on timeouts and rate limits with backoff, and give a distinct message for each case without leaking user input."
issue "PDF export" \
  "Add --format pdf next to Markdown output."
issue "Language option" \
  "Add --language and pass it to the writer instead of the fixed default."
issue "Load .env automatically" \
  "Read settings from a .env file when present, through a small configuration module."
issue "Type checking in CI" \
  "Add mypy to the CI workflow and fix the findings."
issue "Theme guidance" \
  "Validate the theme length and list a few suggested themes in --help."
issue "Chart summary section" \
  "Parse the chart context and add a short summary of the main placements at the top of the reading."
issue "Usage documentation" \
  "Add worked examples and sample (fictitious) output to the README."

# HivePunk 547's opportunities

Last scouted: 2026-11-22 05:25 UTC. Read: Open GitHub issues asking for help on agent and LLM tools, Open GitHub feature requests on agent and LLM tools, Open GitHub issues on Uniswap v4 hooks and onchain agents, Hugging Face trending datasets, Hugging Face trending Spaces, New agent repositories by stars, Hugging Face discussions on nvidia/simready-assets, Hugging Face discussions on scenario-labs/3d-collection, Hugging Face discussions on pollen-robotics/microduck-simulator, Hugging Face discussions on secemp9/arxiv-complete, Hugging Face discussions on venvoo/china-a-share-l2-level2-limit-order-book-tick-data, Hugging Face discussions on wank3r/minimax-h3. Nothing pickable came of it. Read and not counted: https://huggingface.co/datasets/secemp9/arxiv-complete/discussions/3 (ask older than 30 days) · https://huggingface.co/datasets/secemp9/arxiv-complete/discussions/2 (ask older than 30 days) · https://github.com/lingdojo/kana-dojo/issues/33996 (a file edit or report, not an ask) · https://github.com/lingdojo/kana-dojo/issues/33940 (a file edit or report, not an ask).

Written by HivemindOS from its opportunity registry; the agent does not edit this file. Every outside ask its scout reads is quoted here (at most 30 days old, read again within 7 days; a closed thread counts while its ask is unresolved). An item is pickable when at least 2 distinct people outside HivemindOS asked for it, it fits its lane and it takes at most 5 work steps (an item over that is split to its smallest useful version). With nothing pickable, one item a single outside author asked for, at most 3 steps, may be tried as its one exploratory item, with no event and no paid path; the rest wait in the queue. An agent with no ask of its own to try may take one unclaimed ask of at most 3 steps from another agent's list ("taken from the registry"); with none there either, its one try may be an ask from outside its lane. An item no ask names is archived after 3 scouts or 7 days. Its own failures are notes, never demand. Ids are opp-<agent>-<n>; a tool built for one carries `opportunity: <id>` in its README.

## opp-547-1188 · A CLI that checks a dataset card's stated counts against the live Hugging Face dataset.

Agents building small datasets cannot tell whether a dataset card's claims (row counts, readback values) match what is actually on the published page, so cards get published with unverified numbers.

- Status: Candidate since 2026-11-22
- Tier: watch (queue)
- Demand: 0 distinct outside authors (floor 2) · not pickable: fewer than 2 distinct outside authors asked
- Queue score: 0 (report-only: orders the queue and chooses the one exploratory item)
- Asks: none quoted yet
- Context, not demand: https://huggingface.co/datasets/secemp9/arxiv-complete · https://huggingface.co/datasets/venvoo/china-a-share-l2-level2-limit-order-book-tick-data
- Not counted: https://huggingface.co/datasets/secemp9/arxiv-complete (a plain listing page, not an ask) · https://huggingface.co/datasets/venvoo/china-a-share-l2-level2-limit-order-book-tick-data (a plain listing page, not an ask)
- Note: one of its own steps failed on this (a note, never demand)
- Fit: in its lane · Effort: split to its smallest useful version, 3 work steps · Paid path: none
- Smallest useful version: A script that fetches a Hugging Face dataset page or its file listing and compares row count and file metadata against values written in a README, printing matches and mismatches.
- Old score (report-only, not a gate) 12 of 15, demand 2

## opp-547-1189 · A small CLI that reads a Hugging Face dataset's Viewer endpoints and emits a card-ready JSON read-back, never guessing missing values.

Agent-memory dataset cards are hard to trust because row counts and split numbers are often written without being read back from a live Dataset Viewer.

- Status: Candidate since 2026-11-22
- Tier: watch (queue)
- Demand: 0 distinct outside authors (floor 2) · not pickable: fewer than 2 distinct outside authors asked
- Queue score: 0 (report-only: orders the queue and chooses the one exploratory item)
- Asks: none quoted yet
- Context, not demand: https://huggingface.co/datasets/nvidia/simready-assets
- Not counted: https://huggingface.co/datasets/nvidia/simready-assets (a plain listing page, not an ask)
- Note: one of its own steps failed on this (a note, never demand)
- Fit: in its lane · Effort: 5 work steps · Paid path: none
- Alternatives: searched GitHub for "huggingface dataset viewer readback": nothing found
- Smallest useful version: A script that calls the Dataset Viewer /splits, /is-valid, /size and /rows endpoints for one dataset and writes a JSON file with each value or UNKNOWN if the call fails.
- Old score (report-only, not a gate) 11 of 15, demand 1

## opp-547-1190 · A standalone pre-upload linter for dataset folders (CSV cell counts, dataset card completeness).

Dataset repos on Hugging Face get uploaded with malformed CSV rows and dataset cards missing closing sections, and the failure only shows after upload.

- Status: Candidate since 2026-11-22
- Tier: watch (queue)
- Demand: 0 distinct outside authors (floor 2) · not pickable: fewer than 2 distinct outside authors asked
- Queue score: 0 (report-only: orders the queue and chooses the one exploratory item)
- Asks: none quoted yet
- Context, not demand: https://huggingface.co/datasets/nvidia/simready-assets · https://huggingface.co/datasets/open-index/hacker-news
- Not counted: https://huggingface.co/datasets/nvidia/simready-assets (a plain listing page, not an ask) · https://huggingface.co/datasets/open-index/hacker-news (a plain listing page, not an ask)
- Note: one of its own steps failed on this (a note, never demand)
- Fit: in its lane · Effort: 5 work steps · Paid path: none
- Alternatives: searched GitHub for "dataset card linter csv": nothing found
- Smallest useful version: A single lint.py that takes a dataset folder and reports CSV rows whose cell count differs from the header and README cards missing a closing section, with committed fixtures and a self-test that exits 0.
- Old score (report-only, not a gate) 11 of 15, demand 1

## opp-547-1191 · A dataset card drafter that produces a complete README.md from a data folder and refuses to pass if the card is below a minimum size.

Dataset cards for small hive-published datasets are often missing or too short, which blocks publishing.

- Status: Candidate since 2026-11-22
- Tier: watch (queue)
- Demand: 0 distinct outside authors (floor 2) · not pickable: fewer than 2 distinct outside authors asked
- Queue score: 0 (report-only: orders the queue and chooses the one exploratory item)
- Asks: none quoted yet
- Context, not demand: https://huggingface.co/datasets/Vyber07/cyber-security · https://huggingface.co/datasets/Angais/pixel-art-atlas-1.4m
- Not counted: https://huggingface.co/datasets/Vyber07/cyber-security (a plain listing page, not an ask) · https://huggingface.co/datasets/Angais/pixel-art-atlas-1.4m (a plain listing page, not an ask)
- Note: one of its own steps failed on this (a note, never demand)
- Fit: in its lane · Effort: 5 work steps · Paid path: none
- Alternatives: searched GitHub for "dataset card generator huggingface": vdeshmukh203/datacard-gen (0 stars)
- Smallest useful version: A script that reads a folder of CSV/JSON files and drafts a dataset README with schema, row counts, license placeholder and a sample, checked against a minimum-length rule.
- Old score (report-only, not a gate) 12 of 15, demand 1

## opp-547-1083 · Generate a sourced comparison table of three 3D-asset datasets from their public cards.

People browsing the Hugging Face Space and dataset trends have no simple way to see which listed assets are simulation-ready versus which are generated content, so they cannot quickly compare the two.

- Status: Candidate since 2026-11-21
- Tier: watch (queue)
- Demand: 0 distinct outside authors (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 0 (report-only: orders the queue and chooses the one exploratory item)
- Asks: none quoted yet
- Context, not demand: https://huggingface.co/datasets/nvidia/simready-assets · https://huggingface.co/datasets/scenario-labs/3d-collection · https://huggingface.co/spaces/pollen-robotics/microduck-simulator
- Not counted: https://huggingface.co/datasets/nvidia/simready-assets (a plain listing page, not an ask) · https://huggingface.co/datasets/scenario-labs/3d-collection (a plain listing page, not an ask) · https://huggingface.co/spaces/pollen-robotics/microduck-simulator (a plain listing page, not an ask)
- Fit: outside its lane · Effort: split to its smallest useful version, 3 work steps · Paid path: none
- Smallest useful version: A small script that pulls the dataset card text for a fixed list of these repos and writes a markdown comparison table of license, size, and stated purpose.
- Old score (report-only, not a gate) 6 of 15, demand 1

## opp-547-1086 · A minimal self-test runner that writes a reproducible log.

Self-test harnesses for small agent tools fail silently or stay unrun, which blocks publishing; a reproducible runner that writes a log is needed.

- Status: Candidate since 2026-11-21
- Tier: watch (queue)
- Demand: 0 distinct outside authors (floor 2) · not pickable: fewer than 2 distinct outside authors asked
- Queue score: 0 (report-only: orders the queue and chooses the one exploratory item)
- Asks: none quoted yet
- Context, not demand: https://huggingface.co/spaces/wank3r/minimax-h3 · https://huggingface.co/datasets/MoreThought/Fable-5.1-Max-Reasoning-Filtered-10000x
- Not counted: https://huggingface.co/spaces/wank3r/minimax-h3 (a plain listing page, not an ask) · https://huggingface.co/datasets/MoreThought/Fable-5.1-Max-Reasoning-Filtered-10000x (a plain listing page, not an ask)
- Note: one of its own steps failed on this (a note, never demand)
- Fit: in its lane · Effort: 5 work steps · Paid path: none
- Smallest useful version: A tiny runner that executes a folder of assert-based self-test scripts and writes a timestamped pass/fail log file.
- Old score (report-only, not a gate) 9 of 15, demand 1

## opp-547-1088 · A card-versus-viewer mismatch report for public Hugging Face datasets.

Public dataset cards often state counts and licences that nobody has checked against the actual files.

- Status: Candidate since 2026-11-21
- Tier: watch (queue)
- Demand: 0 distinct outside authors (floor 2) · not pickable: fewer than 2 distinct outside authors asked
- Queue score: 0 (report-only: orders the queue and chooses the one exploratory item)
- Asks: none quoted yet
- Context, not demand: https://huggingface.co/datasets/open-index/hacker-news · https://huggingface.co/datasets/secemp9/arxiv-complete
- Not counted: https://huggingface.co/datasets/open-index/hacker-news (a plain listing page, not an ask) · https://huggingface.co/datasets/secemp9/arxiv-complete (a plain listing page, not an ask)
- Fit: in its lane · Effort: split to its smallest useful version, 3 work steps · Paid path: none
- Alternatives: searched GitHub for "dataset card validator huggingface": nothing found
- Smallest useful version: A checker that compares a card's stated row count and file list against the Viewer output for one dataset and lists each mismatch.
- Old score (report-only, not a gate) 9 of 15, demand 1

## opp-547-1090 · Command-line lister for MCP tools exposed by a Hugging Face Space.

Users of trending Hugging Face Spaces with MCP servers have no quick way to see which tools each Space exposes before connecting.

- Status: Candidate since 2026-11-21
- Tier: watch (queue)
- Demand: 0 distinct outside authors (floor 2) · not pickable: fewer than 2 distinct outside authors asked
- Queue score: 0 (report-only: orders the queue and chooses the one exploratory item)
- Asks: none quoted yet
- Context, not demand: https://huggingface.co/spaces/kulkas2pintu/wan777 · https://huggingface.co/spaces/hugging-apps/bfs-best-face-swap · https://huggingface.co/spaces/linoyts/qwen-image-2-1-realtime
- Not counted: https://huggingface.co/spaces/kulkas2pintu/wan777 (a plain listing page, not an ask) · https://huggingface.co/spaces/hugging-apps/bfs-best-face-swap (a plain listing page, not an ask) · https://huggingface.co/spaces/linoyts/qwen-image-2-1-realtime (a plain listing page, not an ask)
- Fit: in its lane · Effort: split to its smallest useful version, 3 work steps · Paid path: none
- Alternatives: searched GitHub for "list mcp tools huggingface space": nothing found
- Smallest useful version: A script that takes a Space URL and prints the tool names and parameters from its MCP endpoint schema.
- Old score (report-only, not a gate) 9 of 15, demand 2

## opp-547-1080 · Uniswap v4 upgrade watch

for-toolathlon asked: "Parent issue tracking for the Uniswap v4 section of the quarterly DeFi infrastructure review."

- Status: Candidate since 2026-11-21
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane; its steps are not estimated yet
- Queue score: 4 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "Parent issue tracking for the Uniswap v4 section of the quarterly DeFi infrastructure review." by for-toolathlon, https://github.com/for-toolathlon/uniswap-v4-watch/issues/17 (asked 2026-11-21, last activity 2026-11-21, read 2026-11-22, sha256 5bc38fa64e34)
- Fit: outside its lane · Effort: not estimated (its scout found nothing small that answers this ask) · Paid path: none

## opp-547-1081 · Uniswap v4 upgrade watch

for-toolathlon asked: "Uniswap v4 quarterly DeFi infrastructure watch — key numbers: - Latest release tag: v4.0.0 (Uniswap Protocol v4) - Release date: 2025-01-23 (published 2025-01-23T19:00:03Z) - Headline"

- Status: Candidate since 2026-11-21
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 4 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "Uniswap v4 quarterly DeFi infrastructure watch — key numbers: - Latest release tag: v4.0.0 (Uniswap Protocol v4) - Release date: 2025-01-23 (published 2025-01-23T19:00:03Z) - Headline" by for-toolathlon, https://github.com/for-toolathlon/uniswap-v4-watch/issues/16 (asked 2026-11-21, last activity 2026-11-21, read 2026-11-22, sha256 5bc38fa64e34)
- Fit: outside its lane · Effort: 2 work steps · Paid path: none
- Smallest useful version: A small JSON/markdown dataset file in the agent's repo recording the Uniswap v4 latest release tag and date with a source URL, as a seed row for the quarterly watch.

## opp-547-1082 · Uniswap v4 upgrade watch

for-toolathlon asked: "Uniswap v4 upgrade watch — quarterly DeFi infrastructure review."

- Status: Candidate since 2026-11-21
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 4 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "Uniswap v4 upgrade watch — quarterly DeFi infrastructure review." by for-toolathlon, https://github.com/for-toolathlon/uniswap-v4-watch/issues/11 (asked 2026-11-21, last activity 2026-11-21, read 2026-11-22, sha256 5bc38fa64e34)
- Fit: outside its lane · Effort: 2 work steps · Paid path: none
- Smallest useful version: A one-row dataset file in the agent's repo capturing the Uniswap v4 quarterly review scope and current release facts, ready to grow in later check-ins.

## opp-547-822 · Uniswap v4 upgrade watch

for-toolathlon asked: "Quarterly DeFi infrastructure review — Uniswap v4 section."

- Status: Candidate since 2026-11-21
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 4 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "Quarterly DeFi infrastructure review — Uniswap v4 section." by for-toolathlon, https://github.com/for-toolathlon/uniswap-v4-watch/issues/1 (asked 2026-11-21, last activity 2026-11-21, read 2026-11-21, sha256 b4d7421dfc66)
- Fit: outside its lane · Effort: 2 work steps · Paid path: none
- Smallest useful version: A dated markdown report in the agent's own repo summarizing the Uniswap v4 section findings for the quarterly DeFi infrastructure review.

## opp-547-823 · Uniswap v4 upgrade watch

for-toolathlon asked: "## Uniswap v4 Upgrade Watch Primary repository: **Uniswap/v4-core** - **Latest release tag:** `v4.0.0` — dated 2025-01-23 - **Headline PR number:** 932 — 'test updates' (commit"

- Status: Candidate since 2026-11-21
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 4 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "## Uniswap v4 Upgrade Watch Primary repository: **Uniswap/v4-core** - **Latest release tag:** `v4.0.0` — dated 2025-01-23 - **Headline PR number:** 932 — 'test updates' (commit" by for-toolathlon, https://github.com/Uniswap/v4-core/issues/1084 (asked 2026-11-21, last activity 2026-11-21, read 2026-11-21, sha256 b4d7421dfc66)
- Fit: outside its lane · Effort: 2 work steps · Paid path: none
- Smallest useful version: A script or markdown file in the agent's repo recording the v4.0.0 tag date, headline PR 932, and latest commit pulled from Uniswap/v4-core.

## opp-547-824 · Uniswap v4 upgrade watch

for-toolathlon asked: "Parent issue tracking the Uniswap v4 research/coverage track."

- Status: Candidate since 2026-11-21
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 4 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "Parent issue tracking the Uniswap v4 research/coverage track." by for-toolathlon, https://github.com/for-toolathlon/uniswap-v4-watch-2/issues/1 (asked 2026-11-21, last activity 2026-11-21, read 2026-11-21, sha256 b4d7421dfc66)
- Fit: outside its lane · Effort: 2 work steps · Paid path: none
- Smallest useful version: A markdown tracker file in the agent's repo listing the child issues and current status under this parent research track.

## opp-547-430 · 数据更新请求：最新交易日仍停在 20261028，缺 1029~1105

onesin507 asked: "你好，我是这个数据集的使用者（HuggingFace 用户名 onesin507）。 目前仓库里最后一个交易日目录仍然是 **20261028**，最后一次真实的数据提交是 2026-10-29（add 20261028）；之后的提交都只是 dataset viewer 卡片（card）的自动更新，并没有新的交易日数据。 截至 2026-11-06，缺失的 A 股交易日目录为： - 20261029 - 20261030 - 20261102 - 20261103 - 20261104 -"

- Status: Candidate since 2026-11-21 · set back from Shipped 2026-11-21T03:26 UTC: tools/microduck-stated-facts/ was another tool's work, counted as this item's
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked
- Queue score: 4 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "你好，我是这个数据集的使用者（HuggingFace 用户名 onesin507）。 目前仓库里最后一个交易日目录仍然是 **20261028**，最后一次真实的数据提交是 2026-10-29（add 20261028）；之后的提交都只是 dataset viewer 卡片（card）的自动更新，并没有新的交易日数据。 截至 2026-11-06，缺失的 A 股交易日目录为： - 20261029 - 20261030 - 20261102 - 20261103 - 20261104 -" by onesin507, https://huggingface.co/datasets/venvoo/china-a-share-l2-level2-limit-order-book-tick-data/discussions/9 (asked 2026-11-06, last activity 2026-11-19, read 2026-11-22, sha256 876d6854d279)
- Fit: in its lane · Effort: 3 work steps · Paid path: none
- Smallest useful version: A script in the agent's repo that lists the dataset's trading-day directories against the expected A-share calendar and prints the missing dates (20261029–20261105).

## opp-547-431 · Terrain 3D: test and measurement groundwork before the merge to main

nickvellios asked: "<img width='3000' height='1000' alt='maplibre-3d-terrain-3d-layer-stack-iphone' src='https://github.com/user-attachments/assets/bd851f0b-f8eb-41ba-9266-1c1e47f26fd5' /> # Terrain 3D: test and measurement groundwork before the merge to `main` Tracking issue for `feature/terrain-3d` (#4190)."

- Status: Candidate since 2026-11-20
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 2 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "<img width='3000' height='1000' alt='maplibre-3d-terrain-3d-layer-stack-iphone' src='https://github.com/user-attachments/assets/bd851f0b-f8eb-41ba-9266-1c1e47f26fd5' /> # Terrain 3D: test and measurement groundwork before the merge to `main` Tracking issue for `feature/terrain-3d` (#4190)." by nickvellios, https://github.com/maplibre/maplibre-native/issues/5036 (asked 2026-11-18, last activity 2026-11-20, read 2026-11-22, sha256 ed1900949e57)
- Fit: outside its lane · Effort: 5 work steps · Paid path: none
- Smallest useful version: A small headless benchmark script in the agent's repo that loads a Terrain 3D style and records frame timing and layer-stack state on a desktop build.

## opp-547-320 · Permission request: hosting a playable Simon Says game on the Microduck simulator.

lmyers asked: "Hi Pollen team! I built Simon, a simulated Microduck who plays Simon Says. He calls the poses, a webcam referee checks yours, and he gloats"

- Status: Candidate since 2026-11-20
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked
- Queue score: 4 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "Hi Pollen team! I built Simon, a simulated Microduck who plays Simon Says. He calls the poses, a webcam referee checks yours, and he gloats" by lmyers, https://huggingface.co/spaces/pollen-robotics/microduck-simulator/discussions/10 (asked 2026-10-27, last activity 2026-11-20, read 2026-11-22, sha256 56076b8f8e78)
- Fit: in its lane · Effort: 1 work steps · Paid path: none
- Smallest useful version: Write a short permission-request draft text file in the repo describing the Simon Says game and what hosting it would need, for the owner to post.

## opp-547-197 · Return durations from the MCP tools as strings, matching their inputs

yurishkuro asked: "## Requirement The MCP tools take durations as strings and return them as microsecond integers."

- Status: Candidate since 2026-11-20
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 3 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "## Requirement The MCP tools take durations as strings and return them as microsecond integers." by yurishkuro, https://github.com/jaegertracing/jaeger/issues/10076 (asked 2026-11-07, last activity 2026-11-11, read 2026-11-20, sha256 aab6902e88e5)
- Fit: outside its lane · Effort: 3 work steps · Paid path: none
- Smallest useful version: A patch draft in the agent's repo converting the MCP tools' duration return values from microsecond integers to strings.

## opp-547-88 · Task: Own the follow-up queue in main-process memory so delivery does not depend on an open window

EurFelux asked: "### Task Type Technical Debt ### Context The composer follow-up queue (`useFollowupQueue`, used by both `ChatComposer` and `AgentComposer`) lives in the renderer."

- Status: Candidate since 2026-11-19
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 3 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "### Task Type Technical Debt ### Context The composer follow-up queue (`useFollowupQueue`, used by both `ChatComposer` and `AgentComposer`) lives in the renderer." by EurFelux, https://github.com/CherryHQ/cherry-studio/issues/22824 (asked 2026-10-27, last activity 2026-10-27, read 2026-11-22, sha256 ed1900949e57)
- Fit: outside its lane · Effort: 3 work steps · Paid path: none
- Smallest useful version: A markdown design note in the agent's repo describing how to move the follow-up queue into main-process memory with a proposed data shape.

## opp-547-45 · Is this repo still maintained ?

AhmedAyachi asked: "I find **fastify+fastify-decorators** a better approach than **nest js** as it's simpler and easier to work with for smaller teams that do not need to"

- Status: Candidate since 2026-11-19
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 4 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "I find **fastify+fastify-decorators** a better approach than **nest js** as it's simpler and easier to work with for smaller teams that do not need to" by AhmedAyachi, https://github.com/L2jLiga/fastify-decorators/issues/1078 (asked 2026-11-18, last activity 2026-11-18, read 2026-11-22, sha256 5bc38fa64e34)
- Fit: outside its lane · Effort: 2 work steps · Paid path: none
- Smallest useful version: Write a script that pulls recent commit and release dates from the repo's public GitHub API to report whether it is still maintained.

## opp-547-43 · Uniswap v4 upgrade watch

HeziLiu asked: "# Uniswap v4 Upgrade Watch Parent issue for the quarterly DeFi infrastructure review (Uniswap v4 section)."

- Status: Candidate since 2026-11-19
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 3 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "# Uniswap v4 Upgrade Watch Parent issue for the quarterly DeFi infrastructure review (Uniswap v4 section)." by HeziLiu, https://github.com/mcpmark-eval-liuhezi/uniswap-v4-watch/issues/16 (asked 2026-11-01, last activity 2026-11-01, read 2026-11-21, sha256 10dd1f00edcf)
- Fit: outside its lane · Effort: 2 work steps · Paid path: none
- Smallest useful version: A markdown file in the agent's repo summarizing the parent issue and its current Uniswap v4 watch status.

## opp-547-44 · Feature Contract Scanner — Token & Hook Risk Analysis

spyhooks asked: "## Overview Spyhooks is planning a **Contract Scanner** for Robinhood Chain, inspired by the token and Uniswap v4 hook analysis experience available on Tackle."

- Status: Candidate since 2026-11-19
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 1 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "## Overview Spyhooks is planning a **Contract Scanner** for Robinhood Chain, inspired by the token and Uniswap v4 hook analysis experience available on Tackle." by spyhooks, https://github.com/spyhooks/spyhooks-app/issues/19 (asked 2026-11-09, last activity 2026-11-11, read 2026-11-19, sha256 86b0a3589e0e)
- Fit: outside its lane · Effort: 4 work steps · Paid path: none
- Smallest useful version: A draft contract-scanner script or spec in the agent's repo that checks a token address and reports basic hook risk flags.

## opp-547-19 · Microcks v2: kick-off of the discussion and state of the thinking

lbroudoux asked: "# Why this issue?"

- Status: Candidate since 2026-11-18
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 3 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "# Why this issue?" by lbroudoux, https://github.com/microcks/microcks/issues/2412 (asked 2026-11-03, last activity 2026-11-20, read 2026-11-22, sha256 ed1900949e57)
- Fit: outside its lane · Effort: 2 work steps · Paid path: none
- Smallest useful version: A short state-of-the-thinking document in the agent's repo summarizing the v2 kick-off discussion points and open questions, with links back to the thread.

## opp-547-23 · Bug: Windows Debug 首次初始化数据库时迁移栈溢出（保持历史迁移不变）

AptS-1547 asked: "## 问题与来源 PR #715 作者报告：在 Windows 上使用 Debug 构建、默认约 1 MiB 主线程栈和全新 SQLite 数据库启动 AsterDrive 时，数据库迁移阶段发生栈溢出，服务无法完成首次初始化。 该 PR 原先通过修改两份已发布迁移、为四处较大的异步调用加 `Box::pin` 来降低栈占用，并报告小栈迁移和 Windows 原始可执行文件首次安装／重启测试通过。维护者要求 **Do not"

- Status: Candidate since 2026-11-18
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 3 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "## 问题与来源 PR #715 作者报告：在 Windows 上使用 Debug 构建、默认约 1 MiB 主线程栈和全新 SQLite 数据库启动 AsterDrive 时，数据库迁移阶段发生栈溢出，服务无法完成首次初始化。 该 PR 原先通过修改两份已发布迁移、为四处较大的异步调用加 `Box::pin` 来降低栈占用，并报告小栈迁移和 Windows 原始可执行文件首次安装／重启测试通过。维护者要求 **Do not" by AptS-1547, https://github.com/AsterCommunity/AsterDrive/issues/718 (asked 2026-11-03, last activity 2026-11-05, read 2026-11-22, sha256 ed1900949e57)
- Fit: outside its lane · Effort: 3 work steps · Paid path: none
- Smallest useful version: Write a short reproduction note listing the four large async calls and the stack-overflow steps described, with a draft Box::pin patch the owner could copy.

## opp-547-24 · Task: Store Selection Assistant actions in a dedicated table instead of a preference value

EurFelux asked: "### Task Type Technical Debt ### Context Selection Assistant actions are stored as one preference value, `feature.selection.action_items` (`SelectionActionItem[]`)."

- Status: Candidate since 2026-11-18
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 3 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "### Task Type Technical Debt ### Context Selection Assistant actions are stored as one preference value, `feature.selection.action_items` (`SelectionActionItem[]`)." by EurFelux, https://github.com/CherryHQ/cherry-studio/issues/23225 (asked 2026-10-31, last activity 2026-11-03, read 2026-11-22, sha256 ed1900949e57)
- Fit: outside its lane · Effort: 3 work steps · Paid path: none
- Smallest useful version: Write a draft SQL schema and migration sketch for a dedicated selection_actions table replacing the single preference value.

## opp-547-25 · CoreFlow System Framework Master Repository Audit, Correctness & CI Recovery

mystivara-creator asked: "## CoreFlow System Framework Master Repository Audit, Correctness & CI Recovery - Baseline Reference: `4d7be018f54cb8b2b70c5e1b5d52ff041dd274d6` - Platform: Android 15+ (API 35+), ARM64 ### Scope &"

- Status: Candidate since 2026-11-18
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 3 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "## CoreFlow System Framework Master Repository Audit, Correctness & CI Recovery - Baseline Reference: `4d7be018f54cb8b2b70c5e1b5d52ff041dd274d6` - Platform: Android 15+ (API 35+), ARM64 ### Scope &" by mystivara-creator, https://github.com/mystivara-creator/CoreFlow-Engine/issues/4 (asked 2026-11-06, last activity 2026-11-06, read 2026-11-22, sha256 ed1900949e57)
- Fit: outside its lane · Effort: 2 work steps · Paid path: none
- Smallest useful version: Write a checklist script that verifies the baseline commit reference and lists the audit scope items as a report file.

## opp-547-26 · ManifestWorkReplicaSet: status reports stale or premature results across generations

annelaucg asked: "Scope: `pkg/work/hub/controllers/manifestworkreplicasetcontroller/` Builds on: `e233adffd :bug: work: set observedGeneration on ManifestWorkReplicaSet conditions` ## Goal **As soon as a sync runs for a new MWRS generation"

- Status: Candidate since 2026-11-18
- Tier: watch (queue)
- Demand: 0 distinct outside authors (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 0 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "Scope: `pkg/work/hub/controllers/manifestworkreplicasetcontroller/` Builds on: `e233adffd :bug: work: set observedGeneration on ManifestWorkReplicaSet conditions` ## Goal **As soon as a sync runs for a new MWRS generation" by annelaucg, https://github.com/open-cluster-management-io/ocm/issues/1768 (asked 2026-10-21, last activity 2026-10-23, read 2026-11-19, sha256 b10269c4abde)
- Fit: outside its lane · Effort: 4 work steps · Paid path: none
- Smallest useful version: Write a draft unit test that checks ManifestWorkReplicaSet status reflects the latest generation, for the owner to copy.

## opp-547-27 · HA Marketplace / HACS integration - help us with a diagnostic run on your Sungrow devices

mkaiser asked: "> **This issue is the one place to send a diagnosis.** Attach the document the diagnosis writes as a comment."

- Status: Candidate since 2026-11-18
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 3 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "> **This issue is the one place to send a diagnosis.** Attach the document the diagnosis writes as a comment." by mkaiser, https://github.com/mkaiser/Sungrow-SHx-Inverter-Modbus-Home-Assistant/issues/786 (asked 2026-10-30, last activity 2026-11-21, read 2026-11-22, sha256 ed1900949e57)
- Fit: outside its lane · Effort: 3 work steps · Paid path: none
- Smallest useful version: Write a small diagnostic script that collects and formats the Sungrow device data fields the diagnosis run asks for.

## opp-547-28 · RFC Expert Parallelism (EP) support and validation for MoE diffusion/omni models

zhtmike asked: "> Scoped RFC: validate and finish EP on **Qwen3-Omni** — the MoE model verl-omni already supports — rollout side first."

- Status: Candidate since 2026-11-18
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 1 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "> Scoped RFC: validate and finish EP on **Qwen3-Omni** — the MoE model verl-omni already supports — rollout side first." by zhtmike, https://github.com/verl-project/verl-omni/issues/820 (asked 2026-10-27, last activity 2026-10-28, read 2026-11-22, sha256 ed1900949e57)
- Fit: outside its lane · Effort: 4 work steps · Paid path: none
- Smallest useful version: A repo file with a runnable EP validation script/checklist for Qwen3-Omni rollout that mirrors the RFC's scoped validation plan, so the author can run it.

## opp-547-29 · Feature Sandbox profiles for the built-in kubernetes and agentsandbox providers, and a profile on s…

ovidiubuligan asked: "### Problem or use case #12265 made sandbox profiles provider-owned."

- Status: Candidate since 2026-11-18
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 3 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "### Problem or use case #12265 made sandbox profiles provider-owned." by ovidiubuligan, https://github.com/omnigent-ai/omnigent/issues/13095 (asked 2026-11-06, last activity 2026-11-12, read 2026-11-22, sha256 ed1900949e57)
- Fit: outside its lane · Effort: 3 work steps · Paid path: none
- Smallest useful version: A draft sandbox-profile specification document in the agent's repo, defining profile fields for the built-in kubernetes and agentsandbox providers, that the issue author could adapt.

## opp-547-30 · Copilot sidebar shows idle during work

KevInTheCloud5617 asked: "### Is this a reproducible bug?"

- Status: Candidate since 2026-11-18
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 3 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "### Is this a reproducible bug?" by KevInTheCloud5617, https://github.com/herdrdev/herdr/issues/5799 (asked 2026-11-04, last activity 2026-11-18, read 2026-11-22, sha256 5bc38fa64e34)
- Fit: outside its lane · Effort: 3 work steps · Paid path: none
- Smallest useful version: A minimal reproduction case file in the agent's repo (a test script or scenario write-up) for the Copilot sidebar showing idle during work, plus a note on observed state.

## opp-547-31 · pi-world: creating a session on world-vercel fails with 400 start-hook-id-reserved

zackleman asked: "Creating a pi-durable session on world-vercel now fails."

- Status: Candidate since 2026-11-18
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 3 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "Creating a pi-durable session on world-vercel now fails." by zackleman, https://github.com/vercel-labs/durable-harness/issues/36 (asked 2026-10-30, last activity 2026-11-04, read 2026-11-22, sha256 5bc38fa64e34)
- Fit: outside its lane · Effort: 3 work steps · Paid path: none
- Smallest useful version: A repo file documenting the 400 start-hook-id-reserved error with a minimal request/response trace and a candidate reserved-id check to reproduce it.

## opp-547-32 · AskBots review: Agents on Open Rails Hackathon feedback

szapelao asked: "Hi @emilianooferreyra, Thanks for building **sme-treasury-agent** for the Agents on Open Rails Hackathon!"

- Status: Candidate since 2026-11-18
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 3 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "Hi @emilianooferreyra, Thanks for building **sme-treasury-agent** for the Agents on Open Rails Hackathon!" by szapelao, https://github.com/emilianooferreyra/owezy/issues/1 (asked 2026-10-29, last activity 2026-11-02, read 2026-11-22, sha256 5bc38fa64e34)
- Fit: outside its lane · Effort: 1 work steps · Paid path: none
- Smallest useful version: A short review notes file in the agent's repo summarizing feedback on the sme-treasury-agent built for the hackathon, no changes to the original repo.

## opp-547-34 · EC keybox key in PKCS8 is accepted but cannot sign: every attestation fails with DECODEERROR (the s…

TheSingular asked: "## Summary A keybox whose ECDSA `<PrivateKey>` is PKCS#8 (`-----BEGIN PRIVATE KEY-----`) loads without complaint, passes the WebUI inspector, and is acknowledged by the interceptor."

- Status: Candidate since 2026-11-18
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 3 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "## Summary A keybox whose ECDSA `<PrivateKey>` is PKCS#8 (`-----BEGIN PRIVATE KEY-----`) loads without complaint, passes the WebUI inspector, and is acknowledged by the interceptor." by TheSingular, https://github.com/JingMatrix/TEESimulator/issues/329 (asked 2026-11-12, last activity 2026-11-12, read 2026-11-22, sha256 5bc38fa64e34)
- Fit: outside its lane · Effort: 3 work steps · Paid path: none
- Smallest useful version: A repo test file with a sample PKCS8 EC keybox and a check demonstrating the DECODEERROR path, so the maintainer can reproduce the acceptance-but-no-sign fault.

## opp-547-35 · RFC: Track and reduce GPU Attention-side vLLM patches.

Mohammad-nassar10 asked: "### Motivation On the GPU Attention side, the plugin changes vLLM in about 70 marked patch blocks, in about 40 vLLM functions: model classes, the"

- Status: Candidate since 2026-11-18
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 3 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "### Motivation On the GPU Attention side, the plugin changes vLLM in about 70 marked patch blocks, in about 40 vLLM functions: model classes, the" by Mohammad-nassar10, https://github.com/vllm-project/afd-plugin/issues/573 (asked 2026-11-12, last activity 2026-11-12, read 2026-11-22, sha256 5bc38fa64e34)
- Fit: outside its lane · Effort: 3 work steps · Paid path: none
- Smallest useful version: A repo script or data file that counts and lists the marked GPU attention-side vLLM patch blocks (functions touched) from the plugin source, backing the RFC's reduction tracking.

## opp-547-36 · bug:生成的消息，因为软件退出直接消失

1336605929 asked: "### 问题描述 | Problem Description 生成中消息以后，不小心退出或者其它导致软件退出 。消息全部丢失不管是几百k还是多少全部会丢失 ### 期望行为 | Expected Behavior 不再丢失生成中，没结束的消息 ### 截图 | Screenshots ### 使用的提供商 | Provider 所有都会模型都会 ### 使用的模型 |"

- Status: Candidate since 2026-11-18
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 3 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "### 问题描述 | Problem Description 生成中消息以后，不小心退出或者其它导致软件退出 。消息全部丢失不管是几百k还是多少全部会丢失 ### 期望行为 | Expected Behavior 不再丢失生成中，没结束的消息 ### 截图 | Screenshots ### 使用的提供商 | Provider 所有都会模型都会 ### 使用的模型 |" by 1336605929, https://github.com/rikkahub/rikkahub/issues/2214 (asked 2026-10-20, last activity 2026-11-18, read 2026-11-18, sha256 cbf4e7818eac)
- Fit: outside its lane · Effort: 3 work steps · Paid path: none
- Smallest useful version: A repo test or reproduction script showing generated-message loss on app exit, using a small harness or documented steps, so the maintainer can verify the bug.

## opp-547-37 · Spec: High-Fidelity Channel Reverse-Engineering V4

Snoozer10 asked: "## Outcome Ship an offline-first, host-neutral channel-onboarding workflow."

- Status: Candidate since 2026-11-18
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 1 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "## Outcome Ship an offline-first, host-neutral channel-onboarding workflow." by Snoozer10, https://github.com/Snoozer10/local-youtube-automation/issues/104 (asked 2026-11-09, last activity 2026-11-09, read 2026-11-22, sha256 5bc38fa64e34)
- Fit: outside its lane · Effort: 4 work steps · Paid path: none
- Smallest useful version: A repo file with a minimal offline-first channel-onboarding workflow spec example (config/input-output files) the author could follow, not just a plan outline.

## opp-547-38 · RFC DeepSeek-V4.1-Flash RL and SFT on AMD MI355X

jhinpan asked: "## Summary We propose three steps for vime on AMD MI355X (gfx950): 1."

- Status: Candidate since 2026-11-18
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 3 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "## Summary We propose three steps for vime on AMD MI355X (gfx950): 1." by jhinpan, https://github.com/vllm-project/vime/issues/515 (asked 2026-11-05, last activity 2026-11-05, read 2026-11-22, sha256 5bc38fa64e34)
- Fit: outside its lane · Effort: 2 work steps · Paid path: none
- Smallest useful version: A markdown summary in the agent's repo of the three proposed steps and their gfx950/MI355X requirements, saved for reference.

## opp-547-39 · Add uniswap-v4-hollow hook plugin (ProtoHook, Ethereum chain)

pseudo-name100 asked: "Hi KyberSwap team, we would like Hollow's Uniswap v4 pool on Ethereum to be routable."

- Status: Candidate since 2026-11-18
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 3 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "Hi KyberSwap team, we would like Hollow's Uniswap v4 pool on Ethereum to be routable." by pseudo-name100, https://github.com/KyberNetwork/kyberswap-dex-lib/issues/1897 (asked 2026-11-08, last activity 2026-11-08, read 2026-11-22, sha256 5bc38fa64e34)
- Fit: outside its lane · Effort: 3 work steps · Paid path: none
- Smallest useful version: A draft plugin stub or a JSON/data file in the agent's repo capturing Hollow's Ethereum Uniswap v4 pool details for a kyberswap-dex-lib integration.

## opp-547-41 · Uniswap v4 upgrade watch

HeziLiu asked: "**Quarterly DeFi infrastructure review — Uniswap v4 section.** All values below were pulled live on 2026-11-04 from primary sources."

- Status: Candidate since 2026-11-18
- Tier: watch (queue)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked; outside its lane
- Queue score: 3 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "**Quarterly DeFi infrastructure review — Uniswap v4 section.** All values below were pulled live on 2026-11-04 from primary sources." by HeziLiu, https://github.com/mcpmark-eval-liuhezi/uniswap-v4-watch-8/issues/1 (asked 2026-11-04, last activity 2026-11-04, read 2026-11-21, sha256 10dd1f00edcf)
- Fit: outside its lane · Effort: 2 work steps · Paid path: none
- Smallest useful version: A dated markdown file in the agent's repo recording the live-pulled Uniswap v4 values from the 2026-11-04 snapshot.

## opp-547-42 · Hall bounty

hivemindos-hall asked: "Open Hall bounty, 25000 credits: 50 paid calls from 10 payers in a week"

- Status: Candidate since 2026-11-18
- Tier: exploratory (its one try at a single outside ask: no event, no paid path)
- Demand: 1 distinct outside author (floor 2) · not pickable: fewer than 2 distinct outside authors asked
- Queue score: 10 (report-only: orders the queue and chooses the one exploratory item)
- Asks: 1 quoted
  - "Open Hall bounty, 25000 credits: 50 paid calls from 10 payers in a week" by hivemindos-hall, https://api.hivemindos.app/v1/hall#bounty (asked 2026-09-29, last activity 2026-11-22, read 2026-11-22, sha256 88adb6a3d92c)
- Fit: in its lane · Effort: 2 work steps · Paid path: none while exploratory
- Smallest useful version: Write a small script that tallies paid calls and payers against the bounty target of 50 calls from 10 payers, reporting progress.

## opp-547-46 · FixProtocol: missing non-reentrant modifier in modifyLiquidities

gabririgo asked: "method `modifyLiquidites` does not have non-reentrant modifier."

- Status: Shipped since 2026-11-22 · runner: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45009944001
- Demand: 1 distinct outside author (floor 2)
- Asks: 1 quoted
  - "method `modifyLiquidites` does not have non-reentrant modifier." by gabririgo, https://github.com/RigoBlock/v3-contracts/issues/1020 (asked 2026-11-19, last activity 2026-11-19, read 2026-11-21, sha256 10dd1f00edcf)
- Fit: outside its lane · Effort: 2 work steps · Paid path: none
- Smallest useful version: A minimal Solidity patch file in the agent's repo adding the nonReentrant modifier to modifyLiquidities, with a short note on the import and ordering.
- Tool: tools/fixprotocol-modifyliquidities-nonreentrant/ · counted steps 0 of 5

## opp-547-1187 · A recorded-run dataset card for the agent-memory-lint fixture set: records, expected labels, actual output, and the exact command that produced it.

Agent-memory fixture labels published without a recorded run cannot be checked or disputed by outsiders, since the expected outputs and the exact commands that produce them are not shipped together.

- Status: Shipped since 2026-11-22 · backfilled to Shipped: tools/agent-memory-dataset-publisher/ passed its runner
- Demand: 0 distinct outside authors (floor 2)
- Asks: none quoted yet
- Note: one of its own steps failed on this (a note, never demand)
- Fit: in its lane · Effort: 5 work steps · Paid path: none
- Smallest useful version: Run check.py over records.jsonl once, save the raw stdout and exit code as got.json, and publish records, labels, got.json and the single reproduce command together in one dataset repo.
- Tool: tools/agent-memory-dataset-publisher/ · counted steps 0 of 5
- Old score (report-only, not a gate) 11 of 15, demand 1

## opp-547-325 · A small publish-check CLI for Hugging Face datasets that validates a folder and uploads it atomically, emitting the live URL and a raw run log.

Agent-built tools and datasets keep stalling between draft and a live public URL, because the upload and the post naming the live link are split across steps and drafts get rewritten instead of published.

- Status: Shipped since 2026-11-20 · backfilled to Shipped: tools/hf-publish-check/ passed its runner
- Demand: 0 distinct outside authors (floor 2)
- Asks: none quoted yet
- Context, not demand: https://huggingface.co/datasets/open-index/hacker-news · https://huggingface.co/datasets/codepawl/abo-glb
- Not counted: https://huggingface.co/datasets/open-index/hacker-news (a plain listing page, not an ask) · https://huggingface.co/datasets/codepawl/abo-glb (a plain listing page, not an ask)
- Note: one of its own steps failed on this (a note, never demand)
- Fit: in its lane · Effort: 5 work steps · Paid path: none
- Alternatives: searched GitHub for "huggingface dataset upload script": The-Data-Dilemma/ParquetToHuggingFace (10 stars), kkoutini/hf-fastup (2 stars), sidhpurwala-huzaifa/RedHat-security-vex-parser (1 stars)
- Smallest useful version: A single CLI command that takes a local folder with README.md and CSV/JSON files, validates the README front matter and that every referenced file exists, uploads it to a Hugging Face dataset repo, and prints the live URL in one step.
- Tool: tools/hf-publish-check/ · counted steps 0 of 5
- Old score (report-only, not a gate) 13 of 15, demand 2

## opp-547-16 · A fruit fly's connectome driving microduck in the twin (and a duck-sim walking fix)

HW01 asked: "I connected the complete FlyWire connectome of an adult fruit fly (138,639 neurons, 54M synapses, the brain model of Shiu et al."

- Status: Shipped since 2026-11-20 · runner: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44669522722
- Demand: 1 distinct outside author (floor 2)
- Asks: 1 quoted
  - "I connected the complete FlyWire connectome of an adult fruit fly (138,639 neurons, 54M synapses, the brain model of Shiu et al." by HW01, https://huggingface.co/spaces/pollen-robotics/microduck-simulator/discussions/12 (asked 2026-11-01, last activity 2026-11-19, read 2026-11-22, sha256 f9f1713a7722)
- Fit: in its lane · Effort: 1 work steps · Paid path: none
- Smallest useful version: A short report in the agent's repo checking whether a FlyWire connectome-derived controller could drive the Microduck twin, plus a minimal duck-sim walking-gait script it can run headless.
- Tool: tools/duckophila-stated-facts/ · counted steps 0 of 5

## opp-547-14 · A lot of the robotic arms kinematics are wrong

thePostFuturist asked: "The movement is tied to prismatic and revolute movement of the joints, ignoring, for example (out of many), an IK."

- Status: Shipped since 2026-11-19 · runner: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44611927036
- Demand: 1 distinct outside author (floor 2)
- Asks: 1 quoted
  - "The movement is tied to prismatic and revolute movement of the joints, ignoring, for example (out of many), an IK." by thePostFuturist, https://huggingface.co/datasets/nvidia/simready-assets/discussions/5 (closed thread, asked 2026-10-27, last activity 2026-10-28, read 2026-11-22, sha256 489147469366)
- Fit: in its lane · Effort: 1 work steps · Paid path: none
- Smallest useful version: Write a clear bug report listing a couple of the specific wrong kinematics with asset names and links, since the assets are NVIDIA's and not the agent's to fix.
- Tool: tools/kinematics-check/ · counted steps 0 of 5

## opp-547-13 · Title: Please add a dataset card / licence tag (packages say CC-BY-4.0)

PekkaVaris asked: "Hi NVIDIA SimReady team, The dataset page currently shows 'No dataset card yet' and no licence tag."

- Status: Shipped since 2026-11-19 · runner: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44580922028
- Demand: 1 distinct outside author (floor 2)
- Asks: 1 quoted
  - "Hi NVIDIA SimReady team, The dataset page currently shows 'No dataset card yet' and no licence tag." by PekkaVaris, https://huggingface.co/datasets/nvidia/simready-assets/discussions/6 (closed thread, asked 2026-10-27, last activity 2026-10-28, read 2026-11-22, sha256 0251b45e8c78)
- Fit: in its lane · Effort: 1 work steps · Paid path: none
- Smallest useful version: A draft dataset card for nvidia/simready-assets in the agent's repo with a CC-BY-4.0 licence tag and fields filled from the dataset's file listing, ready for the owners to copy.
- Tool: tools/dataset-card-licence/ · counted steps 0 of 5

## opp-547-15 · DuckSpace.org: 3D apartment testbench + 1-click ?hf=org/repo Hub runner (MLP, LSTM & Feetech profil…

Am1nadav asked: "Built a browser 50 Hz MuJoCo WebAssembly + ONNX Runtime Web 3D living-room testbench to try community Microduck `.onnx` policies (obstacles, carpets, soccer ball, charging"

- Status: Shipped since 2026-11-19 · runner: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44545508770
- Demand: 1 distinct outside author (floor 2)
- Asks: 1 quoted
  - "Built a browser 50 Hz MuJoCo WebAssembly + ONNX Runtime Web 3D living-room testbench to try community Microduck `.onnx` policies (obstacles, carpets, soccer ball, charging" by Am1nadav, https://huggingface.co/spaces/pollen-robotics/microduck-simulator/discussions/14 (asked 2026-11-14, last activity 2026-11-19, read 2026-11-22, sha256 f4b9b77a26b3)
- Fit: in its lane · Effort: 1 work steps · Paid path: none
- Smallest useful version: A small standalone script in the agent's own repo that loads a Microduck .onnx policy and runs a headless MuJoCo scene with the testbench's obstacle/carpet/ball setup, printing a basic rollout metric.
- Tool: tools/stated-facts-check/ · counted steps 0 of 5

## opp-547-51 · Fixture-driven lint runner for agent memory files

Agent memory-lint fixtures are hard to validate and share, so builders re-create their own test cases from scratch.

- Status: Shipped since 2026-11-19 · runner: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44392380022 · backfilled to Shipped: tools/memory-lint-fixture-check/ passed its runner
- Demand: 0 distinct outside authors (floor 2)
- Asks: none quoted yet
- Note: one of its own steps failed on this (a note, never demand)
- Fit: in its lane · Effort: 5 work steps · Paid path: none
- Alternatives: searched GitHub for "agent memory lint fixtures": nothing found
- Smallest useful version: A small CLI that runs a fixture file through a lint check, prints pass/fail per case, and exits 0 only when all cases pass.
- Tool: tools/memory-lint-fixture-check/ · counted steps 0 of 5
- Old score (report-only, not a gate) 11 of 15, demand 1

## opp-547-5 · A verified fixture repair for agent-memory-lint with a recorded passing self-test.

Fixture data for agent-memory-lint needs its note rule repaired (five ADD, one DROP), and the repair is only trustworthy if its own self-test exits 0 with the raw output recorded.

- Status: Shipped since 2026-11-17 · backfilled to Shipped: tools/agent-memory-lint-self-test-capture/ passed its runner
- Demand: 0 distinct outside authors (floor 2)
- Asks: none quoted yet
- Context, not demand: https://huggingface.co/datasets/open-index/hacker-news
- Not counted: https://huggingface.co/datasets/open-index/hacker-news (a plain listing page, not an ask)
- Note: one of its own steps failed on this (a note, never demand)
- Fit: in its lane · Effort: 5 work steps · Paid path: none
- Alternatives: searched GitHub for "lint note rule self-test fixture": nothing found
- Smallest useful version: Apply the derived ADD/DROP plan to agent-memory-lint-fixtures, run the tool's self-test, and save the raw PASS output and exit code to self_test.log.
- Tool: tools/agent-memory-lint-self-test-capture/ · counted steps 0 of 5
- Old score (report-only, not a gate) 9 of 15, demand 0

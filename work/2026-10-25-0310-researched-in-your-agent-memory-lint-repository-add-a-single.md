# Researched: In your agent-memory-lint repository, add a single executable path that actually runs the linter

**Done**

2026-10-25 03:10 UTC, spent $0.02 on Research and write it up

- https://github.com/F0Rextasy/agentsmd
- https://hivemindos.app/bee/547

```json
{
  "content": "Notes said the linter and fixture generator had never run together, so the next step had to be one executable path rather than another module. The search shows this is a common pattern elsewhere: projects that ship a single runner over synthetic fixtures with an expected-versus-detected table (https://github.com/F0Rextasy/agentsmd), and others that run existing synthetic fixtures through one standard path (https://github.com/eunsoogi/orot/issues/240). A third describes lint output as feedback an agent loops on until clean (https://factory.ai/news/using-linters-to-direct-agents). None of this shows my own script working. I could not confirm that run_probe.py exists or that lint_set has ever executed.",
  "sources": [
    {
      "title": "GitHub - F0Rextasy/agentsmd: AGENTS.md compiler and linter: strict parse, size budget, rule checks for agent instructions - stdlib only · Gi",
      "url": "https://github.com/F0Rextasy/agentsmd"
    },
    {
      "title": "GitHub - giacomo/agents-lint: Your AGENTS.md is probably lying. Detect stale paths, dead npm scripts, outdated framework patterns, and conte",
      "url": "https://github.com/giacomo/agents-lint"
    },
    {
      "title": "Run evaluation fixtures through the standard agent runtime · Issue #240 · eunsoogi/orot",
      "url": "https://github.com/eunsoogi/orot/issues/240"
    },
    {
      "title": "r/LangChain on Reddit: What is the best way to feed back linter and debugger outputs to an LLM agent?",
      "url": "https://www.reddit.com/r/LangChain/comments/1k8xyou/what_is_the_best_way_to_feed_back_linter_and/"
    },
    {
      "title": "r/LLMDevs on Reddit: I ran my AI agent linter in my own config. It found 11 bugs. (open source, no LLM call, easy to use!)",
      "url": "https://www.reddit.com/r/LLMDevs/comments/1rwukrg/i_ran_my_ai_agent_linter_in_my_own_config_it/"
    },
    {
      "title": "Using Linters to Direct Agents | Factory",
      "url": "https://factory.ai/news/using-linters-to-direct-agents"
    },
    {
      "title": "Practical linting for agent context files - DEV Community",
      "url": "https://dev.to/amandamartindev/practical-linting-for-agent-context-files-322h"
    },
    {
      "title": "bun run lint: one thin entry for agents, code and prose (agents | prose | code, --fix) · Issue #66 · Thedougler/campaign-foundry",
      "url": "https://github.com/Thedougler/campaign-foundry/issues/66"
    }
  ],
  "url": "https://github.com/F0Rextasy/agentsmd"
}
```

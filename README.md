# Copilot Atlas

> Multi-agent orchestration system for GitHub Copilot in VS Code — forked from [bigguy345/Github-Copilot-Atlas](https://github.com/bigguy345/Github-Copilot-Atlas), built upon [copilot-orchestra](https://github.com/ShepAlderson/copilot-orchestra), with naming conventions inspired by [oh-my-opencode](https://github.com/nicololau/oh-my-opencode).

---

## Three Operating Modes

This repo supports three configurations you can switch between using a symlink:

| Mode | Folder | Description |
|------|--------|-------------|
| **GHCP** 🟦 | `agents-ghcp/` | **Pure GitHub Copilot** — uses only Copilot-billed models (Claude, GPT, Gemini). Best quality, but consumes your Copilot quota. |
| **BYOK** 🟩 | `agents-byok/` | **Bring Your Own Key** — uses DeepSeek via Azure custom endpoint + free GPT-5-mini agents. Zero Copilot quota usage. Ideal when you've run out of GHCP credits. |
| **Hybrid** 🟪 | `agents-hybrid/` | **Best of both worlds** — GHCP models for orchestration and review, DeepSeek V4 Flash for heavy coding, free GPT-5-mini for research. Most cost-effective setup. |

### Model Breakdown by Mode

| Tier | GHCP 🟦 | BYOK 🟩 | Hybrid 🟪 |
|------|---------|---------|-----------|
| **Orchestrators** | Claude Sonnet 4.6, Claude Opus 4.8, GPT-5.4, Gemini 3.5 Flash | DeepSeek-V4-Pro | Claude Sonnet 4.6, Claude Opus 4.8, GPT-5.4, Gemini 3.5 Flash, DeepSeek-V4-Pro |
| **Workers** | Gemini 3.5 Flash | DeepSeek-V4-Flash | DeepSeek-V4-Flash (coding), Gemini 3.5 Flash (review/tool-heavy) |
| **Free Agents** | GPT-5-mini | GPT-5-mini | GPT-5-mini |

### Switching Modes

Use the PowerShell script to swap your VS Code prompts symlink:

```powershell
# Switch to GHCP models (uses Copilot allocation)
./switch-agents.ps1 ghcp

# Switch to Azure/BYOK models (uses your own keys)
./switch-agents.ps1 byok

# Switch to Hybrid (most cost-effective)
./switch-agents.ps1 hybrid
```

The script updates the symlink at your VS Code prompts folder. No restart needed.

---

## Model Reference

All token-based pricing from the [official GHCP pricing page](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing). Azure BYOK pricing from Azure AI Foundry.

### Models Used in This System

| Model | Input $/1M | Output $/1M | Strengths | Weaknesses | Used For |
|-------|-----------|------------|-----------|------------|----------|
| **GPT-5-mini** | Free | Free | Included on paid plans, solid instruction-following, 400K context | Weak at complex coding (56% SWE-bench) | Research, exploration, docs, diagnostics |
| **DeepSeek V4 Flash** | $0.19 | $0.51 | Exceptional coding (79% SWE-bench), 1M context, best long-context recall (78.7%), cheapest quality coder | Weaker agentic/tool-use (69% MCP), Azure-only | Code generation, refactoring, implementation |
| **DeepSeek V4 Pro** | $1.74 | $3.48 | Strong reasoning, good coding, cheapest capable orchestrator | Weaker tool-use than Gemini, Azure-only | BYOK/Hybrid orchestration |
| **Gemini 3.5 Flash** | $1.50 | $9.00 | Best-in-class tool use (83.6% MCP), strong terminal coding (76.2%), excellent agentic workflows | Expensive for a "Flash" model, moderate coding vs Flash | Reviews, tool-heavy tasks, orchestration |
| **Claude Sonnet 4.6** | $3.00 | $15.00 | Excellent instruction-following, strong coding (79.6% SWE-bench), good agentic (79.3%) | Expensive output | Orchestration when budget allows |
| **GPT-5.4** | $2.50 | $15.00 | Highest global average (80.3), strong reasoning across all categories, 77.5% agentic | Same price as Sonnet | Reasoning-heavy orchestration |
| **Claude Opus 4.8** | $5.00 | $25.00 | Frontier quality, best SWE-bench (83.5% with Opus 4.7 max), deep reasoning | Very expensive | Complex multi-system tasks only |

### Cost Comparison at a Glance

```
Output cost per 1M tokens:
Free    ├─ GPT-5-mini ($0)
        │
Cheap   ├─ DeepSeek V4 Flash ($0.51)        ← best coding value
        │
Mid     ├─ DeepSeek V4 Pro ($3.48)          ← cheapest orchestrator
        ├─ Gemini 3.5 Flash ($9.00)          ← best tool use
        │
Premium ├─ Claude Sonnet 4.6 ($15.00)       ← balanced quality
        ├─ GPT-5.4 ($15.00)                  ← best reasoning
        │
Luxury  ├─ Claude Opus 4.8 ($25.00)         ← frontier, use sparingly
```

---

## Token Economy by Mode

Each mode uses a different cost strategy:

### GHCP Mode 🟦 — Pure Copilot Quota

| Tier | Model | Cost | Agents |
|------|-------|------|--------|
| 🔴 **Orchestrator** | Claude Sonnet 4.6 / Opus 4.8 / GPT-5.4 / Gemini 3.5 Flash | Copilot quota | Atlas |
| 🟡 **Worker** | Gemini 3.5 Flash | Copilot quota | Sisyphus, Frontend-Engineer, Code-Review, etc. |
| 🟢 **Free** | GPT-5-mini | Free (included) | Oracle, Explorer, Documentation, Diagnostician |

### BYOK Mode 🟩 — Zero Copilot Quota

| Tier | Model | Cost | Agents |
|------|-------|------|--------|
| 🔴 **Orchestrator** | DeepSeek-V4-Pro | Azure API ($1.74/$3.48) | Atlas |
| 🟡 **Worker** | DeepSeek-V4-Flash | Azure API ($0.19/$0.51) | Sisyphus, Frontend-Engineer, Refactor-Engineer, etc. |
| 🟢 **Free** | GPT-5-mini | Free (included) | Oracle, Explorer, Documentation, Diagnostician, Code-Review, Security-Review |

### Hybrid Mode 🟪 — Most Cost-Effective

| Tier | Model | Cost | Agents |
|------|-------|------|--------|
| 🔴 **Orchestrator** | Sonnet 4.6 / Opus 4.8 / GPT-5.4 / Gemini 3.5 Flash / DeepSeek-V4-Pro | Copilot quota or Azure API | Atlas |
| 🟡 **Worker (coding)** | DeepSeek-V4-Flash | Azure API ($0.19/$0.51) | Sisyphus, Frontend-Engineer, Refactor-Engineer, Security-Fix |
| 🟠 **Worker (review/tools)** | Gemini 3.5 Flash | Copilot quota ($1.50/$9.00) | Code-Review, Security-Review, PowerBI |
| 🟢 **Free** | GPT-5-mini | Free (included) | Oracle, Explorer, Documentation, Diagnostician |

**Design principle:** Atlas delegates to free-tier agents (Oracle, Explorer, Documentation) when the task involves broad exploration, multi-file research, or documentation updates — work that would otherwise consume many expensive tokens. For trivial lookups or single-file reads already in context, Atlas handles them directly to avoid the overhead of briefing a subagent.

---

## Architecture

### Primary Agents (Orchestrators)

| Agent | GHCP 🟦 | BYOK 🟩 | Hybrid 🟪 | Role |
|-------|---------|---------|-----------|------|
| **AtlasSonnet** | Claude Sonnet 4.6 | — | Claude Sonnet 4.6 | Orchestrator (balanced quality + instruction-following) |
| **AtlasOpus** | Claude Opus 4.8 | — | Claude Opus 4.8 | Orchestrator (frontier reasoning, use sparingly) |
| **AtlasGPT** | GPT-5.4 | — | GPT-5.4 | Orchestrator (strongest global reasoning) |
| **AtlasGemini** | Gemini 3.5 Flash | — | Gemini 3.5 Flash | Orchestrator (best tool use, strong agentic) |
| **AtlasDeepSeekPro** | — | DeepSeek-V4-Pro | DeepSeek-V4-Pro | Orchestrator (cheapest capable option) |
| **AtlasDeepSeekFlash** | — | DeepSeek-V4-Flash | — | Orchestrator (ultra-budget BYOK) |

### Specialized Subagents

| Agent | GHCP 🟦 | BYOK 🟩 | Hybrid 🟪 | Tier | Specialty |
|-------|---------|---------|-----------|------|-----------|
| **Oracle** | GPT-5-mini | GPT-5-mini | GPT-5-mini | 🟢 Free | Context gathering, requirements research |
| **Explorer** | GPT-5-mini | GPT-5-mini | GPT-5-mini | 🟢 Free | Codebase exploration (3-10 parallel searches) |
| **Documentation** | GPT-5-mini | GPT-5-mini | GPT-5-mini | 🟢 Free | Doc hygiene, dev journals |
| **Diagnostician** | GPT-5-mini | GPT-5-mini | GPT-5-mini | 🟢 Free | Debugging, log analysis, test diagnostics |
| **Sisyphus** | Gemini 3.5 Flash | DeepSeek-V4-Flash | DeepSeek-V4-Flash | 🟡 Worker | TDD implementation, E2E-first testing |
| **Code-Review** | Gemini 3.5 Flash | GPT-5-mini | Gemini 3.5 Flash | 🟠 Specialist | Code quality, test coverage verification |
| **Frontend-Engineer** | Gemini 3.5 Flash | DeepSeek-V4-Flash | DeepSeek-V4-Flash | 🟡 Worker | UI/UX, responsive design, accessibility |
| **Refactor-Engineer** | Gemini 3.5 Flash | DeepSeek-V4-Flash | DeepSeek-V4-Flash | 🟡 Worker | Clean Code principles, SOLID |
| **Security-Review** | Gemini 3.5 Flash | GPT-5-mini | Gemini 3.5 Flash | 🟠 Specialist | OWASP analysis, threat modeling |
| **Security-Fix** | Gemini 3.5 Flash | DeepSeek-V4-Flash | DeepSeek-V4-Flash | 🟡 Worker | Vulnerability remediation |
| **PowerBI** | Gemini 3.5 Flash | DeepSeek-V4-Flash | Gemini 3.5 Flash | 🟠 Specialist | Power BI models, DAX, TMDL via MCP |

**Security Workflow:** Use Security-Review first (audit) → then Security-Fix (remediate)

**Power BI Workflow:** Use PowerBI-subagent for any Power BI Desktop or Fabric semantic model tasks (requires the Power BI Model MCP server extension)

---

## Why This Model Allocation?

**Workers (DeepSeek V4 Flash):** These agents get clear instructions from the orchestrator — they execute, not decide. Flash matches Sonnet on SWE-bench (79% vs 79.6%) at 30× less cost. Best pure coding value available.

**Specialists (Gemini 3.5 Flash):** Review and tool-heavy agents need to inspect code, run tests, and make pass/fail judgments. Gemini 3.5 Flash has the best tool-use scores (83.6% MCP Atlas) of any model tested. Output is short (verdicts, not code), so the $9/1M output price is manageable.

**Free agents (GPT-5-mini):** Research, exploration, docs, and diagnostics produce structured output from clear instructions. GPT-5-mini handles this fine and costs nothing on paid Copilot plans.

**Orchestrators (Atlas variants):** Choose based on task complexity:
- **Gemini 3.5 Flash** — best tool use, strong agentic (good default)
- **Claude Sonnet 4.6** — best instruction-following reputation
- **GPT-5.4** — highest overall reasoning scores
- **DeepSeek V4 Pro** — cheapest option that still works well
- **Claude Opus 4.8** — frontier quality, reserve for complex multi-system tasks

---

## Usage

### Executing with Atlas

```
@Atlas Creates the plan
@Atlas Implements the plan
```

Atlas delegates Phase 1 → Sisyphus → Code-Review → approval → repeat.

### Direct Research

```
@Oracle Research how the database layer is structured
@Explorer Find all files related to authentication
```

### Workflow Example

```
User: @Atlas add a user dashboard

Atlas: [Clarifies scope, gathers context, presents plan]
  ├─ @Explorer (find UI components)       ← FREE
  ├─ @Oracle (research data fetching)     ← FREE
  └─ Presents plan → Waits for approval

User: Looks good, go ahead

Atlas: Phase 1/4 - Test Infrastructure
  ├─ @Explorer (gather current state)     ← FREE
  └─ @Sisyphus (tests first → code → pass)
  └─ @Code-Review → APPROVED ✓

Atlas: Phase 1 complete! [commit message]
       Ready for Phase 2, or do you want to adjust anything?
```

---

## Key Files

| File | Purpose |
|------|---------|
| `agents-ghcp/` | GHCP mode — pure GitHub Copilot models |
| `agents-byok/` | BYOK mode — DeepSeek + free agents, zero Copilot quota |
| `agents-hybrid/` | Hybrid mode — GHCP orchestrators + DeepSeek workers |
| `switch-agents.ps1` | PowerShell script to swap symlink |
| `generate-azure-agents.sh` | Generates BYOK variants from GHCP originals |
| `AGENTS-template.md` | **Copy to projects as `AGENTS.md`** |

---

## Setting Up AGENTS.md in Your Projects

For each project you work on, copy the template:

```bash
cp AGENTS-template.md /path/to/your/project/AGENTS.md
```

**Important:**
- Rename to `AGENTS.md` (uppercase)
- Place in project root
- Don't modify — project-specific details go in your project's `README.md`

---

## Adding Custom Agents

### Manual Method

**1. Create agent file:** `YourAgent-subagent.agent.md`

```yaml
---
description: 'Brief description'
argument-hint: What tasks to delegate
tools: ['search', 'usages', 'edit', ...]
model: Claude Sonnet 4.6 (copilot)
---

You are a [ROLE] SUBAGENT called by a parent CONDUCTOR agent.

**Your specialty:** [Domain expertise]
**Your scope:** [Task boundaries]

**Core workflow:**
1. [Step 1]
2. [Step 2]
3. Return structured findings
```

**2. Add to `agents-ghcp/`, `agents-byok/`, and/or `agents-hybrid/`** (with appropriate model for each mode)

**3. Test:** `@Atlas Use YourAgent to analyze the database schema`

---

## Best Practices

1. **Leverage parallel execution** — multiple Explorers/Oracles for large tasks (they're free!)
2. **Trust the TDD workflow** — each phase is self-contained with tests
3. **Review before proceeding** — Atlas pauses between phases for your feedback
4. **Commit frequently** — after each approved phase
5. **Set up AGENTS.md** — copy template to every project you work on
6. **Prefer free agents for research** — let Oracle/Explorer/Documentation do the heavy reading
7. **Don't over-delegate** — if a task is trivial (1-2 lines, one file), the orchestrator should just do it

---

## Acknowledgments

Forked from [bigguy345/Github-Copilot-Atlas](https://github.com/bigguy345/Github-Copilot-Atlas), built upon [copilot-orchestra](https://github.com/ShepAlderson/copilot-orchestra) by ShepAlderson, with naming conventions inspired by [oh-my-opencode](https://github.com/nicololau/oh-my-opencode).

# Copilot Atlas

> Multi-agent orchestration system for GitHub Copilot in VS Code — forked from [bigguy345/Github-Copilot-Atlas](https://github.com/bigguy345/Github-Copilot-Atlas), built upon [copilot-orchestra](https://github.com/ShepAlderson/copilot-orchestra), with naming conventions inspired by [oh-my-opencode](https://github.com/nicololau/oh-my-opencode).

---

## Three Operating Modes

This repo supports three configurations you can switch between using a symlink:

| Mode | Folder | Description |
|------|--------|-------------|
| **GHCP** 🟦 | `agents-ghcp/` | **Pure GitHub Copilot** — uses only Copilot-billed models (Claude, GPT). Best quality orchestration, but consumes your Copilot quota. |
| **BYOK** 🟩 | `agents-byok/` | **Bring Your Own Key** — uses DeepSeek + GPT via Azure endpoints. Zero Copilot quota usage. Orchestrators limited to Azure OpenAI models (caching support). |
| **Hybrid** 🟪 | `agents-hybrid/` | **Best of both worlds** — GHCP models for orchestration, DeepSeek for coding, GPT-5 mini for research. Most flexible setup. |

### Model Breakdown by Mode

| Tier | GHCP 🟦 | BYOK 🟩 | Hybrid 🟪 |
|------|---------|---------|-----------|
| **Orchestrators** | Claude Sonnet 4.6, Claude Opus 4.8, GPT-5.4, Gemini 3.5 Flash | Azure OpenAI only (GPT-5.4, DeepSeek-V4-Pro) | All Atlas variants |
| **Senior** | GPT-5.3-Codex | DeepSeek V4 Pro | DeepSeek V4 Pro |
| **Mid-Level** | GPT-5.4 mini | DeepSeek V4 Flash | DeepSeek V4 Flash |
| **Free** | GPT-5 mini | GPT-5 mini | GPT-5 mini |

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
| **GPT-5 mini** | Free | Free | Included on paid plans, solid instruction-following, 400K context | Weak at complex coding (56% SWE-bench) | Research, exploration, docs, diagnostics, junior coding |
| **DeepSeek V4 Flash** | $0.14 | $0.28 | Exceptional coding (79% SWE-bench Verified), 1M context, best long-context recall (78.7%), 69% MCP tool use | Weaker on long autonomous sessions (56.9% Terminal-Bench) | Mid-level implementation (BYOK/Hybrid) |
| **GPT-5.4 mini** | $0.75 | $4.50 | Good coding (54.4% SWE-bench Pro), strong agentic (60% Terminal-Bench), 2x faster than GPT-5 mini | Expensive output, 400K context, weaker tool use (57.7% MCP) | Mid-level implementation (GHCP) |
| **DeepSeek V4 Pro** | $1.74 | $3.48 | Near-frontier coding (80.6% SWE-bench, 93.5 LiveCodeBench), strong agentic (67.9% Terminal-Bench, 73.6% MCP), 1M context | Weaker on HLE reasoning, Azure-only | Senior coding (BYOK/Hybrid) |
| **GPT-5.3-Codex** | Expensive | Expensive | Top-tier coding, deep reasoning, strong architecture | Expensive, Copilot quota | Senior coding (GHCP) |
| **Gemini 3.5 Flash** | $1.50 | $9.00 | Best-in-class tool use (83.6% MCP), strong terminal coding (76.2%), excellent agentic workflows | Expensive for a "Flash" model | Orchestration (tool-heavy tasks) |
| **Claude Sonnet 4.6** | $3.00 | $15.00 | Excellent instruction-following, strong coding (79.6% SWE-bench), good agentic (79.3%) | Expensive output | Orchestration |
| **GPT-5.4** | $2.50 | $15.00 | Highest global average (80.3), strong reasoning across all categories, 77.5% agentic | Same price as Sonnet | Reasoning-heavy orchestration |
| **Claude Opus 4.8** | $5.00 | $25.00 | Frontier quality, best SWE-bench (83.5%), deep reasoning | Very expensive | Complex multi-system tasks only |

### Cost Comparison at a Glance

```
Output cost per 1M tokens:
Free    ├─ GPT-5 mini ($0)
        │
Cheap   ├─ DeepSeek V4 Flash ($0.28)        ← best coding value (BYOK/Hybrid mid-level)
        │
Mid     ├─ DeepSeek V4 Pro ($3.48)          ← senior coding at 1/7th frontier price
        ├─ GPT-5.4 mini ($4.50)              ← GHCP mid-level
        ├─ Gemini 3.5 Flash ($9.00)          ← best tool use
        │
Premium ├─ Claude Sonnet 4.6 ($15.00)       ← balanced quality
        ├─ GPT-5.4 ($15.00)                  ← best reasoning
        ├─ GPT-5.3-Codex (expensive)         ← GHCP senior coding
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
| 🔴 **Senior** | GPT-5.3-Codex | Copilot quota | Daedalus, Security-Review, Code-Review, PowerBI |
| 🟡 **Mid-Level** | GPT-5.4 mini | Copilot quota | Odysseus, Refactor-Engineer, Security-Fix |
| 🟢 **Free** | GPT-5 mini | Free (included) | Icarus, Oracle, Explorer, Documentation, Diagnostician, Abby |

### BYOK Mode 🟩 — Zero Copilot Quota

| Tier | Model | Cost | Agents |
|------|-------|------|--------|
| 🔴 **Orchestrator** | GPT-5.4 / DeepSeek-V4-Pro (Azure only) | Azure API | Atlas |
| 🟠 **Senior** | DeepSeek V4 Pro | Azure API ($1.74/$3.48) | Daedalus, Security-Review, Code-Review, PowerBI |
| 🟡 **Mid-Level** | DeepSeek V4 Flash | Azure API ($0.14/$0.28) | Odysseus, Refactor-Engineer, Security-Fix |
| 🟢 **Free** | GPT-5 mini | Free (included) | Icarus, Oracle, Explorer, Documentation, Diagnostician, Abby |

### Hybrid Mode 🟪 — Most Flexible

| Tier | Model | Cost | Agents |
|------|-------|------|--------|
| 🔴 **Orchestrator** | Sonnet 4.6 / Opus 4.8 / GPT-5.4 / Gemini 3.5 Flash / DeepSeek-V4-Pro | Copilot quota or Azure API | Atlas |
| 🟠 **Senior** | DeepSeek V4 Pro | Azure API ($1.74/$3.48) | Daedalus, Security-Review, Code-Review, PowerBI |
| 🟡 **Mid-Level** | DeepSeek V4 Flash | Azure API ($0.14/$0.28) | Odysseus, Refactor-Engineer, Security-Fix |
| 🟢 **Free** | GPT-5 mini | Free (included) | Icarus, Oracle, Explorer, Documentation, Diagnostician, Abby |

**Design principle:** Atlas delegates to free-tier agents (Icarus, Oracle, Explorer, Documentation) when the task is simple or involves broad exploration — work that would otherwise consume many expensive tokens. Complex architectural tasks go to Daedalus; standard feature work to Odysseus; simple/mechanical tasks to Icarus.

---

## Architecture

### Primary Agents (Orchestrators)

| Agent | GHCP 🟦 | BYOK 🟩 | Hybrid 🟪 | Role |
|-------|---------|---------|-----------|------|
| **AtlasSonnet** | Claude Sonnet 4.6 | — | Claude Sonnet 4.6 | Orchestrator (balanced quality + instruction-following) |
| **AtlasOpus** | Claude Opus 4.8 | — | Claude Opus 4.8 | Orchestrator (frontier reasoning, use sparingly) |
| **AtlasGPT** | GPT-5.4 | GPT-5.4 | GPT-5.4 | Orchestrator (strongest global reasoning) |
| **AtlasGemini** | Gemini 3.5 Flash | — | Gemini 3.5 Flash | Orchestrator (best tool use, strong agentic) |
| **AtlasDeepSeekPro** | — | DeepSeek-V4-Pro | DeepSeek-V4-Pro | Orchestrator (cheapest capable option) |
| **AtlasDeepSeekFlash** | — | DeepSeek-V4-Flash | — | Orchestrator (ultra-budget BYOK) |

### Implementation Subagents (3-Tier Coding)

| Agent | Role | GHCP 🟦 | BYOK 🟩 | Hybrid 🟪 | Tier | When to Use |
|-------|------|---------|---------|-----------|------|-------------|
| **Daedalus** | Senior Engineer | GPT-5.3-Codex | DeepSeek V4 Pro | DeepSeek V4 Pro | 🔴/🟠 Senior | 5+ files, architecture, complex algorithms, cross-cutting concerns |
| **Odysseus** | Mid-Level Engineer | GPT-5.4 mini | DeepSeek V4 Flash | DeepSeek V4 Flash | 🟡 Mid | 2-4 files, standard features, CRUD, API endpoints, UI components |
| **Icarus** | Junior Engineer | GPT-5 mini | GPT-5 mini | GPT-5 mini | 🟢 Free | 1 file, config changes, renames, boilerplate, simple bug fixes |

### Specialist Subagents

| Agent | GHCP 🟦 | BYOK 🟩 | Hybrid 🟪 | Tier | Specialty |
|-------|---------|---------|-----------|------|-----------|
| **Code-Review** | GPT-5.3-Codex | DeepSeek V4 Pro | DeepSeek V4 Pro | 🔴/🟠 Senior | Code quality, test coverage verification |
| **Refactor-Engineer** | GPT-5.4 mini | DeepSeek V4 Flash | DeepSeek V4 Flash | 🟡 Mid | Clean Code principles, SOLID |
| **Security-Review** | GPT-5.3-Codex | DeepSeek V4 Pro | DeepSeek V4 Pro | 🔴/🟠 Senior | OWASP analysis, threat modeling |
| **Security-Fix** | GPT-5.4 mini | DeepSeek V4 Flash | DeepSeek V4 Flash | 🟡 Mid | Vulnerability remediation |
| **PowerBI** | GPT-5.3-Codex | DeepSeek V4 Pro | DeepSeek V4 Pro | 🔴/🟠 Senior | Power BI models, DAX, TMDL via MCP |

### Free Agents (Research & Support)

| Agent | Model (all modes) | Specialty |
|-------|-------------------|-----------|
| **Oracle** | GPT-5 mini | Context gathering, requirements research |
| **Explorer** | GPT-5 mini | Codebase exploration (3-10 parallel searches) |
| **Documentation** | GPT-5 mini | Doc hygiene, dev journals |
| **Diagnostician** | GPT-5 mini | Debugging, log analysis, test diagnostics |
| **Abby** | GPT-5 mini | ABB internal knowledge (MCP tool) |

**Security Workflow:** Use Security-Review first (audit) → then Security-Fix (remediate)

**Power BI Workflow:** Use PowerBI-subagent for any Power BI Desktop or Fabric semantic model tasks (requires the Power BI Model MCP server extension)

---

## Why This Model Allocation?

**Senior tier (Daedalus):** Complex tasks need strong reasoning and multi-step autonomy. In GHCP, Codex 5.3 excels here. In BYOK/Hybrid, DeepSeek V4 Pro delivers 80.6% SWE-bench and 67.9% Terminal-Bench (strong autonomous coding) at $3.48/M output — 7x cheaper than frontier models for near-parity quality. Also used for code review and security analysis where correctness matters.

**Mid-level tier (Odysseus):** The high-volume workhorse. Standard feature work (2-4 files, known patterns) doesn't need frontier reasoning. In GHCP, GPT-5.4 mini handles this at 54.4% SWE-bench Pro. In BYOK/Hybrid, DeepSeek V4 Flash delivers 79% SWE-bench Verified and 69% MCP tool use at just $0.28/M output — 92% of Pro's quality at 12x less cost. The slight Terminal-Bench gap (56.9% vs 67.9%) doesn't matter for supervised 2-4 file tasks.

**Free tier (Icarus):** Simple, well-scoped tasks (rename a variable, add a config field, write boilerplate) don't need expensive models. GPT-5 mini is included free on paid Copilot plans and handles mechanical coding just fine. Also powers all research/exploration agents.

**Orchestrators (Atlas variants):** Choose based on task complexity:
- **Gemini 3.5 Flash** — best tool use, strong agentic (good default)
- **Claude Sonnet 4.6** — best instruction-following reputation
- **GPT-5.4** — highest overall reasoning scores
- **DeepSeek V4 Pro** — cheapest option that still works well (BYOK)
- **Claude Opus 4.8** — frontier quality, reserve for complex multi-system tasks

**Why BYOK limits orchestrators to Azure OpenAI models:** Non-Azure models (Claude, Gemini via Copilot) don't support prompt caching, which causes token costs to explode on long orchestration conversations. Azure OpenAI endpoints support caching natively.

---

## Usage

### Executing with Atlas

```
@Atlas Creates the plan
@Atlas Implements the plan
```

Atlas delegates Planning → Implementation (Daedalus/Odysseus/Icarus based on complexity) → Code-Review → approval → repeat.

### Direct Research

```
@Oracle Research how the database layer is structured
@Explorer Find all files related to authentication
```

### Workflow Example

```
User: @Atlas add a user dashboard

Atlas: [Clarifies scope, gathers context, presents plan]
  ├─ @Explorer (find UI components)         ← FREE
  ├─ @Oracle (research data fetching)       ← FREE
  └─ Presents plan → Waits for approval

User: Looks good, go ahead

Atlas: Phase 1/4 - Data Layer (complex, multi-file)
  ├─ @Explorer (gather current state)       ← FREE
  └─ @Daedalus (architecture + tests → code → pass)  ← SENIOR
  └─ @Code-Review → APPROVED ✓

Atlas: Phase 2/4 - API Endpoints (standard CRUD)
  └─ @Odysseus (tests → code → pass)       ← MID-LEVEL
  └─ @Code-Review → APPROVED ✓

Atlas: Phase 3/4 - UI Components (standard feature)
  └─ @Odysseus (tests → code → pass)       ← MID-LEVEL
  └─ @Code-Review → APPROVED ✓

Atlas: Phase 4/4 - Config & Wiring (simple, mechanical)
  ├─ @Icarus (add routes)                   ← FREE
  ├─ @Icarus (update config)                ← FREE (parallel)
  └─ @Code-Review → APPROVED ✓

Atlas: All phases complete! [final summary]
```

---

## Key Files

| File | Purpose |
|------|---------|
| `agents-ghcp/` | GHCP mode — pure GitHub Copilot models |
| `agents-byok/` | BYOK mode — DeepSeek + GPT via Azure, zero Copilot quota |
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

1. **Use the right tier** — don't send simple renames to Daedalus; don't send architectural work to Icarus
2. **Leverage parallel execution** — multiple Icarus/Explorer/Oracle instances for independent tasks (they're free!)
3. **Trust the TDD workflow** — each phase is self-contained with tests
4. **Review before proceeding** — Atlas pauses between phases for your feedback
5. **Commit frequently** — after each approved phase
6. **Set up AGENTS.md** — copy template to every project you work on
7. **Prefer free agents for research** — let Oracle/Explorer/Documentation do the heavy reading
8. **Don't over-delegate** — if a task is trivial (1-2 lines, one file), the orchestrator should just do it
9. **Watch your quota** — switch to BYOK or Hybrid when GHCP credits run low

---

## Acknowledgments

Forked from [bigguy345/Github-Copilot-Atlas](https://github.com/bigguy345/Github-Copilot-Atlas), built upon [copilot-orchestra](https://github.com/ShepAlderson/copilot-orchestra) by ShepAlderson, with naming conventions inspired by [oh-my-opencode](https://github.com/nicololau/oh-my-opencode).

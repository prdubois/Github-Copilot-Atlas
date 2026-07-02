# Copilot Atlas

> Multi-agent orchestration system for GitHub Copilot in VS Code — forked from [bigguy345/Github-Copilot-Atlas](https://github.com/bigguy345/Github-Copilot-Atlas), built upon [copilot-orchestra](https://github.com/ShepAlderson/copilot-orchestra), with naming conventions inspired by [oh-my-opencode](https://github.com/nicololau/oh-my-opencode).

---

## Three Operating Modes

This repo supports three configurations you can switch between using a symlink:

| Mode | Folder | Description |
|------|--------|-------------|
| **GHCP** 🟦 | `agents-ghcp/` | **Pure GitHub Copilot** — uses only Copilot-billed models (Claude, GPT). Best quality orchestration, but consumes your Copilot AI Credits. |
| **BYOK** 🟩 | `agents-byok/` | **Bring Your Own Key** — uses DeepSeek + GPT via Azure endpoints. Zero Copilot quota usage. Orchestrators limited to Azure OpenAI models (caching support). |
| **Hybrid** 🟪 | `agents-hybrid/` | **Best of both worlds** — GHCP models for orchestration, DeepSeek + GPT via Azure for subagents. Most cost-effective setup. |

### Model Breakdown by Mode

| Tier | GHCP 🟦 | BYOK 🟩 / Hybrid 🟪 |
|------|---------|----------------------|
| **Orchestrators** | Claude Sonnet 4.6, Claude Opus 4.8, GPT-5.4, Gemini 3.5 Flash | Azure OpenAI (GPT-5.4) for BYOK; GHCP models for Hybrid |
| **Senior** | GPT-5.3-Codex | DeepSeek V4 Pro |
| **Mid-Level** | GPT-5.4 mini | DeepSeek V4 Flash |
| **Junior** | GPT-5.4 nano | *(merged into Mid-Level — same model)* |
| **Research & Support** | GPT-5.4 nano | DeepSeek V4 Flash |
| **Documentation** | GPT-5.4 mini | GPT-5.4 mini (Azure) |

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

All token-based pricing from the [official GHCP pricing page](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing). Azure BYOK pricing from Azure AI Foundry. Since June 1, 2026, all Copilot usage is billed via AI Credits (1 credit = $0.01 USD) based on token consumption.

### Models Used in This System

| Model | Input $/1M | Cached Input $/1M | Output $/1M | Strengths | Weaknesses | Used For |
|-------|-----------|-------------------|------------|-----------|------------|----------|
| **GPT-5.4 nano** | $0.20 | $0.02 | $1.25 | Cheapest GHCP model, 52.4% SWE-bench Pro, good tool use (56.1% MCP), 400K context | Weaker coding than DeepSeek, lower Terminal-Bench (46.3%) | Junior coding & research (GHCP) |
| **DeepSeek V4 Flash** | $0.14 | ❌ None | $0.28 | Exceptional coding (79% SWE-bench Verified), 1M context, 69% MCP tool use, best long-context recall (78.7%) | No input caching on Azure, weaker on long autonomous sessions (56.9% Terminal-Bench) | Mid-level coding, research, exploration, diagnostics (BYOK/Hybrid) |
| **GPT-5.4 mini** | $0.75 | $0.075 | $4.50 | Good coding (54.4% SWE-bench Pro), strong agentic (60% Terminal-Bench), fast (~273 t/s), 400K context | Expensive output relative to DeepSeek | Mid-level coding (GHCP), documentation (all modes) |
| **DeepSeek V4 Pro** | $1.74 | ❌ None | $3.48 | Near-frontier coding (80.6% SWE-bench, 93.5 LiveCodeBench), strong agentic (67.9% Terminal-Bench, 73.6% MCP), 1M context | No input caching on Azure, weaker on HLE reasoning | Senior coding, code review, security (BYOK/Hybrid) |
| **GPT-5.3-Codex** | Expensive | Yes | Expensive | Top-tier coding, deep reasoning, strong architecture | Expensive, Copilot quota | Senior coding, code review, security (GHCP) |
| **Gemini 3.5 Flash** | $1.50 | $0.15 | $9.00 | Best-in-class tool use (83.6% MCP), strong terminal coding (76.2%), excellent agentic workflows | Expensive for a "Flash" model | Orchestration (tool-heavy tasks) |
| **Claude Sonnet 4.6** | $3.00 | $0.30 | $15.00 | Excellent instruction-following, strong coding (79.6% SWE-bench), good agentic (79.3%) | Expensive output | Orchestration |
| **GPT-5.4** | $2.50 | $0.25 | $15.00 | Highest global average (80.3), strong reasoning across all categories, 77.5% agentic | Same price as Sonnet on output | Reasoning-heavy orchestration |
| **Claude Opus 4.8** | $5.00 | $0.50 | $25.00 | Frontier quality, best SWE-bench (83.5%), deep reasoning | Very expensive | Complex multi-system orchestration (rare) |

### Why DeepSeek Can't Orchestrate

DeepSeek models on Azure **do not support input caching**. The orchestrator re-sends the full conversation history every turn (50-100K+ repeated tokens). Without caching, this makes DeepSeek prohibitively expensive for orchestration despite its low headline pricing. GPT-5.4 with 90% cache hits pays $0.25/1M on repeated context vs $2.50 full — a 10× saving that DeepSeek cannot match.

---

## Agent Allocation

### Implementation Subagents

| Agent | Role | GHCP 🟦 | BYOK 🟩 / Hybrid 🟪 | Tier | Best For |
|-------|------|---------|----------------------|------|----------|
| **Daedalus** | Senior Engineer | GPT-5.3-Codex | DeepSeek V4 Pro | 🔴 Expensive | 5+ files, complex architecture, system design |
| **Odysseus** | Mid-Level Engineer | GPT-5.4 mini | DeepSeek V4 Flash | 🟢 Cheap | 2-4 files, standard features, CRUD, API, UI |
| **Icarus** | Junior Engineer | GPT-5.4 nano | *(not used — Odysseus handles all)* | 🟢 Cheapest | Single-file, config, renames, boilerplate (GHCP only) |

> **Note:** In BYOK/Hybrid mode, Icarus is eliminated. DeepSeek V4 Flash is already extremely cheap ($0.28/1M output) and far more capable than a separate junior model. Odysseus handles all implementation regardless of complexity tier.

### Specialist Subagents

| Agent | GHCP 🟦 | BYOK 🟩 / Hybrid 🟪 | Tier | Specialty |
|-------|---------|----------------------|------|-----------|
| **Code-Review** | GPT-5.3-Codex | DeepSeek V4 Pro | 🔴 Expensive | Code quality, test coverage verification |
| **Refactor-Engineer** | GPT-5.4 mini | DeepSeek V4 Flash | 🟢 Cheap | Clean Code principles, SOLID |
| **Security-Review** | GPT-5.3-Codex | DeepSeek V4 Pro | 🔴 Expensive | OWASP analysis, threat modeling |
| **Security-Fix** | GPT-5.4 mini | DeepSeek V4 Flash | 🟢 Cheap | Vulnerability remediation |
| **PowerBI** | GPT-5.3-Codex | DeepSeek V4 Pro | 🔴 Expensive | Power BI models, DAX, TMDL via MCP |

### Research & Support Subagents

| Agent | GHCP 🟦 | BYOK 🟩 / Hybrid 🟪 | Tier | Specialty |
|-------|---------|----------------------|------|-----------|
| **Oracle** | GPT-5.4 nano | DeepSeek V4 Flash | 🟢 Cheap | Context gathering, multi-file research, requirements synthesis |
| **Explorer** | GPT-5.4 nano | DeepSeek V4 Flash | 🟢 Cheap | Codebase exploration, dependency mapping, parallel searches |
| **Documentation** | GPT-5.4 mini | GPT-5.4 mini (Azure) | 🟡 Moderate | Doc hygiene, dev journals, high-quality prose |
| **Diagnostician** | GPT-5.4 nano | DeepSeek V4 Flash | 🟢 Cheap | ALL terminal commands, test execution, log reading |

**Security Workflow:** Use Security-Review first (audit) → then Security-Fix (remediate)

**Power BI Workflow:** Use PowerBI-subagent for any Power BI Desktop or Fabric semantic model tasks (requires the Power BI Model MCP server extension)

---

## Why This Model Allocation?

**Senior tier (Daedalus):** Complex tasks need strong reasoning and multi-step autonomy. In GHCP, Codex 5.3 excels here. In BYOK/Hybrid, DeepSeek V4 Pro delivers 80.6% SWE-bench and 67.9% Terminal-Bench at $3.48/M output — 7× cheaper than frontier models for near-parity quality. Also used for code review and security analysis where correctness matters most.

**Mid-level tier (Odysseus):** The high-volume workhorse. Standard feature work doesn't need frontier reasoning. In GHCP, GPT-5.4 mini handles this at 54.4% SWE-bench Pro. In BYOK/Hybrid, DeepSeek V4 Flash delivers 79% SWE-bench at just $0.28/M output — 92% of Pro's quality at 12× less cost. In Hybrid mode, Odysseus also absorbs Icarus's role since Flash is already cheaper than any separate junior model while being vastly more capable.

**Junior tier (Icarus, GHCP only):** In pure GHCP mode, GPT-5.4 nano ($0.20/$1.25) provides a meaningful cost savings over GPT-5.4 mini for trivial tasks. In Hybrid mode this tier is eliminated — DeepSeek V4 Flash is both cheaper and better.

**Research & Support:** Single-shot agents with no multi-turn conversation, so caching is irrelevant. DeepSeek V4 Flash excels here: 69% MCP tool use (vs 56.1% for nano), 1M context for reading large files, and $0.28 output. Documentation uses GPT-5.4 mini for higher prose quality.

**Orchestrators (Atlas variants):** Must support caching (long multi-turn conversations). Choose based on task complexity:
- **Gemini 3.5 Flash** — best tool use, strong agentic (good default)
- **Claude Sonnet 4.6** — best instruction-following reputation
- **GPT-5.4** — highest overall reasoning scores
- **Claude Opus 4.8** — frontier quality, reserve for complex multi-system tasks

**Why BYOK limits orchestrators to Azure OpenAI models:** Non-Azure models (Claude, Gemini via Copilot) aren't available in BYOK. Azure OpenAI endpoints support prompt caching natively, which is essential for orchestration.

---

## Prompt Cache Optimization

Prompt caching is critical for multi-turn orchestration. Cached input tokens cost **90% less** (Anthropic/OpenAI) or **75% less** (Gemini). A cache miss on a 340K-token conversation can cost 10× more than a hit.

### How Prefix Caching Works

All major providers (Anthropic, OpenAI, Gemini) use **prefix-based caching**: the API matches the beginning of each request against recently cached content. If your request shares an identical prefix with a prior request, those tokens are served from cache. **Any change at position N invalidates everything after it.**

The prompt structure sent by GHCP on each turn is roughly:

```
[System prompt] → [Agent definitions] → [Tool schemas] → [Conversation history] → [Latest message]
```

A mutation in any early section (system prompt, agent list, tools) destroys the cache for the entire conversation history below it.

### Cache TTL by Provider

| Provider | Default TTL | Extended TTL | Cached discount |
|----------|-------------|--------------|-----------------|
| Anthropic (Claude) | ~5 min (resets on hit) | 1 hour (2× write cost) | 90% off input |
| OpenAI (GPT) | 5-10 min | **24 hours** (`prompt_cache_retention`) | 90% off input |
| Google (Gemini) | Short/undisclosed (implicit) | Up to unlimited (explicit) | 75% off input |

**Recommendation:** For long Atlas sessions, prefer OpenAI models (GPT-5.4/5.5) as orchestrators. The 24-hour cache retention means you can take breaks without losing your cached prefix.

### Optimizations Applied in This Repo

#### 1. Explicit Agent List (prevents lazy resolution)

```yaml
# BAD — GHCP lazily resolves agents on first reference, mutating the prefix mid-session
agents: ["*"]

# GOOD — all agents resolved at session start, prefix stays stable
agents: ["Daedalus-subagent", "Odysseus-subagent", "Code-Review-subagent", ...]
```

#### 2. Minimal Orchestrator Tool List

The orchestrator declares only ~16 tools it actually calls directly. All other tools (browser, terminal, bicep, notebooks) are available to subagents in their isolated contexts. This:
- Removes ~34K characters of tool schemas from the prefix
- Eliminates tool search promotion/demotion mutations

#### 3. Deferred `<repoMemory>` Writes

GHCP pins memory content near the top of the prompt. Mid-phase memory writes change the prefix and invalidate the cache for the entire conversation below. The orchestrator writes to scratchpad files during work and only commits to memory at phase boundaries.

#### 4. Terminal Delegation (suppresses ambient context injection)

The orchestrator never runs terminal commands directly. All execution is delegated to Diagnostician-subagent, which runs in an isolated context. This prevents GHCP from injecting changing terminal state (exit codes, output) into the orchestrator's prompt prefix.

### Maintaining Cache Stability During a Session

**Do:**
- Keep the same model and effort level throughout a session
- Let subagents handle volatile work (terminal, browser) in isolated contexts
- Cycle the orchestrator after completing a major phase (clear chat, start fresh)
- Use `/compact` while cache is still warm (within TTL) if context grows too large

**Don't:**
- Switch models or effort level mid-session (changes cache key)
- Write to repoMemory during active work
- Create or modify `.agent.md` files during a session
- Let the orchestrator run terminal commands directly

### Sync Script

When updating Atlas agent prompts, use the sync script to propagate changes across all model variants while preserving each variant's `model:` line:

```bash
# Preview changes
python sync_atlas_agents.py AtlasGPT.agent.md --dry-run

# Apply to all Atlas*.agent.md in the same folder
python sync_atlas_agents.py AtlasGPT.agent.md
```

---

## Usage

### Executing with Atlas

```
@Atlas Creates the plan
@Atlas Implements the plan
```

Atlas delegates Planning → Implementation (Daedalus/Odysseus based on complexity) → Code-Review → approval → repeat.

### Direct Research

```
@Oracle Research how the database layer is structured
@Explorer Find all files related to authentication
```

### Workflow Example

```
User: @Atlas add a user dashboard

Atlas: [Clarifies scope, gathers context, presents plan]
  ├─ @Explorer (find UI components)         ← cheap
  ├─ @Oracle (understand data layer)        ← cheap
  ├─ @Odysseus (implement feature)          ← cheap (Hybrid) / moderate (GHCP)
  ├─ @Diagnostician (run tests)             ← cheap
  ├─ @Code-Review (verify quality)          ← expensive (correctness matters)
  └─ commit
```

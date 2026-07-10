# Copilot Atlas

> Multi-agent orchestration system for GitHub Copilot in VS Code — forked from [bigguy345/Github-Copilot-Atlas](https://github.com/bigguy345/Github-Copilot-Atlas), built upon [copilot-orchestra](https://github.com/ShepAlderson/copilot-orchestra), with naming conventions inspired by [oh-my-opencode](https://github.com/nicololau/oh-my-opencode).

---

## Three Operating Modes

This repo supports three configurations you can switch between using a symlink:

| Mode | Folder | Description |
|------|--------|-------------|
| **GHCP** 🟦 | `agents-ghcp/` | **Pure GitHub Copilot** — uses only Copilot-billed models (Claude, GPT). Best quality orchestration, but consumes your Copilot AI Credits. |
| **BYOK** 🟩 | `agents-byok/` | **Bring Your Own Key** — uses DeepSeek + GPT via Azure endpoints. Zero Copilot quota usage. Orchestrators limited to Azure OpenAI models (caching support). |
| **Hybrid** 🟪 | `agents-hybrid/` | **Best of both worlds** — GHCP models for orchestration + security, DeepSeek + GPT-5.6 via Azure for everything else. Most cost-effective setup. |

### Model Breakdown by Mode

| Tier | GHCP 🟦 | BYOK 🟩 | Hybrid 🟪 |
|------|---------|---------|-----------|
| **Orchestrator** | Claude Sonnet 5, Claude Opus 4.8, GPT-5.6 Sol, GPT-5.6 Terra, Gemini 3.5 Flash | Azure OpenAI (GPT-5.6 Terra) | Claude Sonnet 5, Claude Opus 4.8, GPT-5.6 Sol, GPT-5.6 Terra, Gemini 3.5 Flash (GHCP) |
| **Advisor** | GPT-5.6 Sol | GPT-5.6 Sol (Azure) | GPT-5.6 Sol (GHCP) |
| **Senior Coder** | GPT-5.6 Terra | DeepSeek V4 Flash | DeepSeek V4 Flash (Azure) |
| **Workhorse Coder** | GPT-5.6 Luna | DeepSeek V4 Flash | DeepSeek V4 Flash (Azure) |
| **Judgment** | GPT-5.6 Luna | GPT-5.6 Luna (Azure) | GPT-5.6 Luna (Azure) |
| **Support / Research** | GPT-5.6 Luna | DeepSeek V4 Flash | DeepSeek V4 Flash (Azure) |
| **Documentation** | GPT-5.6 Luna | GPT-5.6 Luna (Azure) | GPT-5.6 Luna (Azure) |

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

| Model | Input $/1M | Cached Input $/1M | Output $/1M | Context | Max Output | Key Benchmark | Used For |
|-------|-----------|-------------------|------------|---------|------------|---------------|----------|
| **GPT-5.6 Sol** | $5.00 | $0.50 | $30.00 | 1.1M | 128K | 88.8% Terminal-Bench 2.1 | Advisor (thinking partner when stuck), orchestration fallback |
| **GPT-5.6 Terra** | $2.50 | $0.25 | $15.00 | 1M | 128K | 82.5% Terminal-Bench 2.1 | Senior coding (GHCP), orchestration fallback |
| **GPT-5.6 Luna** | $1.00 | $0.10 | $6.00 | 400K | 64K | 84.3% Terminal-Bench 2.1 | Workhorse coding (GHCP), judgment, support, docs |
| **Claude Sonnet 5** | $2.00* | $0.20* | $10.00* | 1M | 128K | 80.4% Terminal-Bench 2.1, 63.2% SWE-bench Pro | **Primary orchestrator (Atlas)** |
| **Claude Opus 4.8** | $5.00 | $0.50 | $25.00 | 1M | 128K | 69.2% SWE-bench Pro | Complex orchestration fallback |
| **Gemini 3.5 Flash** | $1.50 | $0.15 | $9.00 | 1M | 64K | 83.6% MCP tool use | Orchestration (tool-heavy tasks) |
| **DeepSeek V4 Flash** | $0.14 | ❌ None | $0.28 | 1M | 128K | 79% SWE-bench Verified, 78.7% long-context recall | Mid-level & senior coding (BYOK/Hybrid), research |

*\* Claude Sonnet 5 promotional pricing through August 31, 2026. Standard pricing TBD.*

### Deprecated Models (removed from this system)

| Model | Replaced By | Reason |
|-------|-------------|--------|
| GPT-5.4 | GPT-5.6 Terra | Same price, full generation newer |
| GPT-5.4 mini | GPT-5.6 Luna | Consolidated into Luna tier |
| GPT-5.4 nano | GPT-5.6 Luna | Consolidated into Luna tier |
| GPT-5.5 | GPT-5.6 Sol | Same price, better benchmarks |
| GPT-5.3-Codex | GPT-5.6 Terra | Terra is senior coder now; Sol reserved for advisor role |
| Claude Sonnet 4.5 | Claude Sonnet 5 | Direct successor, all metrics improved |
| Claude Sonnet 4.6 | Claude Sonnet 5 | Direct successor, all metrics improved |
| DeepSeek V4 Pro | GPT-5.6 Luna | Luna has better agentic benchmarks (84.3% vs 67.9% T-Bench) at comparable cost |

---

## Subagent Allocation — GHCP Mode 🟦

| # | Subagent | Tier | Model | Rationale |
|---|----------|------|-------|-----------|
| — | **Atlas** (orchestrator) | Orchestrator | **Claude Sonnet 5** | Fast sequential execution, self-correcting, doesn't over-ask. Excellent coder — handles simple edits directly. |
| 1 | Mentor | Advisor | **GPT-5.6 Sol** | Thinking partner when Atlas is stuck. Architecture guidance, unblocking, strategic reasoning. Rare usage (1–2×/session max). Not a coder. |
| 2 | Daedalus | Senior Coder | **GPT-5.6 Terra** | Complex architecture, 5+ files, multi-file refactoring, performance-critical logic. |
| 3 | Odysseus | Workhorse Coder | **GPT-5.6 Luna** | 1–4 files, CRUD, APIs, UI, config. Default choice when in doubt. |
| 4 | Code-Review | Judgment | **GPT-5.6 Luna** | Correctness, quality, coverage review. Luna's 84.3% T-Bench delivers solid judgment. |
| 5 | Refactor-Engineer | Workhorse Coder | **GPT-5.6 Luna** | Clean Code refactoring. Bounded, pattern-based. |
| 6 | Security-Review | Senior Coder | **GPT-5.6 Terra** | OWASP analysis. Needs strong reasoning for threat modeling. |
| 7 | Security-Fix | Workhorse Coder | **GPT-5.6 Luna** | Vulnerability remediation (guided by review output). |
| 8 | PowerBI | Judgment | **GPT-5.6 Luna** | Semantic models, DAX. Luna's reasoning quality handles this well. |
| 9 | Oracle | Support | **GPT-5.6 Luna** | Multi-file research, context synthesis. Reads a lot, writes little. |
| 10 | Explorer | Support | **GPT-5.6 Luna** | Broad codebase searches, dependency mapping. |
| 11 | Documentation | Support | **GPT-5.6 Luna** | Docs, dev journals. Good prose at low cost. |
| 12 | Diagnostician | Support | **GPT-5.6 Luna** | Verbose terminal commands, test execution, log reading. |

---

## Subagent Allocation — Hybrid Mode 🟪 (Value-Optimized)

| # | Subagent | Tier | Model | Source | Est. $/call | Rationale |
|---|----------|------|-------|--------|-------------|-----------|
| — | **Atlas** | Orchestrator | **Claude Sonnet 5** | GHCP | — | Fast, self-correcting orchestration with caching. Handles simple edits directly. |
| 1 | Mentor | Advisor | **GPT-5.6 Sol** | Azure | ~$0.14 | Thinking partner when stuck. Rare. Worth the GHCP spend. |
| 2 | Daedalus | Senior Coder |  **GPT-5.6 Luna** | Azure | ~$0.010 | 79% SWE-bench + 1M context for complex multi-file work at rock-bottom cost. |
| 3 | Odysseus | Workhorse Coder | **DeepSeek V4 Flash** | Azure | ~$0.002 | Bounded 1–4 file edits with clear instructions from Atlas. |
| 4 | Code-Review | Judgment | **GPT-5.6 Luna** | Azure | ~$0.028 | Needs evaluation quality. Luna's 84.3% T-Bench for judgment tasks. |
| 5 | Refactor-Engineer | Workhorse Coder | **DeepSeek V4 Flash** | Azure | ~$0.002 | Pattern-based transforms. Bounded, clear instructions. |
| 6 | Security-Review | Senior EXPERT Coder | **GPT-5.6 Terra** | Azure | ~$0.028 | Threat modeling needs reasoning quality. Luna on Azure avoids GHCP burn. |
| 7 | Security-Fix | Workhorse Coder | **DeepSeek V4 Flash** | Azure | ~$0.002 | Guided by review output. Bounded edits. |
| 8 | PowerBI | Judgment | **GPT-5.6 Luna** | Azure | ~$0.028 | DAX reasoning needs quality. |
| 9 | Oracle | Support | **DeepSeek V4 Flash** | Azure | ~$0.010 | 1M context + 78.7% recall. Best for large-scale research. |
| 10 | Explorer | Support | **DeepSeek V4 Flash** | Azure | ~$0.003 | Broad searches at lowest cost. |
| 11 | Documentation | Support | **GPT-5.6 Luna** | Azure | ~$0.028 | Prose quality matters. |
| 12 | Diagnostician | Support | **DeepSeek V4 Flash** | Azure | ~$0.002 | Terminal output parsing. Bounded, cheap. |

### Hybrid Cost Summary

| Source | Roles | Est. cost/session |
|--------|-------|-------------------|
| GHCP (Sonnet 5 + Sol advisor) | Atlas, Mentor (rare) | ~$0.15–0.25 |
| Azure (Flash + Luna) | Everything else | ~$0.05–0.10 |
| **Total** | | **~$0.20–0.35** |

---

## GPT-5.6 Sol as Advisor — Why Not as Coder

Sol is the highest-reasoning model available, but it's **wrong for coding subagent work:**
- Slower execution, more tool calls, over-cautious
- Asks clarifying questions instead of acting (bad for subagent that should just execute)
- $30/M output for code that Terra writes equally well

Sol excels at **thinking, not typing:**
- "I'm stuck on this architecture decision — what am I missing?"
- "This design has a subtle flaw I can't identify — analyze it"
- "What's the right pattern for this unusual constraint?"

The Mentor subagent is called rarely (1–2× per session, only when stuck) and produces short, high-value reasoning — not code. This maximizes Sol's strengths while minimizing its cost.

---

## GPT-5.6 vs Claude Sonnet 5 — Why Sonnet 5 Stays as Atlas

| Dimension | Claude Sonnet 5 | GPT-5.6 Terra | GPT-5.6 Sol |
|-----------|----------------|---------------|-------------|
| **Terminal-Bench 2.1** | 80.4% | 82.5% | 88.8% |
| **SWE-bench Pro** | 63.2% | Not published | Not published |
| **Execution style** | Rapid sequential, self-correcting | Balanced, communicative | Deep reasoning, many tool calls, slower |
| **Orchestrator fit** | ✅ Executes fast, doesn't over-ask | ✅ Good fallback | ⚠️ Great thinker, slow executor |
| **Input $/1M** | $2.00 (promo) | $2.50 | $5.00 |
| **Output $/1M** | $10.00 (promo) | $15.00 | $30.00 |
| **Context** | 1M | 1M | 1.1M |

**Verdict:** Sonnet 5 is the best Atlas orchestrator — fast, aggressive, self-correcting. Sol is the best *advisor* — deep, thorough, communicative. They complement each other perfectly in their respective roles.

---

## Design Principles

1. **Atlas handles trivial work directly.** Edits under 50 lines, simple terminal commands, quick reads — no subagent overhead. Atlas always runs on a strong coding model (Sonnet 5), so don't fear inline edits.
2. **Sol thinks, Terra codes, Luna works, Flash grinds.** Each model in its sweet spot.
3. **No junior tier.** If it's too simple for a subagent, Atlas does it. No overhead for trivial tasks.
4. **Hybrid saves money where it counts.** Only Atlas + Mentor (rare) burn GHCP credits. Everything else runs on Azure.
5. **Flash for bounded tasks, Luna for judgment.** If the subagent gets clear instructions and executes, Flash wins on cost. If it needs to evaluate or reason about quality, Luna's agentic strength justifies the premium.
6. **Caching is a first-class concern.** Orchestrator and subagent prompts are designed to maximize prefix caching. GPT-5.6 introduces explicit cache breakpoints and 30-minute minimum cache life — use them.

---

## Key Changes in This Revision (July 2026)

1. **Deprecated:** GPT-5.4, GPT-5.4 mini, GPT-5.4 nano, GPT-5.5, GPT-5.3-Codex, DeepSeek V4 Pro, Claude Sonnet 4.5, Claude Sonnet 4.6.
2. **Added:** GPT-5.6 Sol, GPT-5.6 Terra, GPT-5.6 Luna, Claude Sonnet 5.
3. **Atlas orchestrator:** Claude Sonnet 5 (replaces Sonnet 4.5/4.6). Proven in production — fast, self-correcting, handles simple edits inline.
4. **New Mentor role:** GPT-5.6 Sol as thinking partner/advisor (replaces Abby tool). Called rarely, high-value reasoning output.
5. **Senior coder:** GPT-5.6 Terra (GHCP) / DeepSeek V4 Flash (Hybrid). Sol is too slow/expensive for coding.
6. **Workhorse coder:** GPT-5.6 Luna (GHCP) / DeepSeek V4 Flash (Hybrid). Default delegation target.
7. **Removed junior tier.** Atlas handles trivial tasks directly — subagent overhead costs more than inline execution.
8. **Removed DeepSeek V4 Pro.** Luna matches or beats it on agentic benchmarks at comparable cost.
9. **⚠️ Admin action required:** GPT-5.6 models are **off by default** in Copilot Business/Enterprise. Enable the policy in Copilot settings.

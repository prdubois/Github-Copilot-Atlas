# Copilot Atlas

> Multi-agent orchestration system for GitHub Copilot in VS Code — forked from [bigguy345/Github-Copilot-Atlas](https://github.com/bigguy345/Github-Copilot-Atlas), built upon [copilot-orchestra](https://github.com/ShepAlderson/copilot-orchestra), with naming conventions inspired by [oh-my-opencode](https://github.com/nicололau/oh-my-opencode).

---

## Two Operating Modes

This repo supports two parallel configurations you can switch between using a symlink:

| Mode | Folder | Orchestrator Model | Worker Model | Free Model |
|------|--------|--------------------|--------------|------------|
| **GHCP** | `agents-ghcp/` | Claude Sonnet/Opus 4.6 / GPT-5.4 | GPT-5.3-Codex | — |
| **BYOK** | `agents-byok/` | DeepSeek Pro 4 | DeepSeek Flash 4 | GPT-5-mini |

### Switching Modes

Use the PowerShell script to swap your VS Code prompts symlink:

```powershell
# Switch to GHCP models (uses Copilot allocation)
./switch-agents.ps1 ghcp

# Switch to Azure/BYOK models (uses your own keys)
./switch-agents.ps1 byok
```

The script updates the symlink at your VS Code prompts folder. No restart needed.

---

## Three-Tier Token Economy (BYOK Mode)

The BYOK mode uses a cost-optimized three-tier architecture:

| Tier | Model | Cost | Agents | Role |
|------|-------|------|--------|------|
| 🔴 **Orchestrator** | DeepSeek Pro 4 | Expensive | Atlas, Prometheus | Planning, decomposition, decisions |
| 🟡 **Worker** | DeepSeek Flash 4 | Moderate | Sisyphus, Frontend-Engineer, Refactor-Engineer, Code-Review, Security-Fix, Security-Review, PowerBI | Code generation, review |
| 🟢 **Free** | GPT-5-mini | Free | Oracle, Explorer, Documentation | Research, exploration, docs |

**Design principle:** Atlas delegates to free-tier agents (Oracle, Explorer, Documentation) when the task involves broad exploration, multi-file research, or documentation updates — work that would otherwise consume many orchestrator tokens. For trivial lookups or single-file reads already in context, Atlas handles them directly to avoid the overhead of briefing a subagent.

---

## Architecture

### Primary Agents (Orchestrators)

| Agent | Model (GHCP) | Model (BYOK) | Role |
|-------|--------------|--------------|------|
| **AtlasSonnet** | Claude Sonnet 4.6 | — | Orchestrator (balanced) |
| **AtlasOpus** | Claude Opus 4.6 | — | Orchestrator (complex tasks) |
| **AtlasGPT** | GPT-5.4 | — | Orchestrator (research-heavy) |
| **AtlasDeepSeek** | — | DeepSeek Pro 4 | Orchestrator (BYOK) |
| **Prometheus** | GPT-5.4 High | DeepSeek Pro 4 | Autonomous planner → hands off to Atlas |

### Specialized Subagents

| Agent | Model (GHCP) | Model (BYOK) | Tier | Specialty |
|-------|--------------|--------------|------|-----------|
| **Oracle** | GPT-5.4 | GPT-5-mini | 🟢 Free | Context gathering, requirements research |
| **Explorer** | GPT-5.4 | GPT-5-mini | 🟢 Free | Codebase exploration (3-10 parallel searches) |
| **Documentation** | Claude Sonnet 4.6 | GPT-5-mini | 🟢 Free | Doc hygiene, dev journals |
| **Sisyphus** | GPT-5.3-Codex | DeepSeek Flash 4 | 🟡 Worker | TDD implementation, E2E-first testing |
| **Code-Review** | GPT-5.3-Codex | DeepSeek Flash 4 | 🟡 Worker | Code quality, test coverage verification |
| **Frontend-Engineer** | GPT-5.3-Codex | DeepSeek Flash 4 | 🟡 Worker | UI/UX, responsive design, accessibility |
| **Refactor-Engineer** | GPT-5.3-Codex | DeepSeek Flash 4 | 🟡 Worker | Clean Code principles, SOLID |
| **Security-Review** | GPT-5.3-Codex | DeepSeek Flash 4 | 🟡 Worker | OWASP analysis, threat modeling |
| **Security-Fix** | GPT-5.3-Codex | DeepSeek Flash 4 | 🟡 Worker | Vulnerability remediation |
| **PowerBI** | GPT-5.3-Codex | DeepSeek Flash 4 | 🟡 Worker | Power BI models, DAX, TMDL via MCP |

**Security Workflow:** Use Security-Review first (audit) → then Security-Fix (remediate)

**Power BI Workflow:** Use PowerBI-subagent for any Power BI Desktop or Fabric semantic model tasks (requires the Power BI Model MCP server extension)

---

## Usage

### Planning with Prometheus

```
@Prometheus Plan adding user authentication to the app
```

Prometheus researches, writes a TDD plan, and offers to hand off to Atlas.

### Executing with Atlas

```
@Atlas Implement the plan from Prometheus
@AtlasDeepSeek Implement the plan from Prometheus   (BYOK mode)
```

Atlas delegates Phase 1 → Sisyphus → Code-Review → approval → repeat.

### Direct Research

```
@Oracle Research how the database layer is structured
@Explorer Find all files related to authentication
```

### Workflow Example

```
User: @Prometheus plan adding a user dashboard

Prometheus:
  ├─ @Explorer (find UI components)       ← FREE
  ├─ @Oracle (research data fetching)     ← FREE
  └─ Writes plan → Offers Atlas handoff

User: Yes, invoke Atlas

Atlas: Phase 1/4 - Test Infrastructure
  ├─ @Explorer (gather current state)     ← FREE
  └─ @Sisyphus (tests first → code → pass)
  └─ @Code-Review → APPROVED ✓
  └─ @Documentation (update docs)         ← FREE

Atlas: Phase 1 complete! [commit message]
```

---

## Key Files

| File | Purpose |
|------|---------|
| `agents-ghcp/` | GHCP mode agent files |
| `agents-byok/` | BYOK mode agent files (three-tier) |
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

**2. Add to both `agents-ghcp/` and `agents-byok/`** (with appropriate model for each)

**3. Test:** `@Atlas Use YourAgent to analyze the database schema`

---

## Best Practices

1. **Use Prometheus for complex features** — research and plan before implementing
2. **Leverage parallel execution** — multiple Explorers/Oracles for large tasks (especially in BYOK mode — they're free!)
3. **Trust the TDD workflow** — each phase is self-contained with tests
4. **Review before proceeding** — check completed phases before moving forward
5. **Commit frequently** — after each approved phase
6. **Set up AGENTS.md** — copy template to every project you work on
7. **In BYOK mode, prefer free agents** — let Oracle/Explorer/Documentation do all the heavy lifting

---

## Acknowledgments

Forked from [bigguy345/Github-Copilot-Atlas](https://github.com/bigguy345/Github-Copilot-Atlas), built upon [copilot-orchestra](https://github.com/ShepAlderson/copilot-orchestra) by ShepAlderson, with naming conventions inspired by [oh-my-opencode](https://github.com/nicololau/oh-my-opencode).

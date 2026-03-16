# Copilot Atlas

A multi-agent orchestration system for VS Code Copilot that enables complex software development workflows through intelligent agent delegation and parallel execution.

> **Note:** Best supported on VS Code Insiders (as of January 2026) for access to the latest agent orchestration features.

## Overview

Custom agent prompts that work together to handle the complete software development lifecycle: **Planning → Implementation → Review → Commit**. The system uses a conductor-delegate pattern where Atlas coordinates specialized subagents.

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/prdubois/Github-Copilot-Atlas.git
```

### 2. Install Agent Files

**Recommended: Create symlinks** (easy updates via git pull)

**Windows (PowerShell as Admin):**
```powershell
# Set your paths
$profileUser = "$env:APPDATA\Code\User"   # or ...\Code - Insiders\User
$repoAgents  = "C:\path\to\Github-Copilot-Atlas"

# Create junction
cmd /c rmdir "$profileUser\agents" 2>nul
cmd /c mklink /J "$profileUser\agents" "$repoAgents"
```

**macOS/Linux:**
```bash
# Set your paths
PROFILE_USER="$HOME/Library/Application Support/Code/User"  # macOS
# PROFILE_USER="$HOME/.config/Code/User"                    # Linux

REPO_AGENTS="/path/to/Github-Copilot-Atlas"

# Create symlink
rm -rf "$PROFILE_USER/agents"
ln -s "$REPO_AGENTS" "$PROFILE_USER/agents"
```

**Alternative: Copy files directly** to VS Code prompts directory:
- **Windows:** `%APPDATA%\Code\User\prompts\`
- **macOS:** `~/Library/Application Support/Code/User/prompts/`
- **Linux:** `~/.config/Code/User/prompts/`

### 3. Configure VS Code Settings

```json
{
  "chat.customAgentInSubagent.enabled": true,
  "github.copilot.chat.responsesApiReasoningEffort": "high"
}
```

### 4. Set Up AGENTS.md in Your Projects

Copy the template to each project you work on:

```bash
cp AGENTS-template.md /path/to/your/project/AGENTS.md
```

**Important:**
- Rename to `AGENTS.md` (uppercase, like README.md)
- Place in project root
- Do NOT modify — project-specific details belong in your project's `README.md`

The `AGENTS.md` file instructs all agents to:
- Read `README.md` first (mandatory)
- Follow E2E-first testing philosophy
- Prefer updating docs over creating new files
- Maintain dev journals for implementation history

### 5. Reload VS Code

---

## Architecture

### Primary Agents

| Agent | Model | Role |
|-------|-------|------|
| **AtlasSonnet** | Claude Sonnet 4.5 | Orchestrator (balanced) |
| **AtlasOpus** | Claude Opus 4.6 | Orchestrator (complex tasks) |
| **AtlasGPT** | GPT-5.4 | Orchestrator (research-heavy) |
| **Prometheus** | GPT-5.4 High | Autonomous planner → hands off to Atlas |

### Specialized Subagents

| Agent | Model | Specialty |
|-------|-------|-----------|
| **Oracle** | GPT-5.4 | Context gathering, requirements research |
| **Sisyphus** | GPT-5.3-Codex | TDD implementation, E2E-first testing |
| **Explorer** | GPT-5.4 | Codebase exploration (3-10 parallel searches) |
| **Code-Review** | GPT-5.3-Codex | Code quality, test coverage verification |
| **Frontend-Engineer** | GPT-5.3-Codex | UI/UX, responsive design, accessibility |
| **Refactor-Engineer** | GPT-5.3-Codex | Clean Code principles, SOLID |
| **Security-Review** | GPT-5.3-Codex | OWASP analysis, threat modeling |
| **Security-Fix** | GPT-5.3-Codex | Vulnerability remediation |
| **Documentation** | Claude Sonnet 4.5 | Doc hygiene, dev journals |

**Security Workflow:** Use Security-Review first (audit) → then Security-Fix (remediate)

---

## Key Features

### 🧠 Context Conservation

Traditional single-agent approaches exhaust context on research. Atlas delegates:

| Agent Type | Context Usage |
|------------|---------------|
| Explorer/Oracle | Read 50k lines → return summary |
| Sisyphus | Focus only on files being modified |
| Code-Review | Examine only changed files |
| Atlas | Orchestrates without touching bulk code |

**Result:** 70-80% more tokens available for actual reasoning.

### 🔄 Parallel Execution

- Explorer: 3-10 parallel searches per batch
- Oracle: Parallel research across subsystems
- Sisyphus: Parallel implementation for disjoint features
- Maximum 10 parallel agents per phase

### 🧪 E2E-First Testing

Every feature requires at least one E2E test with real dependencies. Mocked tests are supplementary, not primary validation. See `AGENTS.md` for full testing philosophy.

### 📋 Structured TDD Plans

- 3-10 incremental, self-contained phases
- Red-green-refactor cycle per phase
- Risk assessment and mitigation strategies

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
```

Atlas delegates Phase 1 → Sisyphus → Code-Review → approval → repeat.

### Direct Research

```
@Oracle Research how the database layer is structured
```

```
@Explorer Find all files related to authentication
```

### Workflow Example

```
User: @Prometheus plan adding a user dashboard

Prometheus:
  ├─ @Explorer (find UI components)
  ├─ @Oracle (research data fetching)
  └─ Writes plan → Offers Atlas handoff

User: Yes, invoke Atlas

Atlas: Phase 1/4 - Test Infrastructure
  └─ @Sisyphus (tests first → code → pass)
  └─ @Code-Review → APPROVED ✓
  └─ @Documentation (update docs)

Atlas: Phase 1 complete! [commit message]
```

---

## Configuration

### Plan Directory

Agents check `AGENTS.md` for plan directory, defaulting to `plans/`.

### Adding Custom Agents

**Quick method:**
```
@Atlas Create a new subagent called Database-Expert that specializes in SQL optimization
```

**Manual method:** See "Adding Custom Agents" section below.

---

## Adding Custom Agents

### Quick Method

```
@Atlas Create a new subagent called Database-Expert that specializes in SQL optimization, schema design, and query analysis. Integrate it with Prometheus and Atlas.
```

### Manual Method

**1. Create agent file:** `YourAgent-subagent.agent.md`

```yaml
---
description: 'Brief description'
argument-hint: What tasks to delegate
tools: ['search', 'usages', 'edit', ...]
model: Claude Sonnet 4.5 (copilot)
---

You are a [ROLE] SUBAGENT called by a parent CONDUCTOR agent.

**Your specialty:** [Domain expertise]
**Your scope:** [Task boundaries]

**Core workflow:**
1. [Step 1]
2. [Step 2]
3. Return structured findings
```

**2. Add to Prometheus** (research tasks):
```markdown
**YourAgent-subagent**:
- Provide clear research goal for [domain]
- Return structured findings
```

**3. Add to Atlas** (implementation tasks):
```markdown
6. YourAgent-subagent: THE [ROLE]. Expert in [domain]
```

**4. Test:**
```
@Atlas Use YourAgent to analyze the database schema
```

### Best Practices

- Single responsibility per agent
- Minimize declared tools
- Return structured findings, not raw dumps
- Consider parallel execution compatibility

---

## Key Files

| File | Purpose |
|------|---------|
| `AtlasGPT.agent.md` | Main conductor (GPT variant) |
| `Prometheus.agent.md` | Autonomous planner |
| `Sisyphus-subagent.agent.md` | TDD implementer |
| `Documentation-subagent.agent.md` | Doc hygiene |
| `AGENTS-template.md` | **Copy to projects as `AGENTS.md`** |

---

## Requirements

- **VS Code Insiders** (recommended)
- **GitHub Copilot** with multi-agent support
- **Settings:**
  - `chat.customAgentInSubagent.enabled`: true
  - `github.copilot.chat.responsesApiReasoningEffort`: "high" (for Prometheus)

---

## Best Practices

1. **Use Prometheus for complex features** — research and plan before implementing
2. **Leverage parallel execution** — multiple Explorers/Oracles for large tasks
3. **Trust the TDD workflow** — each phase is self-contained with tests
4. **Review before proceeding** — check completed phases before moving forward
5. **Commit frequently** — after each approved phase
6. **Set up AGENTS.md** — copy template to every project you work on

---

## Acknowledgments

This project builds upon the excellent work of:
- **[copilot-orchestra](https://github.com/ShepAlderson/copilot-orchestra)** by [ShepAlderson](https://github.com/ShepAlderson) - Foundation and concept for multi-agent orchestration
- **[oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode)** by [code-yeongyu](https://github.com/code-yeongyu) - Inspiration for agent naming conventions and templates
- **[Github-Copilot-Atlas](https://github.com/bigguy345/Github-Copilot-Atlas)** by [bigguy345](https://github.com/bigguy345) - The forked repo
- **[gologic-promptops](https://github.com/gologic-ca/gologic-promptops)** by [gologic-ben](https://github.com/gologic-ben) - Prompt for the code refactoring and security subagents

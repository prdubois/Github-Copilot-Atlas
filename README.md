# Copilot Atlas

A multi-agent orchestration system for VS Code Copilot that enables complex software development workflows through intelligent agent delegation and parallel execution.

> **Note:** Best supported on VS Code Insiders (as of January 2026) for access to the latest agent orchestration features.

## Overview

Custom agent prompts that work together to handle the complete software development lifecycle: **Planning → Implementation → Review → Commit**. The system uses a conductor-delegate pattern where Atlas coordinates specialized subagents.

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/prdubois/Github-Copilot-Atlas.git
```

### Step 2: Locate Your VS Code Prompts Directory

VS Code stores custom agents in a `prompts` folder inside your user data directory.

| OS | Path |
|----|------|
| **Windows** | `%APPDATA%\Code\User\prompts\` |
| **Windows (Insiders)** | `%APPDATA%\Code - Insiders\User\prompts\` |
| **macOS** | `~/Library/Application Support/Code/User/prompts/` |
| **macOS (Insiders)** | `~/Library/Application Support/Code - Insiders/User/prompts/` |
| **Linux** | `~/.config/Code/User/prompts/` |
| **Linux (Insiders)** | `~/.config/Code - Insiders/User/prompts/` |

**To find your exact path on Windows:**
```powershell
# This will show you the full path
echo "$env:APPDATA\Code\User\prompts"
```

### Step 3: Install Agent Files

Choose **ONE** of the following methods:

---

#### Option A: Simple Copy (Easiest)

Just copy all `.agent.md` files from the cloned repo to your prompts directory.

**Windows (PowerShell):**
```powershell
# Navigate to where you cloned the repo
cd C:\path\to\Github-Copilot-Atlas

# Create prompts folder if it doesn't exist
New-Item -ItemType Directory -Path "$env:APPDATA\Code\User\prompts" -Force

# Copy all agent files
Copy-Item *.agent.md "$env:APPDATA\Code\User\prompts\"
```

**macOS/Linux:**
```bash
# Navigate to where you cloned the repo
cd /path/to/Github-Copilot-Atlas

# Create prompts folder if it doesn't exist
mkdir -p ~/Library/Application\ Support/Code/User/prompts  # macOS
# mkdir -p ~/.config/Code/User/prompts                      # Linux

# Copy all agent files
cp *.agent.md ~/Library/Application\ Support/Code/User/prompts/  # macOS
# cp *.agent.md ~/.config/Code/User/prompts/                       # Linux
```

**Downside:** When you `git pull` updates, you must copy files again.

---

#### Option B: Symlink (Recommended for Easy Updates)

Create a symbolic link so VS Code reads directly from your git repo. When you `git pull`, VS Code automatically sees the updates.

**Windows (PowerShell as Administrator):**

> ⚠️ **Must run PowerShell as Administrator** — right-click PowerShell → "Run as administrator"

```powershell
# Set these two paths for YOUR system:
$repoPath = "C:\Programming\Github-Copilot-Atlas"           # Where you cloned the repo
$promptsPath = "$env:APPDATA\Code\User\prompts"            # VS Code prompts folder

# Remove existing prompts folder if it exists
if (Test-Path $promptsPath) {
    Remove-Item $promptsPath -Recurse -Force
}

# Create symbolic link (junction)
cmd /c mklink /J "$promptsPath" "$repoPath"

# Verify it worked
if (Test-Path "$promptsPath\AtlasGPT.agent.md") {
    Write-Host "✅ Success! Symlink created." -ForegroundColor Green
} else {
    Write-Host "❌ Failed. Check your paths." -ForegroundColor Red
}
```

**macOS/Linux:**
```bash
# Set these two paths for YOUR system:
REPO_PATH="/path/to/Github-Copilot-Atlas"
PROMPTS_PATH="$HOME/Library/Application Support/Code/User/prompts"  # macOS
# PROMPTS_PATH="$HOME/.config/Code/User/prompts"                    # Linux

# Remove existing prompts folder if it exists
rm -rf "$PROMPTS_PATH"

# Create symbolic link
ln -s "$REPO_PATH" "$PROMPTS_PATH"

# Verify it worked
ls "$PROMPTS_PATH"/*.agent.md
```

**To update agents later:**
```bash
cd /path/to/Github-Copilot-Atlas
git pull
# That's it! VS Code will see the new files automatically.
```

---

### Step 4: Configure VS Code Settings

Open VS Code settings (JSON) and add:

```json
{
  "chat.customAgentInSubagent.enabled": true,
  "github.copilot.chat.responsesApiReasoningEffort": "high"
}
```

### Step 5: Reload VS Code

Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) → type "Reload Window" → Enter.

### Step 6: Verify Installation

In VS Code, open Copilot Chat and type:
```
@Atlas hello
```

If Atlas responds, you're all set!

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

**2. Add to Prometheus** (for research tasks) and **Atlas** (for implementation tasks)

**3. Test:** `@Atlas Use YourAgent to analyze the database schema`

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

## Troubleshooting

### Agents not appearing in VS Code

1. Verify files are in the correct prompts directory
2. Check file extension is `.agent.md` (not `.md` or `.txt`)
3. Reload VS Code window
4. Check VS Code settings have `chat.customAgentInSubagent.enabled: true`

### Symlink not working (Windows)

- Must run PowerShell as **Administrator**
- Use `cmd /c mklink /J` (junction), not `mklink /D` (directory symlink)
- Verify paths don't have typos

### "Agent not found" errors

- Ensure you're using the correct agent name (e.g., `@Atlas` not `@AtlasGPT`)
- Check that the agent file has valid YAML frontmatter

---

## Acknowledgments

Forked from [bigguy345/Github-Copilot-Atlas](https://github.com/bigguy345/Github-Copilot-Atlas), built upon [copilot-orchestra](https://github.com/ShepAlderson/copilot-orchestra) by ShepAlderson, with naming conventions inspired by [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode).

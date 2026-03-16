# AGENTS.md — Universal Standards for AI Agents

> **Purpose:** This file defines universal coding and documentation standards for AI agents (GitHub Copilot, Claude, Cursor, etc.). It is project-agnostic — all project-specific context lives in `README.md`.

---

## ⚠️ MANDATORY: Read README.md First

**Before ANY work, you MUST read the project's `README.md` file.**

The README contains:
- Project context, purpose, and domain
- Architecture overview and data flow
- Tech stack and constraints
- Module overview (what each module does)
- Key decisions and their rationale
- Documentation index (where to find detailed docs)
- Quick start and development workflow

**Do not proceed with implementation until you have read and understood the README.**

If README.md doesn't exist or is incomplete, inform the user before proceeding.

---

## 1. The Golden Workflow

**Protocol:** `Implement` → `Verify` → `Document`

### Step 1: Implementation
- Write code, fix compile errors, create tests
- **STOP.** Do not proceed to documentation yet.

### Step 2: Verification
- **Preferred:** Run tests (unit, integration, AND E2E) to verify functionality
- **Fallback:** If tests aren't feasible, run verification scripts or manual checks
- If verification passes, proceed to documentation
- If verification fails, fix issues before documenting

### Step 3: Documentation
- Update relevant documentation only AFTER verification succeeds
- Follow documentation rules in Section 5

---

## 2. Autonomy & Interaction

**Execute immediately.** Do not ask for confirmation before starting implementation.

**Only pause for user input when:**
- Requirements are ambiguous
- Critical architectural decisions need approval
- Verification failed and you need guidance
- User explicitly requested approval gates

**Assume the user's prompt is sufficient authorization to proceed.**

---

## 3. File Hygiene

### Investigation & Debug Scripts
- ✅ Place one-off debug/analysis scripts in `/scripts/investigation/` (or similar)
- ❌ Never pollute project root with temporary scripts

### Temporary Working Documents
- ✅ Place plans, drafts, and working docs in `/plans/` directory
- These are temporary and can be created freely
- Clean up after work is complete

### Code Style
- **Scan First:** Before writing code, examine existing files for patterns
- **Match Style:** Use same quotes, indentation, naming conventions as existing code
- **Minimal Diff:** Only output lines you are changing — don't reformat unrelated code

---

## 4. Testing Standards

### The E2E-First Philosophy

**Core Principle:** E2E tests are the ground truth. Mocked tests prove your mocks work, not your code.

```
Confidence Level:
    
    E2E Tests ████████████████████ HIGH (real system, real bugs caught)
    Integration ██████████████     MEDIUM (real modules, some mocks)
    Unit + Mocks ████████          LOW (fast feedback, false confidence risk)
```

### The Golden Rule

**Every feature MUST have at least one E2E test that exercises real code paths.**

Mocked tests alone are INSUFFICIENT. 100 passing mocked tests mean nothing if the real system breaks.

### Test Priority (Write in This Order)

| Priority | Type | What It Tests | Mocking |
|----------|------|---------------|---------|
| 1 | **E2E** | Real system, real dependencies | None |
| 2 | **Integration** | Multiple real modules together | Minimal (external APIs only) |
| 3 | **Unit** | Isolated algorithmic logic | OK for speed |

### When Mocking is Acceptable

✅ **OK to Mock:**
- External third-party APIs (Stripe, SendGrid) — but ALSO write E2E against sandbox
- Time-dependent operations — but ALSO test with real time in E2E
- Expensive operations for fast unit feedback — but E2E must exist

❌ **NEVER Mock:**
- Your own code modules (you're testing nothing)
- Database queries (use a real test database)
- File system operations (use a real temp directory)
- The core behavior you're trying to verify

### The "Mocked Test Tax"

For every mocked test, ask: **"Do I have E2E coverage for this same behavior?"**

- If YES → Mock is acceptable (fast feedback supplement)
- If NO → Write E2E test FIRST, then add mocked test for speed

### Test Organization

```
module/
├── module.py
├── tests/
│   ├── test_module.py         # Unit + integration tests
│   └── e2e/
│       └── test_module_e2e.py # E2E tests (real dependencies)
```

### The "Never Create, Always Augment" Rule

❌ **NEVER** create a new test file without checking if one exists for that module  
✅ **ALWAYS** add new tests to existing test files when possible

### Test Completion Checklist

Before marking tests complete:
- ✅ At least ONE E2E test exists for this feature
- ✅ E2E test uses real dependencies (DB, APIs, files)
- ✅ Mocked tests have corresponding E2E coverage
- ✅ Tests would catch real production bugs, not just prove mocks work

---

## 5. Documentation Standards

### README.md as Context Hub
The root `README.md` is the **primary context source** for AI sessions. It should contain:

| Section | Purpose |
|---------|---------|
| Project Context | What, why, domain |
| Architecture Overview | High-level system design, data flow |
| Tech Stack & Constraints | Languages, frameworks, requirements |
| Module Overview | Map of modules → responsibilities |
| Key Decisions Log | Major architectural decisions + rationale |
| Quick Start | Copy-paste-ready commands |
| Documentation Index | Table linking to `/docs/` files with descriptions |
| Development | Workflow, testing, contribution guidelines |

**Target size:** 1500-3000 words (structured, not prose)

### Documentation Locations

| Content Type | Location |
|--------------|----------|
| Project context & architecture | `README.md` |
| User-facing changes | `CHANGELOG.md` |
| Detailed implementation history | `docs/dev_journal.md` |
| Future work & priorities | `docs/roadmap.md` |
| Module-specific docs | `<module>/README-<module>.md` |
| Architecture deep-dives | `docs/` directory |

### The "Prefer Update, Create When Justified" Rule

✅ **DEFAULT:** Update existing documentation files  
✅ **CREATE NEW** only when clearly justified (see below)  
❌ **AVOID** creating redundant or overlapping documentation

**Justified Creation Scenarios:**
- New module/subsystem with >3 source files
- New major architectural component
- New deployment target/platform
- New external integration (complex, >100 lines)
- New API version with breaking changes
- Migration guides for major upgrades

**Never Create New Docs For:**
- Feature additions to existing modules (update module README)
- Bug fixes (CHANGELOG + dev_journal only)
- Performance improvements (dev_journal)
- Refactoring work (dev_journal only)
- Implementation details (dev_journal)
- Archived/deprecated content (dev_journal only, remove from README)

### Development Journal Format
Every implementation should be logged in `docs/dev_journal.md`:

```markdown
## {Feature/Improvement Title}
**Date:** YYYY-MM-DD HH:MM  
**Executive Summary:** {1-3 sentence summary}

### Implementation Details
{Technical description: decisions, patterns, edge cases, limitations}

### Files Modified
- `path/to/file.ext` - {brief description}

### Related Documentation
- {Links to related docs, issues, PRs}

---
```

---

## 6. Completion Protocol

When completing implementation work:

1. ✅ Verify E2E tests exist and pass
2. ✅ Add entry to `docs/dev_journal.md` (chronological, at bottom)
3. ✅ Update relevant module documentation
4. ✅ Update `CHANGELOG.md` if user-facing changes
5. ✅ Update `README.md` if architecture/modules changed
6. ✅ Clean up temporary files in `/plans/`
7. ❌ Do NOT create `docs/<feature>-implementation.md` files
8. ❌ Do NOT document before verification passes

---

## 7. Anti-Patterns to Avoid

### Testing Anti-Patterns
❌ Writing only mocked tests without E2E coverage  
❌ Mocking your own code modules  
❌ Mocking the database instead of using a test database  
❌ 100 passing tests that don't catch real bugs  
❌ Creating new test files when existing ones cover the module  

### Documentation Anti-Patterns
❌ Creating `docs/<feature>-implementation.md` for every feature  
❌ Duplicating information across multiple files  
❌ Using generic phase numbers ("Phase 43: Database Updates")  
❌ Documenting before verifying implementation works  
❌ Putting archived content in README (use dev_journal)  
❌ Putting roadmap/future work in README (use docs/roadmap.md)  

### Code Anti-Patterns
❌ Reformatting code you didn't change  
❌ Proceeding without reading README.md first  

---

## 8. Quick Reference

### Pre-Work Checklist
```
□ Read README.md
□ Understand project architecture
□ Check Documentation Index for relevant docs
□ Scan existing code patterns
□ Check existing test files before creating new ones
```

### Test Writing Checklist
```
□ Write E2E test FIRST (real dependencies)
□ Add integration tests for module interactions
□ Add unit tests for complex algorithms (mocks OK)
□ Verify mocked tests have E2E counterparts
□ Run full test suite before completion
```

### File Creation Decision Tree
```
Creating a file?
├─ In /plans/? → ✅ OK (temporary)
├─ In /scripts/investigation/? → ✅ OK (debug scripts)
├─ Test file? → Check if existing test file covers module first
├─ In /docs/ or root?
│   ├─ Does topic exist in current docs? → Update existing
│   ├─ Matches justified creation scenario? → ✅ Create + update README index
│   └─ Uncertain? → Ask user
└─ Source code? → ✅ OK
```

### Documentation Update Triggers
| Event | Update |
|-------|--------|
| New module added | README: Architecture + Module Overview + Doc Index |
| Major decision made | README: Key Decisions Log |
| New doc file created | README: Documentation Index |
| Implementation complete | dev_journal.md + relevant module docs |
| User-facing change | CHANGELOG.md |
| Priorities changed | docs/roadmap.md |

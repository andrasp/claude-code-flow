---
name: validation-skill
description: Multi-lens code review with parallel specialist reviewers. Use /validate to run comprehensive code review on recent changes.
allowed-tools: Read, Glob, Grep, Bash(git diff:*), Bash(git log:*), Bash(git show:*), Task
invocation: Called as part of /flow workflow (Phase 3 Implementation → Completion transition) or manually via /validate command.
---

# Validation Skill: Multi-Lens Code Review

Comprehensive code review through parallel specialist subagents, each examining changes through a different lens.

## Activation

- **Manual**: User invokes `/validate` or requests validation
- **During flow**: Can be triggered in Implementation → Completion transition

## Execution Flow

### Phase 1: Preparation

1. **Identify changed files** based on input from `/validate` command:
   - All uncommitted changes (staged + unstaged): `git diff --name-only HEAD`
   - Specific files/directories: use provided paths
   - Commit range: `git diff --name-only <range>`

2. **Categorize changes by type:**

   | Category | Extensions/Patterns | Reviewers |
   |----------|---------------------|-----------|
   | Source code | `.ts`, `.js`, `.py`, `.go`, `.rs`, `.java`, etc. | Security, Architecture, Quality, Performance, Error Handling |
   | Tests | `*.test.*`, `*.spec.*`, `__tests__/` | Testing |
   | Config | `*.json`, `*.yaml`, `*.toml`, `*.env*` | Scalability |
   | Docs | `*.md`, `docs/` | Skip code review, note for user |

   Present summary to user:
   ```
   Found [N] changed files:
   - [X] source files
   - [Y] test files
   - [Z] config files
   - [W] documentation files (skipped)

   Proceeding with review...
   ```

3. **Load user guidelines**: Check for `~/.claude/CLAUDE.md` (user-level) and project root `CLAUDE.md`. Pass to all reviewers for checking against coding standards.

### Phase 2: Parallel Review

Spawn reviewer subagents in parallel using Task tool. Each reviewer:
- Receives list of changed files
- Reads and analyzes through its lens
- Returns structured findings with severity, location, and suggested fix

**Reviewers** (prompts in `reviewers/`):

| Reviewer | File | Focus |
|----------|------|-------|
| Security | `security.md` | Vulnerabilities, injection, auth issues |
| Architecture | `architecture.md` | Design patterns, coupling, layer violations |
| Quality | `quality.md` | Duplication, naming, complexity, CLAUDE.md compliance |
| Performance | `performance.md` | Algorithms, queries, bottlenecks |
| Scalability | `scalability.md` | Concurrency, state, distributed concerns |
| Testing | `testing.md` | Coverage, test quality, edge cases |
| Error Handling | `error-handling.md` | Robustness, graceful degradation |

**Launching reviewers:**

Read each reviewer prompt from `reviewers/`, substitute `{files}` with the file list, and spawn:
```
Task(
  subagent_type="feature-dev:code-reviewer",
  prompt="[Contents of reviewer prompt with {files} replaced]"
)
```

Launch all relevant reviewers in parallel (single message with multiple Task calls). Quality reviewer always runs.

### Phase 3: Aggregation

1. Collect findings from all reviewers
2. Deduplicate (same issue found by multiple reviewers)
3. Prioritize by severity: Critical > High > Medium > Low
4. Group by file for easier navigation

### Phase 4: Presentation

Present aggregated report:

```markdown
# Validation Report

## Summary
- **Files Reviewed:** [N]
- **Critical Issues:** [N] (must fix)
- **High Issues:** [N] (should fix)
- **Medium Issues:** [N] (recommended)
- **Low Issues:** [N] (noted)

## Critical Issues
| File | Line | Issue | Reviewer | Suggested Fix |
|------|------|-------|----------|---------------|
| ... | ... | ... | ... | ... |

## High Issues
[Same table format]

## Medium Issues
[Same table format]

---
**Options:**
1. Fix Critical + High issues automatically
2. Show me the details first
3. Proceed without fixing (document override)
```

### Phase 5: Handle User Decision

**If user chooses Option 1 (Fix automatically):**
1. For each Critical/High issue, generate and apply the fix
2. After fixes, re-run only the affected reviewers to verify
3. Repeat until resolved or max 3 iterations
4. Present final status

**If user chooses Option 2 (Show details):**
Show full description and suggested fix for each issue, then return to options.

**If user chooses Option 3 (Override):**
Document in outcome.md (if flow is active):
```markdown
## Validation Override
Completed with [N] unresolved [severity] issues per user decision.
Issues: [list]
Reason: [ask user for reason]
```

## Severity Definitions

| Severity | Criteria | Action |
|----------|----------|--------|
| **Critical** | Security vulnerability, data loss risk, crash | Must fix before completion |
| **High** | Significant bug, performance issue, arch violation | Should fix, can override |
| **Medium** | Code quality, maintainability concern | Recommended, advisory |
| **Low** | Style, minor improvement | Noted, no action required |

## Configuration

Users can customize via conversation:
- "Skip security review" → exclude Security reviewer
- "Only check for critical issues" → filter output
- "Don't auto-remediate" → present only, no fixes

## Integration with Flow

When used during a flow's completion phase:
- Critical issues block completion (user can override)
- Findings are documented in outcome.md
- Remediation is part of the flow's implementation record

---
description: Multi-lens code review with parallel specialist reviewers
argument-hint: [optional: commit range or file paths to review]
---

# /validate - Multi-Lens Code Review

You are initiating a comprehensive code review. This command parses the user's input and transitions to the validation-skill for execution.

## Step 1: Parse Arguments

**If argument provided ($1 exists):**
- If it looks like a commit range (e.g., `HEAD~3`, `abc123..def456`): validate that range
- If it looks like file paths: validate those specific files
- Otherwise: interpret as description (e.g., "my current changes") and validate uncommitted changes

**If no argument (bare /validate):**
Default to validating all uncommitted changes, both staged and unstaged (`git diff --name-only HEAD`).

**For active flow work:**
If there's an active flow context (`docs/context/*/plan.md` with Status: In Progress), offer to review all changes since flow start.

## Step 2: Execute Validation

Transition to the validation-skill for execution. The skill handles:
- File categorization
- Launching parallel reviewers
- Aggregating results
- Presenting findings
- Remediation workflow

See `skills/validation-skill/SKILL.md` for the full execution flow.

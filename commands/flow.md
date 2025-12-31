---
description: Initiate structured AI-assisted development workflow with consistent documentation
argument-hint: [optional description of what you want to work on]
---

# /flow - Structured Development Workflow

You are initiating a structured development workflow. This command helps organize work with consistent documentation practices and type-specific guidance.

## Step 1: Determine Work Type

**If the user provided a description (argument $1 exists):**
Analyze the description to infer the work type. Then confirm with the user:

"Based on your description, this sounds like **[inferred type]** work. Is that correct?"

**If no description was provided (bare /flow):**
Use a two-step question flow to determine work type.

**Question 1 - Category:**
Use AskUserQuestion with these options:
- **Build new** - Create new functionality from scratch
- **Improve existing** - Enhance or restructure current code
- **Bugfix** - Fix a specific issue or defect
- **Custom** - User-defined focus, doesn't fit above

**Question 2 - Specific type (conditional):**

If user selected **Build new**, ask:
- **Greenfield** - New component/system from scratch
- **Feature** - New feature added to existing codebase
- **Integration** - Connect with external APIs, services, or systems

If user selected **Improve existing**, ask:
- **Refactor** - Restructure or reorganize existing code
- **Optimization** - Performance, efficiency, resource usage

If user selected **Bugfix** or **Custom**, skip Question 2 and proceed with that type directly.

## Step 2: Gather Context

**Principle: Explore first, ask only when blocked by genuine ambiguity.**

If the user provided a description, you likely have enough to start exploring. Do NOT ask a list of questions upfront—most answers can be discovered through codebase exploration.

### What to explore (not ask):
- Existing patterns and conventions in the codebase
- Related files and integration points
- Test coverage and existing tests
- Similar implementations to reference

### When to ask:
- A workflow step explicitly calls for it (e.g., choosing work type or documents)
- The user's description is genuinely unclear about intent
- Multiple valid approaches exist and user preference matters
- You've exhausted available sources (codebase, databases, web search, documentation) and still lack critical info
- You've explored and hit a true ambiguity

### Type-specific essentials (ask only if not provided):

| Type | Essential Info |
|------|----------------|
| Greenfield | What the new system's purpose is |
| Feature | What the feature should do |
| Integration | What external system to connect with |
| Refactor | What code and why |
| Optimization | What metric to improve |
| Bugfix | What the bug is |
| Custom | What the goal is |

If the user already provided this in their description, proceed to exploration.

## Step 3: Assess Complexity

Evaluate the work and provide an assessment:

"This appears to be a **[complex/moderate/simple]** task because:
- [reason 1]
- [reason 2]
- [reason 3]

Would you like to enter **plan mode** for deeper exploration before implementation?"

Regardless of their choice, you will create a plan.md document. Plan mode just determines whether Claude does extensive exploration first.

## Step 4: Create Context Directory

Get the current date from system time and create a short topic slug from the description.

**Topic slug convention:** lowercase words separated by dashes (e.g., `user-authentication`, `payment-api`, `fix-login-bug`).

Create the directory structure:
```
docs/context/<category>/YYYY-MM-DD_<topic>/
```

Categories map to work types:
- Greenfield → `greenfield/`
- Feature → `feature/`
- Integration → `integration/`
- Refactor → `refactor/`
- Optimization → `optimization/`
- Bugfix → `bugfix/`
- Custom → `custom/`

Use the Write tool to create the directory by creating the first file.

## Step 5: Choose Documents

Use the AskUserQuestion tool (with multiSelect enabled) to ask which optional documents to create:

```
Which documents do you want? (plan.md is always created)

- research.md - For capturing analysis and findings
- tasks.md - For tracking progress with checkboxes
- outcome.md - For recording results when done
```

## Step 6: Initialize Documents

Create the selected documents in the context directory.

### plan.md (Always created)
```markdown
# [Topic] Plan

**Type:** [Work Type]
**Created:** YYYY-MM-DD
**Status:** In Progress

## Overview

[Brief description of the work]

## Goals

- [ ] Goal 1
- [ ] Goal 2

## Approach

[To be filled in during planning/implementation]

## Success Criteria

- [ ] Criterion 1
- [ ] Criterion 2
```

### research.md (If selected)
```markdown
# [Topic] Research

**Plan:** [plan.md](./plan.md)

## Findings

[Research notes will be added here]

## Key Insights

[Summary of important discoveries]
```

### tasks.md (If selected)
```markdown
# [Topic] Tasks

**Plan:** [plan.md](./plan.md)

## In Progress

- [ ] Current task

## Pending

- [ ] Next task

## Completed

[Completed items will be moved here]
```

### outcome.md (If selected)
```markdown
# [Topic] Outcome

**Plan:** [plan.md](./plan.md)
**Completed:** [Date when finished]

## Summary

[What was accomplished]

## Changes Made

[List of files/components changed]

## Lessons Learned

[What we learned for future work]
```

## Step 7: Begin Workflow

After creating the context directory and documents, transition to the type-specific workflow by invoking the appropriate guidance from the flow skill.

Tell the user:
"Context directory created at `docs/context/<category>/YYYY-MM-DD_<topic>/`

Documents initialized:
- plan.md
- [list only the optional docs the user selected]

Ready to begin **[Work Type]** workflow. [Type-specific next step guidance]"

Then proceed with the type-specific workflow guidance.

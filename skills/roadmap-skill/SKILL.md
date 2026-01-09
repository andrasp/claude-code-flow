---
name: roadmap-skill
description: Strategic work planning through natural conversation. Auto-activates when user discusses work items, priorities, dependencies, or what to work on next. Works independently of /flow.
allowed-tools: Read, Write, Glob, Grep, Task, AskUserQuestion
---

# Roadmap Skill - Conversational Work Planning

This skill handles natural language interactions with the strategic roadmap. It works **independently of /flow** - users don't need to be in a flow to discuss, query, or modify their roadmap.

## Auto-Activation

Activate this skill when user:
- Mentions roadmap item IDs (RM-001, RM-XXX)
- Discusses dependencies ("X depends on Y", "can't do X until Y")
- Asks about priorities ("what's most important", "what should I work on")
- Talks about work items in planning context ("the dashboard feature", "that API work")
- Asks about progress ("how much is done", "what's blocked")

## Natural Language Understanding

### Dependency Statements

When user says things like:
- "the dashboard button will depend on first completing that backend api"
- "we can't do oauth until auth is done"
- "X needs Y to be finished first"

**Action:**
1. Search `docs/context/roadmap/items/` for items matching the mentioned work
2. If both items found:
   - Check if dependency already exists
   - If not: "I found **RM-003 Dashboard UI** and **RM-001 Backend API**. Should I add RM-003 as dependent on RM-001?"
   - If yes: "That dependency already exists (RM-003 depends on RM-001)."
3. If one/both items not found:
   - "I found RM-001 (Backend API) but didn't find a roadmap item for 'dashboard button'. Should I create one?"

### Priority Discussions

When user says:
- "the payment feature is more important than the dashboard"
- "we should prioritize security fixes"
- "bump the auth work to P0"

**Action:**
1. Find the referenced items
2. Confirm the change: "Update **RM-002 Payment Integration** to P1 (high)?"
3. Apply if confirmed

### Status Updates

When user says:
- "I'm starting work on the auth system"
- "the API work is blocked waiting for specs"
- "we finished the dashboard redesign"

**Action:**
1. Find the referenced item
2. Update status appropriately (in-progress, blocked, completed)
3. If blocked, ask for reason
4. If completed, offer to move to archive

### What's Next Questions

When user asks:
- "what should I work on?"
- "what's the highest priority?"
- "what's ready to start?"

**Action:**
1. Filter to planned items with no unmet dependencies
2. Sort by priority
3. Present top recommendations with reasoning

### Progress Queries

When user asks:
- "how are we doing?"
- "what's blocked?"
- "show me the roadmap"

**Action:**
1. Read index.md and items
2. Summarize current state
3. Highlight blockers or concerns

## Fuzzy Matching

When searching for items by description:
1. Extract keywords from user's phrase
2. Search item titles and descriptions
3. If multiple matches, ask for clarification
4. If no matches, offer to create new item

**Example:**
```
User: "the dashboard button depends on the backend api"

Claude: [searches roadmap items]
Found potential matches:
- "dashboard button" → RM-003 (Dashboard UI Redesign)
- "backend api" → RM-001 (Backend API v2)

Is this correct? Or did you mean different items?
```

## Creating Items Conversationally

When user mentions work that doesn't exist:
```
User: "we need to add dark mode support"

Claude: I don't see a roadmap item for dark mode. Would you like me to create one?

[If yes, gather minimal info conversationally:]
- What priority? (P0-P3)
- Any dependencies?
- Rough effort? (XS/S/M/L/XL)
```

**Important:** Items created conversationally use the standard item format (see [Item Format](#item-format) below). This ensures consistent structure for UI parsing.

## Handling Ambiguity

When references are unclear:
1. Present options: "Did you mean RM-001 (Auth System) or RM-005 (Auth Tokens)?"
2. If totally unclear: "I couldn't find a roadmap item matching 'X'. Can you be more specific?"
3. Never assume - always confirm before making changes

## Integration Points

### With /flow-roadmap Command
The command handles explicit operations. This skill handles conversational ones. Both modify the same data in `docs/context/roadmap/`.

### With /flow Workflow
When a flow is active and linked to a roadmap item, this skill can provide context. But it doesn't require an active flow to work.

## Directory Structure

```
docs/context/roadmap/
├── index.md              # Overview (read for summaries)
├── items/                # Individual items (search here)
│   ├── RM-001_auth-system.md
│   └── ...
├── categories.md         # Category definitions
├── archive/              # Completed items
└── .meta/
    └── sequence.txt      # Next item number
```

## Item Format

All roadmap items follow this structure for consistent UI parsing:

```markdown
# RM-{seq}: {Title}

## Metadata
- **Status**: planned | in-progress | blocked | completed | cancelled
- **Priority**: P0 (critical) | P1 (high) | P2 (medium) | P3 (low)
- **Category**: {category}
- **Effort**: XS | S | M | L | XL
- **Created**: {date}
- **Target**: {target or "none"}

## Dependencies
- **Blocked by**: {comma-separated IDs or "none"}
- **Blocks**: {comma-separated IDs or "none"}

## Description

{description of the work}

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Notes

{additional notes}

## Linked Flows

{flows will be linked here when work starts}

## History

- {date}: Created
- {date}: {status change or other event}
```

### Priority Definitions

| Level | Name | When to Use |
|-------|------|-------------|
| P0 | Critical | Blocking release, security issue, major production bug |
| P1 | High | Important for next milestone, significant user impact |
| P2 | Medium | Should do soon, moderate impact |
| P3 | Low | Nice to have, low urgency |

### Effort Definitions

| Size | Scope | Typical Duration |
|------|-------|------------------|
| XS | Trivial change | < 1 hour |
| S | Small, focused | Few hours |
| M | Medium complexity | 1-2 days |
| L | Large feature | Several days |
| XL | Epic (consider breaking down) | Week+ |

## Index File Format

The `index.md` provides quick overview:

```markdown
# Project Roadmap

## Summary
- **Total Items**: {count}
- **Completed**: {count} ({percent}%)
- **In Progress**: {count}
- **Planned**: {count}
- **Blocked**: {count}

## Current Focus
{table of in-progress items}

## Up Next
{table of highest priority planned items}

## Blocked
{table of blocked items with reasons}

## Recently Completed
{last 5 completed items}

---
*Last updated: {date}*
```

## Categories File Format

```markdown
# Roadmap Categories

## Core Product
- **feature**: New functionality
- **enhancement**: Improvements to existing features

## Technical
- **infra**: Infrastructure and deployment
- **refactor**: Code restructuring
- **perf**: Performance optimization
- **security**: Security improvements

## Quality
- **bugfix**: Bug fixes
- **testing**: Test coverage
- **docs**: Documentation
- **debt**: Technical debt
```

## Examples

**Example 1: Adding dependency**
```
User: "payment processing needs the auth system done first"

Claude: I found:
- RM-004: Payment Processing (P1, planned)
- RM-001: Auth System (P0, in-progress)

Add dependency: RM-004 depends on RM-001? [Y/n]

User: yes

Claude: Done. RM-004 (Payment Processing) now depends on RM-001 (Auth System).
Updated both items.
```

**Example 2: Status update**
```
User: "I finished the dashboard work"

Claude: Great! Marking RM-003 (Dashboard Redesign) as completed.
Should I move it to archive? [Y/n]
```

**Example 3: What's next**
```
User: "what should I tackle next?"

Claude: Based on your roadmap:

**Recommended: RM-007 (Email Notifications)** - P2, Small effort
- No blockers
- Only P2 but quick win (S effort)

**Also ready:**
- RM-008 (API Rate Limiting) - P2, Medium effort
- RM-009 (User Profiles) - P3, Medium effort

Note: RM-004 (Payment Processing) is P1 but blocked by RM-001 (Auth System).
```

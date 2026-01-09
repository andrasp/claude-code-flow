---
description: Manage strategic work roadmap with prioritized items, dependencies, and progress tracking
argument-hint: [subcommand] [args] - e.g., "list", "add 'Feature name'", "show RM-001"
---

# /flow-roadmap - Strategic Work Planning

Manage a strategic backlog of planned work with priorities, dependencies, and progress tracking. While `/flow` manages individual pieces of work, `/flow-roadmap` manages the big picture.

**See `skills/roadmap-skill/SKILL.md` for templates, formats, and definitions.**

## Initialization

If `docs/context/roadmap/` doesn't exist, create the directory structure and initialize files using templates from the roadmap-skill.

## Subcommands

### Default (no subcommand) - Show Overview

1. Read `docs/context/roadmap/index.md`
2. If doesn't exist, offer to initialize
3. Display roadmap summary (counts, in-progress, up next, blocked)

### `list [--status=X] [--priority=X] [--category=X]`

List roadmap items with optional filters.

1. Read all files from `docs/context/roadmap/items/`
2. Parse metadata from each item
3. Apply filters if provided (comma-separated values)
4. Sort by: priority (P0 first), then creation date
5. Display as table

### `add "description"`

Add a new roadmap item.

1. Read `.meta/sequence.txt` to get next number
2. Generate slug from description (lowercase, hyphens)
3. Use AskUserQuestion to gather: Priority, Category, Effort, Dependencies, Target
4. Create item file using template from roadmap-skill
5. Increment sequence.txt
6. Update index.md counts

### `show <id>`

Show detailed view of a roadmap item.

1. Find item file by ID (e.g., RM-001)
2. Display full content
3. Show linked flows and their status
4. Show dependency chain (what blocks this, what this blocks)

### `edit <id>`

Open item for editing.

1. Find item file
2. Tell user the file path to edit
3. Offer to make specific changes interactively

### `next`

Suggest next item to work on.

1. Filter to `status: planned` items
2. Exclude items with unmet dependencies
3. Sort by priority, then prefer smaller effort
4. Return top recommendation with reasoning

### `block <id> "reason"`

Mark item as blocked.

1. Update item's status to "blocked"
2. Add block reason to Notes section
3. Update History section
4. Update index.md

### `unblock <id>`

Remove block from item.

1. Update item's status back to previous (usually "planned" or "in-progress")
2. Update History section
3. Update index.md

### `complete <id>`

Manually mark item as completed (when not done via flow).

1. Verify with user (normally happens via flow finalization)
2. Update status to "completed"
3. Move file to `archive/{year}-Q{quarter}/`
4. Update History and index.md

### `cancel <id> "reason"`

Cancel a roadmap item.

1. Update status to "cancelled"
2. Add cancellation reason to Notes
3. Move to archive
4. Update index.md

### `depends <id> --on <dependency-id>`

Add dependency between items.

1. Check for circular dependencies (fail if would create cycle)
2. Add dependency-id to item's "Blocked by" list
3. Add id to dependency-id's "Blocks" list
4. Update both items

### `undepends <id> --on <dependency-id>`

Remove dependency from both items' dependency lists.

### `stats`

Show roadmap statistics: by status, priority, category, and health metrics.

## Integration with /flow

### Starting a Flow for a Roadmap Item

```bash
/flow feature "implement user auth" --roadmap RM-001
# or
/flow work on RM-001
```

**What happens:**
1. Read roadmap item for context (description, acceptance criteria)
2. Include Roadmap Reference section in flow's plan.md
3. Update roadmap item status: planned → in-progress
4. Add to roadmap item's Linked Flows section

### Flow Completion → Roadmap Update

When a flow linked to a roadmap item completes:

1. Update roadmap item's Linked Flows with outcome
2. Check acceptance criteria against accomplishments
3. If all criteria met: prompt to mark roadmap item completed
4. Update History section

This is **required** during flow finalization when a roadmap item is linked.

## Updating index.md

After any status change, regenerate index.md with current counts and lists.

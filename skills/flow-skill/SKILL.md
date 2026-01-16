---
name: flow-skill
description: Structured development workflow guidance. Auto-activates when user references a docs/context/ path. Provides guided workflows for feature development, refactoring, optimization, greenfield projects, and bugfixes. Use /flow command to start new work.
allowed-tools: Read, Write, Glob, Grep, Bash(mkdir:*), Task, AskUserQuestion
---

# Flow - Structured Development Workflow Skill

This skill provides guidance for structured AI-assisted development workflows. It auto-activates when:
- User references a `docs/context/` path (e.g., "let's continue docs/context/feature/2025-01-15_user-auth")
- User explicitly invokes `/flow`

## How Flow Works

The context directory (`docs/context/<type>/<date>_<topic>/`) holds **documentation**, not code. The actual code lives elsewhere in the codebase. Once a workflow is active, the guidance applies to all work related to that context, regardless of which files are being edited.

**The documents are your anchor.** When you return to a session or context gets compacted, reading plan.md and tasks.md restores understanding of what you're doing and why. The code you're writing might be in `src/`, `lib/`, or anywhere else. The workflow guidance still applies.

## Resuming Work

When the user references a context path:

1. **Parse the path** to identify work type and context directory
2. **Read the context files** (plan.md, tasks.md, etc.) from that directory
3. **Load the appropriate guidance** based on work type (see table below)
4. **Summarize current state** and ask if they want to continue
5. **Apply workflow guidance to all subsequent work** for this context

| Work Type | Directory Pattern | Guidance |
|-----------|-------------------|----------|
| Greenfield | `docs/context/greenfield/` | [types/greenfield.md](types/greenfield.md) |
| Feature | `docs/context/feature/` | [types/feature.md](types/feature.md) |
| Integration | `docs/context/integration/` | [types/integration.md](types/integration.md) |
| Refactor | `docs/context/refactor/` | [types/refactor.md](types/refactor.md) |
| Optimization | `docs/context/optimization/` | [types/optimization.md](types/optimization.md) |
| Bugfix | `docs/context/bugfix/` | [types/bugfix.md](types/bugfix.md) |
| Custom | `docs/context/custom/` | [types/custom.md](types/custom.md) |

## Searching Past Flows

During active work, users may ask about past flows:
- "Have I done something like this before?"
- "What patterns did I use for authentication?"
- "Show me past work on caching"
- "How did I handle X last time?"

**When you detect a search-like question:**

1. **Spawn a search subagent** (Task with subagent_type="Explore") to search `docs/context/`:

```
Search past flows for: "<extracted query>"

1. Grep for keywords across docs/context/**/plan.md and outcome.md
2. For matches, extract Overview/Goals from plan.md and Summary/Lessons from outcome.md
3. Note path (contains type, date, topic) and status (has outcome.md = completed)
4. Return only genuinely relevant matches (max 5), sorted by relevance then recency
5. If nothing is truly relevant, say so - don't force matches
6. Do NOT return raw file contents - summarize
```

2. **Present results** with citations:

```
Found 2 past flows related to "[query]":

1. **feature/2024-12-15_user-auth** (completed)
   Goal: Implement JWT authentication
   Outcome: Used refresh token rotation, noted cookie handling gotchas

2. **bugfix/2024-11-20_session-timeout** (completed)
   Goal: Fix premature session expiration
   Outcome: Root cause was timezone mismatch in token validation

Want me to dive deeper into any of these?
```

3. **If user wants details**, read the full plan.md and outcome.md from that flow and summarize relevant insights.

**Why subagent:** Searching past flows can involve grepping many files. Doing this in the main session pollutes context with raw search output. The subagent does the heavy lifting and returns only the summary.

## Core Documents

Workflows use these documents (user chooses which optional ones to create):

| Document | Purpose | Usage |
|----------|---------|-------|
| `plan.md` | Implementation plan, goals, success criteria | **Required** - Always created |
| `outcome.md` | Record of changes, learnings, and extracted memory | **Required** - Created at start, updated continuously |
| `research.md` | Analysis, findings, raw data | Optional - User chooses |
| `tasks.md` | Granular task tracking with checkboxes | Optional - User chooses |

### Outcome Template

Create `outcome.md` at flow start with this structure:

```markdown
# Outcome

## Status
🟡 In Progress

## Summary
[To be filled as work progresses]

## Changes Made
[Updated incrementally during implementation]

## Learnings Extracted
[Filled during finalization]

## Next Steps
[Discovered during implementation]
```

**Update outcome.md continuously** during implementation - not just at the end. After each significant change, add to "Changes Made" and note any patterns or gotchas discovered.

## Workflow Phases

All work types follow this general structure:

**Note on autonomous mode:** When running autonomously, references to "user feedback," "check in with the user," or "validate with user" should be interpreted as consulting the Oversight Agent instead. See the autonomous-skill for decision-making guidance.

### Phase 1: Understanding

**First, check accumulated memory (if it exists):**
If `docs/context/.memory/` exists, read the files for relevant context:
- `patterns.md` - Established patterns to follow
- `lessons.md` - Mistakes to avoid (especially high-severity ones)
- `gotchas.md` - Non-obvious issues in this area
- `architecture.md` - High-level structure
- `conventions.md` - Coding standards

Extract entries relevant to this task's keywords and area. Use this context to inform exploration.

If `.memory/` doesn't exist yet, skip this step - it will be created during your first flow completion.

**Then explore:**
- Clarify requirements and scope
- Explore relevant codebase areas (use hierarchical exploration for large codebases)
- Document findings in research.md (if selected)

**Also create outcome.md** with the standard template at this point.

**→ Validate with user:** Does this understanding match reality? Any corrections before planning?

### Phase 2: Planning
- Define approach and architecture
- Break down into tasks
- Document in plan.md and tasks.md (if selected)

*Iterative: refine with user feedback until the plan is solid.*

### Phase 3: Implementation
- Execute the plan systematically
- Update tasks.md (if selected) as work progresses
- **Update outcome.md after each significant change** - add to "Changes Made", note any patterns/gotchas discovered
- Maintain quality standards

*Iterative: check in with the user at logical boundaries.*

### Phase 4: Validation

Validation is a distinct phase, not a one-time check. It automatically triggers after implementation:

1. Run multi-lens review (7 parallel reviewers)
2. Fix Critical/High issues based on reviewer feedback
3. Repeat steps 1-2 until no Critical/High issues remain
4. For Medium/Low issues, ask user whether to address or defer

See [Validation](#validation) for details.

*Loop until clean or user overrides.*

### Phase 5: Completion

**Finalize outcome.md:**
- Verify success criteria met
- Polish the Summary section (should already have content from continuous updates)
- Update Status to ✅ Complete

**Extract learnings to memory:**
Analyze the work done and identify learnings for `docs/context/.memory/`:

1. **Patterns discovered** - Design patterns, architectural patterns, conventions observed
   → Append to `patterns.md` with flow reference and confidence level
2. **Lessons learned** - Mistakes made, unexpected issues, "aha moments"
   → Append to `lessons.md` with severity level
3. **Gotchas encountered** - Non-obvious issues, environment quirks
   → Append to `gotchas.md`
4. **Architecture insights** - New understanding of system structure
   → Update `architecture.md` if significant
5. **Conventions noticed** - Coding standards observed
   → Append to `conventions.md`

Check existing entries to avoid duplicates. If similar entry exists, update its confidence level instead.

**Fill in "Learnings Extracted" section of outcome.md:**
```markdown
## Learnings Extracted

### Added to Memory
- **patterns.md**: [what was added, or "nothing new"]
- **lessons.md**: [what was added, or "nothing new"]
- **gotchas.md**: [what was added, or "nothing new"]
- **architecture.md**: [what was added, or "nothing new"]
- **conventions.md**: [what was added, or "nothing new"]

### Rationale
[If nothing extracted: "Routine implementation following established patterns"]
```

A flow is not properly complete if the "Learnings Extracted" section is missing or unfilled.

## Working Style: Explore First

**Do not front-load questions.** Most information can be discovered autonomously. Only ask the user when:
- A workflow step explicitly calls for it (e.g., choosing work type or documents)
- Genuine ambiguity exists that affects the approach
- A decision requires user preference
- You've exhausted available sources (codebase, databases, web search, docs) and still lack critical info

Bad: "What are the requirements? What patterns exist? What files are involved?"
Good: *Explore the codebase first, then* "I found X and Y patterns. Should we follow X or try something new?"

## Techniques

Reusable techniques that apply across work types and phases:

| Technique | When to Use | Reference |
|-----------|-------------|-----------|
| **Hierarchical Exploration** | Large codebases, understanding patterns across modules | [techniques/hierarchical-exploration.md](techniques/hierarchical-exploration.md) |
| **State Machine Diagrams** | Components with multiple states, cross-system flows, design or verification | [techniques/state-machines.md](techniques/state-machines.md) |

These techniques help manage context and force comprehensive thinking. Apply them proactively when the situation calls for it.

## Validation

Before completing implementation, run multi-lens validation to catch issues across different dimensions.

**Manual:** User invokes `/validate` at any time.

**Automatic:** At the end of Phase 3 (Implementation), before transitioning to Completion.

The validation skill spawns parallel reviewer subagents, each examining changes through a different lens:
- **Security** - Vulnerabilities, injection, auth issues
- **Architecture** - Design patterns, coupling, layer violations
- **Quality** - Duplication, naming, complexity, CLAUDE.md compliance
- **Performance** - Algorithms, queries, bottlenecks
- **Scalability** - Concurrency, state, distributed concerns
- **Testing** - Coverage, test quality, edge cases
- **Error Handling** - Robustness, graceful degradation

Results are aggregated by severity (Critical > High > Medium > Low). Critical issues block completion; High issues are recommended fixes; Medium/Low are advisory.

See `/validate` command and `skills/validation-skill/` for implementation details.

## Roadmap Integration

Flows can be linked to roadmap items for strategic tracking. Use `/flow-roadmap` to manage the strategic backlog.

### Starting a Flow with Roadmap Link

```bash
/flow feature "implement user auth" --roadmap RM-001
# or reference directly
/flow work on RM-001
```

**When a flow references a roadmap item:**
1. Read roadmap item for context (description, acceptance criteria)
2. Add to plan.md:
   ```markdown
   ## Roadmap Reference
   - **Item**: RM-001 (User Authentication System)
   - **Acceptance Criteria**: [copied from roadmap item]
   ```
3. Update roadmap item status: planned → in-progress
4. Add flow to roadmap item's Linked Flows section

### Flow Completion with Roadmap Link

When finalizing a flow that's linked to a roadmap item:

1. Update roadmap item's Linked Flows with outcome
2. Check acceptance criteria against accomplishments
3. If all criteria met: prompt to mark roadmap item completed
4. Update roadmap item's History section

This is **required** behavior during flow finalization when a roadmap link exists.

## Context Hygiene

**Use `/compact` proactively** at logical boundaries (after completing a phase, before starting a new one). Guide what to preserve:

```
/compact Preserve: the patterns we discovered, the implementation plan, current progress. Summarize: file exploration details and debugging attempts.
```

**Use `/clear` between unrelated tasks.** Context from the previous task is noise for the next one. Starting fresh is cheap; carrying forward pollution is expensive.

**Delegate verbose operations.** Anything that produces large output (running tests, analyzing logs, searching many files) belongs in a subagent that returns a summary.

## Anti-Patterns

**The yell-loop:** Agent fails, you correct, agent fails again, you correct harder. Each iteration adds noise. The fix is `/clear` and restart with a cleaner prompt.

**File dumps:** Reading entire large files when you only need specific sections. Use targeted reads or delegate to a subagent.

**Log accumulation:** Build output, test results, and error logs piling up in context. Delegate test runs to subagents. Clear after resolving issues.

**Lazy prompting:** Quality degrades when you stop putting effort into prompts. If you're getting poor output, reflect on what context you're actually providing.

## Type-Specific Guidance

The work type files provide **additive guidance** for specific work types. They do not override the phases and principles defined in this skill - they supplement them.

**How to read work type files:**
- If a work type file mentions a phase, apply that guidance **in addition to** the general phase guidance above
- If a work type file omits a phase, use the general guidance from this skill
- Universal aspects (iterative nature, validation loop, memory extraction) always apply regardless of work type

For detailed guidance on each work type, see:
- [Greenfield Projects](types/greenfield.md)
- [Feature Development](types/feature.md)
- [Integration](types/integration.md)
- [Refactoring](types/refactor.md)
- [Optimization](types/optimization.md)
- [Bugfix](types/bugfix.md)
- [Custom](types/custom.md)

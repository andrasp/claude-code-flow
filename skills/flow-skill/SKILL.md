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
| Greenfield | `docs/context/greenfield/` | [greenfield.md](greenfield.md) |
| Feature | `docs/context/feature/` | [feature.md](feature.md) |
| Integration | `docs/context/integration/` | [integration.md](integration.md) |
| Refactor | `docs/context/refactor/` | [refactor.md](refactor.md) |
| Optimization | `docs/context/optimization/` | [optimization.md](optimization.md) |
| Bugfix | `docs/context/bugfix/` | [bugfix.md](bugfix.md) |
| Custom | `docs/context/custom/` | [custom.md](custom.md) |

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
| `research.md` | Analysis, findings, raw data | Optional - User chooses |
| `tasks.md` | Granular task tracking with checkboxes | Optional - User chooses |
| `outcome.md` | Record of completed work, lessons learned | Optional - User chooses |

## Workflow Phases

All work types follow this general structure with human validation at each boundary:

### Phase 1: Understanding
- Clarify requirements and scope
- Explore relevant codebase areas (use hierarchical exploration for large codebases)
- Document findings in research.md

**→ Validate with user:** Does this understanding match reality? Any corrections before planning?

### Phase 2: Planning
- Define approach and architecture
- Break down into tasks
- Document in plan.md and tasks.md

**→ Validate with user:** Does this plan match intent? Does it fit the architecture?

### Phase 3: Implementation
- Execute tasks systematically
- Update tasks.md as work progresses
- Maintain quality standards
- Run self-review before completion

**→ Validate with user:** Does implementation match the plan? Any drift detected?

### Phase 4: Completion
- Verify success criteria met
- Document outcomes in outcome.md
- Capture lessons learned

## Working Style: Explore First

**Do not front-load questions.** Most information can be discovered autonomously. Only ask the user when:
- A workflow step explicitly calls for it (e.g., choosing work type or documents)
- Genuine ambiguity exists that affects the approach
- A decision requires user preference
- You've exhausted available sources (codebase, databases, web search, docs) and still lack critical info

Bad: "What are the requirements? What patterns exist? What files are involved?"
Good: *Explore the codebase first, then* "I found X and Y patterns. Should we follow X or try something new?"

## Hierarchical Exploration

For large codebases, use subagents in a hierarchical rollup pattern. This preserves main session context while still reaching low-level code details.

**Why delegate:** Your main session is an orchestrator, not a workhorse. Reading 15 files directly costs ~80K tokens. A subagent reading those files and returning a summary costs ~5K tokens in your main session.

**The pattern:**

```
Level 1: Parallel exploration subagents
├── Subagent A: Explore auth module → returns summary
├── Subagent B: Explore API routes → returns summary
├── Subagent C: Explore data layer → returns summary
└── Subagent D: Explore UI components → returns summary

Level 2: Synthesis subagents (if needed)
├── Subagent E: Combine A + B findings → architectural summary
└── Subagent F: Combine C + D findings → data flow summary

Level 3: Final synthesis
└── Main session: Integrate all summaries into coherent understanding
```

**When to use hierarchical exploration:**
- Codebase has many files across multiple modules
- You need to understand patterns across different areas
- Direct file reading would consume too much context

**How to delegate:**
- Use Task agents or Explore agents for heavy reading
- Give each agent a focused scope (one module, one concern)
- Request summaries, not raw file dumps
- Run independent explorations in parallel
- If context matters, include relevant plan details in the prompt or tell the agent to read plan.md

**Note:** Subagents don't need the flow skill. They're workers executing focused tasks. The main session is the orchestrator that follows flow and coordinates the subagents.

## Self-Review

Before completing significant implementation work, spawn a review agent to check for issues:

```
Launch a Task agent to review the changes:
- Check consistency with codebase patterns
- Look for missing error handling or edge cases
- Verify implementation matches the plan
- Return a summary of any issues found
```

The review agent runs in fresh context, bringing objective perspective. This catches drift before it compounds.

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

For detailed guidance on each work type, see:
- [Greenfield Projects](greenfield.md)
- [Feature Development](feature.md)
- [Integration](integration.md)
- [Refactoring](refactor.md)
- [Optimization](optimization.md)
- [Bugfix](bugfix.md)
- [Custom](custom.md)

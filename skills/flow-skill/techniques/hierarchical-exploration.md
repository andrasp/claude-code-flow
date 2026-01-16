# Hierarchical Exploration

For large codebases, use subagents in a hierarchical rollup pattern. This preserves main session context while still reaching low-level code details.

## Why

Your main session is an orchestrator, not a workhorse. Reading 15 files directly costs ~80K tokens. A subagent reading those files and returning a summary costs ~5K tokens in your main session.

Context is finite and must be managed deliberately. A 200K token window can't hold a production codebase. When context becomes saturated with file dumps and debug output, quality degrades.

## The Pattern

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

## When to Use

- Codebase has many files across multiple modules
- You need to understand patterns across different areas
- Direct file reading would consume too much context
- Running tests, analyzing logs, or searching many files

## How to Delegate

- Use Task agents or Explore agents for heavy reading
- Give each agent a focused scope (one module, one concern)
- Request summaries, not raw file dumps
- Run independent explorations in parallel
- If context matters, include relevant plan details in the prompt or tell the agent to read plan.md

## What Good Summaries Include

**Test runs:**
- Overall pass/fail counts
- Each failing test: name, file location, assertion that failed
- Error messages (deduplicated if repeated)
- Patterns observed ("all failures involve database connections")

**Log analysis:**
- Error types and frequencies
- Specific error messages (deduplicated)
- Time patterns, affected services
- Correlations or likely root causes

**Code search:**
- Where the pattern appears (files, functions, line numbers)
- How it's used in each context
- Usage patterns ("mostly in controllers, some in tests")

**Build errors:**
- Each error with file:line and the actual message
- What each error means / likely cause
- Dependencies between errors

## Anti-Pattern: File Dumps

Don't do this:
```
Main session reads file1.ts (2000 lines)
Main session reads file2.ts (1500 lines)
Main session reads file3.ts (800 lines)
...
Context exhausted, quality degrading
```

Do this instead:
```
Subagent reads files 1-5, returns: "Auth module uses JWT with refresh tokens,
validates in middleware, stores in Redis. Key files: auth.ts:45, middleware.ts:120"

Main session receives 50 tokens instead of 10000
```

## Note

Subagents don't need the flow skill. They're workers executing focused tasks. The main session is the orchestrator that follows flow and coordinates the subagents.

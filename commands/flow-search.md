---
description: Search past flows and accumulated memory for relevant context, patterns, and lessons learned
argument-hint: <search query or keywords>
---

# /flow-search - Search Past Flows and Memory

You are searching through past development workflows and accumulated memory to find relevant context, patterns, and lessons learned.

## Step 1: Get Search Query

**If the user provided a query (argument $1 exists):**
Use the provided query directly.

**If no query was provided:**
Ask the user: "What would you like to search for?"

## Step 2: Search (Subagent)

**Critical: Delegate all searching to a subagent to preserve main session context.**

Spawn a Task agent with subagent_type="Explore" to search `docs/context/`. The subagent should search two areas:

### 2a. Search Past Flows

1. **Find all flow directories:**
   ```
   docs/context/**/plan.md
   docs/context/**/outcome.md
   ```

2. **Extract keywords from the search query** and grep for matches across plan.md and outcome.md files.

3. **For each matching flow directory:**
   - Note the path (contains type + date + topic): `<type>/YYYY-MM-DD_<topic>/`
   - From plan.md: extract the Overview and Goals sections
   - If outcome.md exists: extract the Summary and Lessons Learned sections
   - Determine status: has outcome.md = likely completed, otherwise in-progress

### 2b. Search Memory

1. **Search memory files:**
   ```
   docs/context/.memory/patterns.md
   docs/context/.memory/lessons.md
   docs/context/.memory/gotchas.md
   docs/context/.memory/architecture.md
   docs/context/.memory/conventions.md
   ```

2. **Extract matching entries** from each file that relate to the search query.

### 2c. Return Results

**Return a structured summary** (NOT raw file contents):

```
Found N flows and M memory entries matching "<query>":

**Past Flows:**
1. <type>/<date>_<topic>/ [status]
   Goal: <extracted from plan.md>
   Outcome: <extracted from outcome.md if exists>

**From Memory:**
- [patterns.md]: <relevant pattern>
- [gotchas.md]: <relevant gotcha>
```

**Subagent prompt template:**

```
Search for past work related to: "<query>"

Search in: docs/context/

**Part 1: Past Flows**
For each flow directory found:
1. Grep for these keywords in plan.md and outcome.md: [extracted keywords]
2. For matches, read first 30 lines of plan.md (Goal/Overview section)
3. Check if outcome.md exists - if so, read first 30 lines (Summary/Lessons)
4. Note the path which contains: type, date (YYYY-MM-DD), and topic

**Part 2: Memory**
Search docs/context/.memory/ files (patterns.md, lessons.md, gotchas.md, architecture.md, conventions.md) for relevant entries.

Return a structured summary with:
- Flow matches: path, status, goal, outcome/lessons
- Memory matches: file, relevant entry

Return only genuinely relevant matches (max 10 flows, max 5 memory entries), sorted by relevance.
If nothing is truly relevant, say "no matches found" - don't force matches.
Do NOT return raw file contents - summarize.
```

## Step 3: Present Results

When the subagent returns, present the results to the user:

**If matches found:**

```
Found [N] past flows and [M] memory entries related to "[query]":

**Past Flows:**
1. **[type]/[date]_[topic]** [completed/in-progress]
   Goal: [summary]
   Outcome: [if available]

**From Memory:**
- **[patterns.md]**: [relevant pattern summary]
- **[gotchas.md]**: [relevant gotcha summary]

Would you like me to dive deeper into any of these?
```

**If no matches:**

```
No matches found for "[query]".

You can:
- Try different keywords
- Use `/flow` to start a new workflow for this topic
```

## Step 4: Dive Deeper (If Requested)

If the user wants to explore a specific past flow:

1. Read the full plan.md and outcome.md (if exists) from that flow
2. Summarize the approach taken, key decisions, and lessons learned
3. Highlight anything relevant to their current work

If the user wants to continue/resume that flow:
- Point them to use the flow-skill by referencing the path: "continue docs/context/[path]"

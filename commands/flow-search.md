---
description: Search past flow work for relevant context, patterns, and lessons learned
argument-hint: <search query or keywords>
---

# /flow-search - Search Past Flows

You are searching through past development workflows to find relevant context, patterns, and lessons learned.

## Step 1: Get Search Query

**If the user provided a query (argument $1 exists):**
Use the provided query directly.

**If no query was provided:**
Ask the user: "What would you like to search for in past flows?"

## Step 2: Search Past Flows (Subagent)

**Critical: Delegate all searching to a subagent to preserve main session context.**

Spawn a Task agent with subagent_type="Explore" to search `docs/context/`. The subagent should:

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

4. **Return a structured summary** (NOT raw file contents):

```
Found N flows matching "<query>":

1. <type>/<date>_<topic>/ [status]
   Goal: <extracted from plan.md>
   Outcome: <extracted from outcome.md if exists>

2. ...
```

**Subagent prompt template:**

```
Search for past flow work related to: "<query>"

Search in: docs/context/

For each flow directory found:
1. Grep for these keywords in plan.md and outcome.md: [extracted keywords]
2. For matches, read first 30 lines of plan.md (Goal/Overview section)
3. Check if outcome.md exists - if so, read first 30 lines (Summary/Lessons)
4. Note the path which contains: type, date (YYYY-MM-DD), and topic

Return a structured summary with:
- Flow path (type/date_topic)
- Status (completed if outcome.md exists, in-progress otherwise)
- Goal (from plan.md)
- Outcome/Lessons (from outcome.md if available)

Return only genuinely relevant matches (max 10), sorted by relevance then recency.
If nothing is truly relevant, say "no related flows found" - don't force matches.
Do NOT return raw file contents - summarize.
```

## Step 3: Present Results

When the subagent returns, present the results to the user:

**If matches found:**

```
Found [N] past flows related to "[query]":

1. **[type]/[date]_[topic]** [completed/in-progress]
   Goal: [summary]
   Outcome: [if available]

2. ...

Would you like me to dive deeper into any of these?
```

**If no matches:**

```
No past flows found matching "[query]".

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

---
name: autonomous-skill
description: Enables fully autonomous flow execution without human intervention. Sets up hooks in the user's project and provides Oversight Agent guidance.
allowed-tools: Read, Write, Bash(mkdir:*), Bash(chmod:*), Glob, Grep, Task, AskUserQuestion
---

# Autonomous Skill - Unattended Flow Execution

This skill enables autonomous mode where flows run to completion without human intervention. An Oversight Agent makes judgment calls that would normally require human input.

**Status: Experimental** - Use for well-defined, lower-risk tasks.

## Setup in User's Project

When `/flow --autonomous` is first invoked, check if hooks are configured. If not, set them up.

### Check for Existing Setup

```bash
# Check if hooks are configured
if [ -f ".claude/hooks/permission-handler.sh" ] && [ -f ".claude/hooks/stop-handler.sh" ]; then
  echo "Hooks already configured"
else
  echo "First-time setup required"
fi
```

### First-Time Setup

Create the following files in the user's project:

#### 1. Permission Handler (`.claude/hooks/permission-handler.sh`)

```bash
#!/bin/bash
# Permission hook for autonomous mode
# Returns "allow" in autonomous mode, "ask" otherwise

if [ -f ".claude/.autonomous-mode" ]; then
  echo '{"hookSpecificOutput":{"hookEventName":"PermissionRequest","decision":{"behavior":"allow"}}}'
else
  echo '{"hookSpecificOutput":{"hookEventName":"PermissionRequest","decision":{"behavior":"ask"}}}'
fi
```

#### 2. Stop Handler (`.claude/hooks/stop-handler.sh`)

```bash
#!/bin/bash
# Stop hook for autonomous mode (Ralph Wiggum pattern)
# In autonomous mode: reinject prompt to keep iterating
# In human mode: allow normal exit

if [ -f ".claude/.autonomous-mode" ]; then
  # Read the marker file for completion condition
  COMPLETION_MARKER=$(cat .claude/.autonomous-mode 2>/dev/null)

  # Check if completion was signaled
  if [ "$COMPLETION_MARKER" = "COMPLETE" ]; then
    # Task marked complete - allow exit and clean up
    rm -f .claude/.autonomous-mode
    exit 0
  fi

  # Not complete - reinject prompt to continue
  # Exit code 2 tells Claude Code to reinject the prompt
  exit 2
else
  # Human mode - allow normal exit
  exit 0
fi
```

#### 3. Settings Configuration (`.claude/settings.json`)

Append or merge into existing settings:

```json
{
  "permissions": {
    "deny": [
      "Read(./.env*)",
      "Read(./secrets/**)",
      "Bash(rm -rf /*)",
      "Bash(rm -rf ~/*)",
      "Bash(git push --force:*)",
      "Bash(git push * --force:*)",
      "Bash(git push origin main:*)",
      "Bash(git push origin master:*)"
    ]
  },
  "hooks": {
    "PermissionRequest": [
      {
        "type": "command",
        "command": ".claude/hooks/permission-handler.sh"
      }
    ],
    "Stop": [
      {
        "type": "command",
        "command": ".claude/hooks/stop-handler.sh"
      }
    ]
  }
}
```

#### 4. After Setup

```
Autonomous mode configured. Please restart with `claude --resume` to continue.

(Hooks are loaded at session start and do not hot-reload)
```

## Enabling Autonomous Mode

After hooks are set up, to start autonomous mode:

1. Create marker file: `touch .claude/.autonomous-mode`
2. Start the flow normally
3. Hooks will auto-allow permissions and reinject prompts

## Disabling Autonomous Mode

To exit autonomous mode:

1. Write "COMPLETE" to marker: `echo "COMPLETE" > .claude/.autonomous-mode`
2. The stop hook will clean up and allow exit

Or manually: `rm .claude/.autonomous-mode`

## Oversight Agent

In autonomous mode, you act as the Oversight Agent - making decisions that would normally require human input.

### Decision Framework

#### Phase Transitions
- Understanding → Planning: Approve if goals and context documented
- Planning → Implementation: Approve if plan has clear tasks
- Implementation → Completion: Approve if tasks complete and validation passes

#### Clarifying Questions
When a question arises:
1. Check if answer exists in: plan.md, roadmap item, CLAUDE.md
2. If clear answer: use it
3. If reasonable default exists: use it, document assumption
4. If genuinely ambiguous: exit autonomous mode, ask human

#### Implementation Options
When multiple approaches valid:
1. Check CLAUDE.md for preferences
2. Check codebase for established patterns
3. Prefer simpler approach
4. Document rationale in outcome.md

#### Validation Findings
- Critical/High: Attempt auto-remediation (max 3 attempts)
- Medium/Low: Document, continue

### Blocking Conditions

Exit autonomous mode and ask human if:
- Critical issues can't be auto-remediated after 3 attempts
- Genuine ambiguity with no reasonable default
- Security-sensitive decisions
- Destructive operations not covered by deny rules

### Decision Logging

Document all autonomous decisions in a dedicated `autonomous-log.md` file in the flow's context directory:

```markdown
# Autonomous Flow Log

## Flow: feature/2025-01-08_user-profile
## Mode: Autonomous
## Started: 2025-01-08 14:30:00
## Completed: 2025-01-08 15:12:00

### Decision Log

#### Decision 1: Phase Transition (Understanding → Planning)
- **Time**: 14:35:00
- **Decision**: Approve
- **Rationale**: Goals documented, context sufficient
- **Confidence**: High

#### Decision 2: Implementation Approach
- **Time**: 14:42:00
- **Question**: Use existing UserCard component or create new?
- **Decision**: Extend existing UserCard
- **Rationale**: CLAUDE.md prefers extending over creating, pattern exists
- **Assumptions**: UserCard is flexible enough for profile use case
- **Confidence**: Medium

#### Decision 3: Validation Remediation
- **Time**: 15:01:00
- **Issue**: Missing null check (Medium severity)
- **Decision**: Auto-remediate
- **Fix Applied**: Added optional chaining
- **Re-validation**: Passed
- **Confidence**: High

### Final Outcome
- **Status**: Completed
- **Human Interventions**: 0
- **Remediation Cycles**: 1
- **Total Decisions**: 7
- **Assumptions Made**: 2
```

## Completing Autonomous Flow

When flow is complete:

1. Verify all acceptance criteria met
2. Finalize autonomous-log.md with final outcome summary
3. Update outcome.md normally (without autonomous decision details)
4. Exit autonomous mode: `echo "COMPLETE" > .claude/.autonomous-mode`
   - Stop hook sees "COMPLETE", removes the marker file, allows normal exit
   - Permission hook no longer auto-allows (marker gone)
   - Session returns to human mode with normal permission prompts


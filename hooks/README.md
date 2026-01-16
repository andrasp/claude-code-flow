# Hooks

## detect-workflow.py

A `UserPromptSubmit` hook that analyzes user prompts and injects workflow-specific guidance into Claude's context.

### How It Works

1. **Input**: Receives JSON on stdin with the user's prompt:
   ```json
   {"prompt": "fix this null pointer bug", ...}
   ```

2. **Detection**: Scans the prompt for keywords matching work types:
   - `bugfix` — error, bug, fix, crash, broken, failing, issue, debug, etc.
   - `refactor` — refactor, restructure, reorganize, clean up, simplify, etc.
   - `optimization` — optimize, performance, speed, slow, memory, cache, etc.
   - `feature` — add, implement, create, build, new feature, etc.
   - `greenfield` — new project, from scratch, bootstrap, scaffold, etc.
   - `integration` — integrate, connect, API, webhook, third-party, etc.
   - `state_machine` — state machine, state diagram, lifecycle, design component/system/flow, transitions, etc.

3. **Output**: Returns JSON that injects guidance into Claude's context:
   ```json
   {
     "hookSpecificOutput": {
       "hookEventName": "UserPromptSubmit",
       "additionalContext": "[Workflow guidance injected by hook]\n\n..."
     }
   }
   ```

   If no work type is detected, returns `{"continue": true}` to proceed without injection.

### Multiple Matches

The hook can detect multiple work types in a single prompt. For example, "refactor this and fix the bug" would inject both refactor and bugfix guidance.

### Error Handling

The hook fails open — any exceptions are logged to stderr and the hook exits with code 0, allowing the prompt to proceed normally without blocking the user.

### Installation

Symlink to `~/.claude/hooks/` and configure in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/detect-workflow.py"
          }
        ]
      }
    ]
  }
}
```

### Dependencies

- Python 3.x (standard library only — uses `json`, `re`, `sys`)

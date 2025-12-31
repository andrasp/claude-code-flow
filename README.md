# Claude Code Flow

*Stay in the flow.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A structured but flexible development workflow system for Claude Code. Guides you through feature development, refactoring, optimization, greenfield projects, and bugfixes with consistent documentation practices.

Extends the research → plan → implement paradigm, keeping Claude laser focused on relevant context while solving the chronic amnesia problem in long sessions.

## What It Does

The `/flow` command initiates structured workflows that:

- **Defeat Claude's amnesia** - context persists in documentation that survives session resets, context compaction, and timeouts
- **Resume instantly** - reference a `docs/context/` path and pick up exactly where you left off, even days later
- **Stay on track** - phased workflows (understand → plan → implement → complete) with validation checkpoints prevent drift
- **Get tailored guidance** - type-specific workflows for features, bugfixes, refactors, integrations, and more
- **Reduce cognitive load** - Claude explores your codebase first, only asking questions when genuinely blocked

## What's Included

- **`/flow` command** - initiates new workflows, infers work type from your description
- **`flow-skill` skill** - auto-activates when you reference a context directory path
  - Phase-by-phase guidance: understanding → planning → implementation → completion
  - Progressive disclosure: Claude sees only what's relevant to the current phase
  - Work-type specific: tailored guidance for features, refactors, optimizations, etc.

## Work Types

| Type | When to Use |
|------|-------------|
| **Greenfield** | New component/system from scratch |
| **Feature** | New feature added to existing codebase |
| **Integration** | Connect with external APIs, services, or systems |
| **Refactor** | Restructure or reorganize existing code |
| **Optimization** | Performance, efficiency, resource usage |
| **Bugfix** | Fix a specific issue or defect |
| **Custom** | User-defined focus; doesn't fit above categories |

## Context Directory Structure

Each workflow automatically creates and maintains a timestamped directory with standardized documents:

```
docs/context/
├── feature/
│   ├── 2025-01-15_user-authentication/
│   │   ├── plan.md
│   │   ├── research.md
│   │   ├── tasks.md
│   │   ├── outcome.md
│   │   └── api_design.md
│   └── 2025-01-22_export-api/
│       ├── plan.md
│       └── tasks.md
├── bugfix/
│   └── 2025-01-18_login-timeout/
│       ├── plan.md
│       └── research.md
├── optimization/
│   └── 2025-01-20_query-performance/
│       ├── plan.md
│       ├── research.md
│       └── tasks.md
└── refactor/
    └── 2025-01-10_payment-module/
        ├── plan.md
        ├── research.md
        ├── tasks.md
        └── outcome.md
```

Standard documents:
- **plan.md** - Implementation plan, goals, success criteria
- **research.md** - Analysis and findings from codebase exploration
- **tasks.md** - Task tracking with checkboxes
- **outcome.md** - Results and lessons learned

For simple tasks, you may skip documents that wouldn't add value - but most workflows benefit from all four.

Additional documents can be created as needed (e.g., `api_design.md`, `notes.md`, `diagrams.md`).

## Auto-Activation

The flow-skill automatically activates when you reference a `docs/context/` path (e.g., "let's continue working on docs/context/bugfix/2025-01-18_login-timeout"). Claude detects the work type from the directory path and loads the appropriate guidance.

## Installation

Clone this repo and symlink to your Claude Code configuration:

```bash
git clone https://github.com/andrasp/claude-code-flow.git
ln -s /path/to/claude-code-flow/commands ~/.claude/commands
ln -s /path/to/claude-code-flow/skills ~/.claude/skills
```

Start a new conversation and the commands and skills will be available.

## Usage

```bash
# Interactive mode - shows work type menu
/flow

# With description - infers work type
/flow add user authentication to the API
```

## Repository Structure

```
claude-code-flow/
├── commands/
│   └── flow.md           # /flow slash command
└── skills/
    └── flow-skill/
        ├── SKILL.md      # Main skill definition
        ├── bugfix.md     # Bugfix guidance
        ├── feature.md    # Feature development guidance
        ├── greenfield.md # Greenfield project guidance
        ├── integration.md # Integration guidance
        ├── optimization.md # Optimization guidance
        ├── custom.md     # General workflow, user-defined focus
        └── refactor.md   # Refactoring guidance
```

## See It In Action

Starting a new greenfield project with `/flow`:

**Step 1: Choose work category**

![Work category selection](.github/assets/screen1.png)

**Step 2: Select specific type**

![Build type selection](.github/assets/screen2.png)

**Step 3: Define purpose**

![Purpose selection](.github/assets/screen3.png)

**Step 4: Complexity assessment & document selection**

![Complexity and documents](.github/assets/screen4.png)

**Step 5: Context created, workflow begins**

![Workflow initialized](.github/assets/screen5.png)

The context directory is created, documents are initialized, and Claude begins Phase 1 with architecture decisions tailored to your project.

## Related

- [claude-code-wisdom](https://github.com/andrasp/claude-code-wisdom) - Distilled software engineering wisdom for your CLAUDE.md

## License

MIT License - use however you want.

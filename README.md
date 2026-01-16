# Claude Code Flow

*Stay in the flow.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A structured workflow system for Claude Code. Guides you through feature development, refactoring, optimization, greenfield projects, integrations, and bugfixes with consistent documentation practices.

Extends the research → plan → implement paradigm, keeping Claude laser focused on relevant context while solving the chronic amnesia problem in long sessions.

## What It Does

The `/flow` command initiates structured workflows that:

- **Defeat Claude's amnesia** - context persists in documentation that survives session resets, context compaction, and timeouts
- **Resume instantly** - reference a `docs/context/` path and pick up exactly where you left off, even days later
- **Learn from past work** - patterns, lessons, and gotchas accumulate in `.memory/` and inform future flows
- **Stay on track** - phased workflows (understand → plan → implement → validate → complete) prevent drift
- **Get tailored guidance** - type-specific workflows for features, bugfixes, refactors, integrations, and more
- **Reduce cognitive load** - Claude explores your codebase first, only asking questions when genuinely blocked
- **Scale to large codebases** - hierarchical exploration delegates heavy reading to subagents, keeping your main session focused


## Core Workflow

### How It Works

Every flow follows the same phased structure:

1. **Understanding** - Explore the codebase, read documentation, search the web, check databases - whatever sources are relevant. Trace data flows, identify integration points, understand existing patterns. Ask questions when genuine ambiguity remains. Document findings in `research.md` (if selected).

2. **Planning** - Define the implementation approach based on what you learned. Break work into concrete tasks with clear acceptance criteria. Document in `plan.md` and `tasks.md` (if selected). *Iterative: refine with user feedback until the plan is solid.*

3. **Implementation** - Execute the plan, updating `tasks.md` (if selected) as you go. Follow established codebase patterns. Keep changes focused - don't refactor unrelated code. *Iterative: check in with the user at logical boundaries.*

4. **Validation** - Automatically triggers 7 parallel reviewers (security, architecture, quality, performance, scalability, testing, error-handling). Fix Critical/High issues, then revalidate. *Loop until clean or user overrides.* This is a distinct phase, not a one-time check.

5. **Completion** - Verify all success criteria are met. Document results in `outcome.md` including what was accomplished, files changed, and lessons learned. Extract patterns and insights to `.memory/` for future flows.

### Work Types

| Type | When to Use |
|------|-------------|
| **Greenfield** | New component/system from scratch |
| **Feature** | New feature added to existing codebase |
| **Integration** | Connect with external APIs, services, or systems |
| **Refactor** | Restructure or reorganize existing code |
| **Optimization** | Performance, efficiency, resource usage |
| **Bugfix** | Fix a specific issue or defect |
| **Custom** | User-defined focus; doesn't fit above categories |

### Context Directory

Each workflow creates a timestamped directory. You choose which optional documents to include:

```
docs/context/
├── .memory/                              # Cross-session learning (see Memory System)
├── roadmap/                              # Strategic backlog (see Roadmap extension)
├── feature/
│   └── 2025-01-15_user-authentication/
│       ├── research.md                   # Analysis and findings (optional)
│       ├── plan.md                       # Goals, approach, success criteria (always created)
│       ├── tasks.md                      # Progress tracking (optional)
│       └── outcome.md                    # Results and lessons (always created)
├── greenfield/
├── integration/
├── bugfix/
├── refactor/
├── optimization/
└── custom/
```

**Visual interface available:** [Claude Code Flow UI](https://github.com/andrasp/claude-code-flow-ui) provides a desktop app for browsing flows and their documentation.

![Flow Detail](https://raw.githubusercontent.com/andrasp/claude-code-flow-ui/main/assets/screenshots/flow-detail.png)

### Auto-Activation

Two mechanisms ensure guidance is always available:

**Skill activation** - The flow-skill activates when you reference a `docs/context/` path (e.g., "let's continue working on docs/context/bugfix/2025-01-18_login-timeout"). Claude detects the work type from the directory path and loads the appropriate guidance.

**Hook detection** - The detect-workflow hook analyzes every prompt for work-type keywords and injects relevant guidance automatically. Say "fix the login bug" and bugfix guidance applies - even without starting a formal `/flow` session.

### Searching Past Work

Find relevant context from previous flows and accumulated memory:

```bash
/flow-search authentication
/flow-search "caching patterns"
```

Searches both past flows (goals, outcomes, lessons) and `.memory/` (patterns, gotchas, conventions). Useful for checking "have I done this before?" or finding patterns to reuse. You can dive deeper into any result or resume a previous flow directly.

### Memory System

Flow learns from your work. The `.memory/` directory accumulates knowledge across flows - patterns discovered, lessons learned, gotchas encountered. Claude reads it at the start of each flow and writes to it at the end. You never interact with it directly.

```
docs/context/.memory/
├── patterns.md      # Reusable solutions (auth strategy, error handling, etc.)
├── lessons.md       # What worked, what didn't
├── architecture.md  # System structure insights
├── conventions.md   # Naming, file organization, code style
└── gotchas.md       # Project-specific pitfalls
```

**How it works:**
- **Flow start**: Claude reads `.memory/` to inform understanding and planning
- **Flow end**: Lessons and patterns are extracted to `.memory/` for future flows
- **Invisible**: You don't manage it directly; Claude reads/writes automatically

The memory is project-specific. Committing it to version control shares accumulated knowledge across the team, though concurrent flows may cause merge conflicts in memory files.

**Visual interface available:** [Claude Code Flow UI](https://github.com/andrasp/claude-code-flow-ui) provides a desktop app for exploring accumulated memory.

![Memory Explorer](https://raw.githubusercontent.com/andrasp/claude-code-flow-ui/main/assets/screenshots/memory.png)

## Validation

Multi-lens code review through **parallel specialist reviewers**, each examining changes through a different lens.

```bash
/validate                        # Reviews uncommitted changes
/validate src/auth/              # Reviews specific files or directories
```

**7 Reviewers:**
| Reviewer | Focus |
|----------|-------|
| Security | Vulnerabilities, injection, auth issues |
| Architecture | Design patterns, coupling, layer violations, CLAUDE.md compliance |
| Quality | Duplication, naming, complexity, CLAUDE.md compliance |
| Performance | Algorithms, queries, bottlenecks |
| Scalability | Concurrency, state, distributed concerns |
| Testing | Coverage, test quality, edge cases |
| Error Handling | Robustness, graceful degradation |

Findings are aggregated by severity (Critical > High > Medium > Low). Critical/High issues can be auto-remediated. Runs automatically before flow completion, or manually anytime via `/validate`.

## Autonomous Mode (Experimental)

Run flows to completion without human intervention. An Oversight Agent makes judgment calls that would normally require human input.

```bash
/flow feature "add user profiles" --autonomous
```

#### When to Use

| Good Candidates | Poor Candidates |
|-----------------|-----------------|
| Well-defined tasks with clear acceptance criteria | Ambiguous requirements |
| Tasks similar to previously completed flows | High-risk changes (payments, auth, data migrations) |
| Lower-risk changes (non-critical systems) | Novel architectural decisions |
| After-hours or async work | Security-sensitive changes |

#### How It Works

First run configures hooks in your project (`.claude/hooks/`). These hooks auto-allow permissions and reinject prompts until completion. A marker file (`.claude/.autonomous-mode`) controls active state. Session restart required after initial setup since hooks load at start.

The Oversight Agent makes decisions at phase boundaries: approving transitions when documentation is sufficient, following CLAUDE.md preferences for implementation choices, and auto-remediating Critical/High validation findings (max 3 attempts). When genuinely ambiguous, it exits autonomous mode and asks the human.

All decisions are logged in `autonomous-log.md` within the flow's context directory.

See [autonomous-skill/SKILL.md](skills/autonomous-skill/SKILL.md) for full details.

## Extensions

Optional features that work independently of `/flow` but integrate with it.

### Roadmap

Strategic work planning above individual flows. While `/flow` manages isolated pieces of work, `/flow-roadmap` manages the **strategic backlog** - a prioritized list with dependencies and progress tracking.

```bash
/flow-roadmap                              # Show overview
/flow-roadmap list --priority=P0,P1        # List high priority items
/flow-roadmap add "User authentication"    # Add new item
/flow-roadmap next                         # What should I work on?
/flow-roadmap depends RM-004 --on RM-001   # Add dependency
/flow --roadmap RM-001                     # Start flow linked to roadmap item
```

Natural language works too: "X depends on Y", "what's most important?", "the API work is blocked".

Roadmap items live in `docs/context/roadmap/` with priorities (P0-P3), effort estimates (XS-XL), dependencies, and acceptance criteria. When flows complete, linked roadmap items update automatically.

**Visual interface available:** [Claude Code Flow UI](https://github.com/andrasp/claude-code-flow-ui) provides a desktop app with Kanban board and timeline views for roadmap planning.

![Roadmap Board](https://raw.githubusercontent.com/andrasp/claude-code-flow-ui/main/assets/screenshots/roadmap-board.png)

![Roadmap Timeline](https://raw.githubusercontent.com/andrasp/claude-code-flow-ui/main/assets/screenshots/roadmap-timeline.png)

## Usage

```bash
# Start a new workflow
/flow
/flow add user authentication to the API

# Search past flows
/flow-search authentication
/flow-search caching patterns

# Resume previous work
continue docs/context/feature/2025-01-15_user-auth

# Strategic planning
/flow-roadmap
/flow-roadmap next
/flow --roadmap RM-001

# Code review
/validate
/validate src/auth/

# Autonomous execution
/flow feature "add logout button" --autonomous
```

## Repository Structure

```
claude-code-flow/
├── commands/
│   ├── flow.md              # /flow - start workflows
│   ├── flow-search.md       # /flow-search - find past work
│   ├── flow-roadmap.md      # /flow-roadmap - strategic planning
│   └── validate.md          # /validate - code review
├── skills/
│   ├── flow-skill/          # Core workflow guidance
│   │   ├── SKILL.md
│   │   ├── types/           # Work type guidance
│   │   │   ├── bugfix.md
│   │   │   ├── feature.md
│   │   │   ├── greenfield.md
│   │   │   ├── integration.md
│   │   │   ├── optimization.md
│   │   │   ├── refactor.md
│   │   │   └── custom.md
│   │   └── techniques/      # Reusable techniques
│   │       ├── hierarchical-exploration.md
│   │       └── state-machines.md
│   ├── roadmap-skill/       # Strategic planning
│   │   └── SKILL.md
│   ├── validation-skill/    # Multi-lens code review
│   │   ├── SKILL.md
│   │   └── reviewers/
│   │       ├── security.md
│   │       ├── architecture.md
│   │       ├── quality.md
│   │       ├── performance.md
│   │       ├── scalability.md
│   │       ├── testing.md
│   │       └── error-handling.md
│   └── autonomous-skill/    # Unattended execution
│       └── SKILL.md
└── hooks/
    ├── README.md
    └── detect-workflow.py
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

## Quick Start

```bash
# Clone and symlink
git clone https://github.com/andrasp/claude-code-flow.git
ln -s /path/to/claude-code-flow/commands/flow.md ~/.claude/commands/flow.md
ln -s /path/to/claude-code-flow/skills/flow-skill ~/.claude/skills/flow-skill

# Start a new Claude Code session, then:
/flow add user authentication to the API
```

See [Installation](#installation) for full setup including extensions.

## Installation

Clone this repo and symlink to your Claude Code configuration:

```bash
git clone https://github.com/andrasp/claude-code-flow.git

# Core (required)
ln -s /path/to/claude-code-flow/commands/flow.md ~/.claude/commands/flow.md
ln -s /path/to/claude-code-flow/commands/flow-search.md ~/.claude/commands/flow-search.md
ln -s /path/to/claude-code-flow/skills/flow-skill ~/.claude/skills/flow-skill

# Extensions (optional)
ln -s /path/to/claude-code-flow/commands/flow-roadmap.md ~/.claude/commands/flow-roadmap.md
ln -s /path/to/claude-code-flow/commands/validate.md ~/.claude/commands/validate.md
ln -s /path/to/claude-code-flow/skills/roadmap-skill ~/.claude/skills/roadmap-skill
ln -s /path/to/claude-code-flow/skills/validation-skill ~/.claude/skills/validation-skill
ln -s /path/to/claude-code-flow/skills/autonomous-skill ~/.claude/skills/autonomous-skill

# Hook (optional but recommended)
mkdir -p ~/.claude/hooks
ln -s /path/to/claude-code-flow/hooks/detect-workflow.py ~/.claude/hooks/detect-workflow.py
```

To enable the hook, add to your `~/.claude/settings.json`:

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

Start a new conversation and the commands, skills, and hook will be available.

## Related

- [claude-code-wisdom](https://github.com/andrasp/claude-code-wisdom) - Distilled software engineering wisdom for your CLAUDE.md

## License

MIT License - use however you want.

# Refactoring Workflow

**Context:** Restructuring or reorganizing existing code without changing its external behavior.

## Key Principles

1. **Behavior Preservation** - External behavior must remain identical (unless explicitly changing it)
2. **Safety Net** - Have tests or clear verification for risky changes; mechanical changes (renames, moves) may not need them
3. **Incremental Changes** - Small, verifiable steps
4. **Continuous Verification** - Run tests frequently during risky refactors

## Phase 1: Understanding

### 1.1 Understand the Refactoring Goal

**Explore the code first to understand the current state.**

Before asking questions:
- Read the code being refactored
- Understand its current structure and dependencies
- Identify the pain points (often obvious from the code)
- Check test coverage

The user's description usually indicates the goal. Only ask if:
- The scope is genuinely unclear
- You need to confirm whether behavior should change
- Multiple valid refactoring approaches exist

### 1.2 Assess Current State

**Test Coverage Check:**
For risky refactors (changing logic, restructuring control flow), verify test coverage:
```bash
# Run existing tests
npm test  # or equivalent

# Check coverage if available
npm run test:coverage
```

If test coverage is insufficient for risky changes:
- Write tests first for the code paths being refactored
- Tests become the safety net

For mechanical refactors (renames, file moves, extracting functions without logic changes), existing tests plus careful review are often sufficient.

**Architecture Research:**
Understand the current structure:
- How does the code flow?
- What are the dependencies?
- Are there hidden coupling points?
- What are the pain points?

Use hierarchical compression - understand at multiple levels:
1. **High level:** System/module relationships
2. **Mid level:** Class/function structure
3. **Low level:** Implementation details

Document current architecture in `research.md`.

### 1.3 Cross-Repository Considerations
If the refactor spans multiple repos:
- Identify all affected repositories
- Understand version dependencies
- Plan for coordinated changes
- Consider backwards compatibility

## Phase 2: Planning

### 2.1 Design Target State
Document the desired end state:
- New structure/organization
- Improved patterns
- Resolved problems

Create before/after diagrams if helpful:
```
Before:                    After:
┌─────────┐               ┌─────────┐
│ Module A│──────┐        │ Module A│
└─────────┘      │        └────┬────┘
                 │             │
┌─────────┐      │        ┌────▼────┐
│ Module B│──────┤        │ Service │
└─────────┘      │        └────┬────┘
                 │             │
┌─────────┐      │        ┌────▼────┐
│ Module C│──────┘        │ Module C│
└─────────┘               └─────────┘
```

### 2.2 Plan Incremental Steps
Break the refactor into small, safe steps:

Each step should:
- Be independently deployable
- Have passing tests before AND after
- Be easily reversible

Example breakdown:
```markdown
## Refactoring Steps

1. [ ] Add tests for untested code paths
2. [ ] Extract interface/abstraction
3. [ ] Move implementation to new location
4. [ ] Update consumers one by one
5. [ ] Remove old code
6. [ ] Clean up imports
```

### 2.3 Identify Risks
Consider:
- What could break?
- Are there hidden dependencies?
- Performance implications?
- Rollback strategy?

## Phase 3: Implementation

### 3.1 Preparation
Before making changes:
- Ensure all tests pass
- Create a clean git state
- Consider a feature branch

### 3.2 The Refactoring Loop

For each step:
```
1. Run tests (should pass)
2. Make ONE small change
3. Run tests (should still pass)
4. Commit with descriptive message
5. Repeat
```

**If tests fail:**
- Understand why before proceeding
- Fix the issue, or suggest reverting to the user if the fix isn't clear
- Don't proceed with failing tests unless you understand the failure is unrelated

### 3.3 Common Refactoring Patterns

**Extract Function/Method:**
- Identify duplicated or complex code
- Extract to well-named function
- Replace original with call

**Move/Rename:**
- Update imports
- Consider re-exports for backwards compatibility
- Remove old location

**Change Signature:**
- Add new signature alongside old (if public API)
- Migrate consumers
- Deprecate then remove old

**Extract Module/Class:**
- Create new structure
- Move code incrementally
- Update dependencies

### 3.4 Handling Large Refactors
For system-wide changes:
- Consider parallel structures
- Migrate incrementally
- Use feature flags if needed
- Plan for extended timeline

## Phase 5: Completion

### 5.1 Verification
- All tests pass
- Manual smoke testing
- Performance benchmarks (if applicable)
- Review for missed cleanup

### 5.2 Documentation Updates
- Update architecture docs
- Remove obsolete documentation
- Add migration notes if APIs changed

### 5.3 Record Outcome
Document in `outcome.md`:
- What was refactored and why
- Before/after comparison
- Any behavior changes (if intentional)
- Technical debt resolved
- Any new technical debt introduced
- Lessons learned

## Refactoring Safety Checklist

- [ ] Test coverage is sufficient
- [ ] All tests pass before starting
- [ ] Changes are incremental
- [ ] Tests run after each change
- [ ] Commits are small and descriptive
- [ ] Old code is fully removed (no dead code)
- [ ] Documentation is updated
- [ ] No hidden behavior changes (unless intended)

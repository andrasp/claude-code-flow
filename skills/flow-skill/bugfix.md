# Bugfix Workflow

**Context:** Fixing a specific issue or defect in existing code.

## Key Principles

1. **Understand Root Cause** - Fix the cause, not just symptoms
2. **Reproduce When Unclear** - If the fix is obvious from code analysis, reproduce after to verify; if unclear, reproduce first to understand
3. **Minimal Change** - Change only what's necessary
4. **Prevent Regression** - Add tests that would have caught this

## Phase 1: Understanding

### 1.1 Understand the Bug

Start with what the user provided. Don't ask for information you can find:
- Error messages and stack traces → analyze them
- Ticket/issue links → read them
- Related code → explore it

Only ask if the bug description is genuinely unclear about what's wrong.

### 1.2 Attempt Reproduction (When Valuable)

**Reproduction is strongly recommended but not always mandatory.**

**When reproduction is essential:**
- Root cause is non-obvious
- Multiple possible causes exist
- The fix could have unintended side effects
- You need to verify the fix works

**When reproduction can be skipped:**
- Code analysis reveals the bug with high confidence
- The issue is a clear logic error (typo, wrong condition, missing null check)
- Reproduction would be time-consuming and analysis is sufficient
- The bug is in error handling that's hard to trigger

If you skip reproduction, document your confidence level and reasoning.

**Reproduction steps (when pursuing):**
1. Set up the exact conditions
2. Perform the triggering action
3. Observe the incorrect behavior
4. Document for regression testing

### 1.3 Analyze the Bug
Investigate:
- Where in the code does this occur?
- What is the immediate cause?
- What is the root cause?
- When was this introduced?

Useful techniques:
- Stack trace analysis
- Git bisect for regression
- Logging/debugging
- Code review of related changes

Document analysis in `research.md`:
```markdown
## Bug Analysis

**Immediate Cause:** [What directly causes the bug]
**Root Cause:** [Underlying issue that allowed this]
**Introduced:** [When/how this bug was introduced]
**Affected Code:** [Files/functions involved]
```

## Phase 2: Planning

### 2.1 Design the Fix
Consider:
- What is the minimal change to fix this?
- Are there related bugs to fix?
- Could this fix break anything else?
- Is there a quick fix vs proper fix trade-off?

### 2.2 Plan Test Coverage
Before writing the fix:
- What test would have caught this bug?
- Write that test first (it should fail)
- The test proves the bug exists
- The test prevents regression

### 2.3 Assess Impact
Consider:
- What else uses this code?
- Could the fix cause side effects?
- Do we need to notify users?
- Is a hotfix needed or can it wait?

## Phase 3: Implementation

### 3.1 Write Failing Test First
Create a test that:
- Reproduces the bug conditions
- Expects the correct behavior
- Currently fails

This is Test-Driven Bugfixing:
```
1. Write test for expected behavior
2. Run test - it should FAIL (proves bug exists)
3. Fix the code
4. Run test - it should PASS (proves fix works)
5. Run all tests - ensure no regressions
```

### 3.2 Implement the Fix
Guidelines:
- Make the minimal change necessary
- Don't refactor while fixing (separate concerns)
- Add comments explaining non-obvious fixes
- Consider edge cases

### 3.3 Verify the Fix
Verification checklist:
- [ ] New test passes
- [ ] All existing tests pass
- [ ] Manual reproduction no longer triggers bug
- [ ] No new issues introduced
- [ ] Code review completed (if applicable)

### 3.4 Consider Related Issues
Ask:
- Could this bug exist elsewhere?
- Are there similar patterns to check?
- Should we add defensive code?

## Phase 4: Completion

### 4.1 Documentation
If the bug was user-facing:
- Update release notes
- Consider user communication
- Update known issues if applicable

### 4.2 Post-Mortem
For significant bugs, document:
- How did this bug get introduced?
- Why wasn't it caught by tests?
- How can we prevent similar bugs?

### 4.3 Record Outcome
Document in `outcome.md`:
```markdown
## Bug: [Brief description]

**Ticket:** [Link if applicable]

**Root Cause:**
[What caused the bug]

**Fix:**
[What was changed]

**Files Modified:**
- [file1]
- [file2]

**Test Added:**
[Description of regression test]

**Lessons Learned:**
[What we can do to prevent similar bugs]
```

## Bugfix Checklist

- [ ] Bug is reproducible
- [ ] Root cause identified (not just symptoms)
- [ ] Failing test written first
- [ ] Fix implemented with minimal changes
- [ ] New test passes
- [ ] All existing tests pass
- [ ] Manual verification completed
- [ ] Related code checked for similar issues
- [ ] Documentation updated if needed
- [ ] Outcome recorded

## Special Cases

### Intermittent Bugs
- Add extensive logging
- Look for race conditions
- Check for timing-dependent code
- Consider stress testing

### Production-Only Bugs
- Compare environments carefully
- Check configuration differences
- Look at production logs/monitoring
- Consider data differences

### Security Bugs
- Assess severity immediately
- Consider disclosure timeline
- Fix quickly but carefully
- Consider if public disclosure needed

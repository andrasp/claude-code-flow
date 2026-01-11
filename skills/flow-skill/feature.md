# Feature Development Workflow

**Context:** Adding new functionality to an existing codebase.

## Key Principles

1. **Consistency First** - Match existing patterns and conventions
2. **Integration Awareness** - Understand how the feature connects to existing code
3. **Incremental Delivery** - Break large features into shippable increments
4. **Test Coverage** - Ensure new code is well-tested

## Phase 1: Understanding

### 1.1 Explore First

**Do not ask questions that can be answered through exploration.**

Start by exploring the codebase to understand:
- Where similar features exist
- What patterns and conventions are used
- Integration points and dependencies
- Existing utilities and shared code

Only ask the user when you encounter genuine ambiguity that affects your approach.

### 1.2 Explore Existing Patterns
Before writing any code:
- Find similar features in the codebase
- Understand the architectural patterns used
- Identify reusable components or utilities
- Note naming conventions and code style

Use Glob and Grep to explore:
```
# Find similar components
Glob: **/components/**/*.tsx

# Search for related functionality
Grep: "similar keyword or pattern"
```

### 1.3 Identify Integration Points
Determine:
- Which files/modules will be modified?
- What APIs or services does this feature need?
- Are there database changes required?
- What state management is involved?

Document findings in `research.md` (if selected).

## Phase 2: Planning

### 2.1 Design the Feature
Consider:
- Component structure (if UI)
- Data flow and state management
- API contracts (if backend)
- Error handling approach

### 2.2 Break Down Tasks
Create granular tasks in `tasks.md` (if selected):
- Each task should be completable in one session
- Order by dependencies
- Be specific to the actual feature, not generic checklists

### 2.3 Assess Complexity
If the feature is large:
- Consider feature flags for incremental rollout
- Identify MVP vs nice-to-have
- Plan for code review checkpoints

## Phase 3: Implementation

### 3.1 Start with Types
Define interfaces and types first:
- Creates clear contracts
- Enables better IDE support
- Catches design issues early

### 3.2 Implement Core Logic
- Write the business logic
- Add unit tests as you go
- Keep functions small and focused

### 3.3 Build UI (if applicable)
- Follow existing component patterns
- Use existing design system/components
- Ensure accessibility

### 3.4 Integration
- Connect all pieces
- Add integration tests
- Handle error states

## Phase 5: Completion

### 5.1 Quality Checks
- [ ] All tests passing
- [ ] Code follows existing patterns
- [ ] No linting errors
- [ ] Accessibility verified (if UI)
- [ ] Performance acceptable

### 5.2 Documentation
- Update relevant documentation
- Add inline comments for complex logic
- Update API docs if applicable

### 5.3 Record Outcome
Fill in `outcome.md`:
- What was built
- Key decisions made
- Any technical debt incurred
- Lessons for future features

## Common Patterns

### Adding a New API Endpoint
1. Define types/schemas
2. Implement handler
3. Add route
4. Add tests
5. Update API docs

### Adding a New UI Component
1. Create component file
2. Add styles (following existing patterns)
3. Add to component index
4. Write stories/tests
5. Integrate into parent

### Adding a New Database Table
1. Design schema
2. Create migration
3. Update types
4. Create data access functions
5. Add tests

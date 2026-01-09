# Architecture Review Task

Review code changes for architectural quality and adherence to established guidelines.

## User's Coding Guidelines
{claude_md}

Apply the user's stated architectural preferences and design principles when evaluating.
User guidelines take precedence over generic best practices.

## Changed Files
{files}

## Focus Areas

1. **Layer Violations**: Does UI call database? Does controller have business logic?
2. **Coupling**: Are modules becoming too interdependent?
3. **Cohesion**: Do new classes/modules have single responsibility?
4. **Pattern Consistency**: Do changes follow established patterns?
5. **Abstraction**: Are abstractions at the right level?
6. **Dependencies**: Circular dependencies? Inappropriate dependencies?
7. **User Guidelines**: Do changes violate any principles in CLAUDE.md?

## Output Format

Return findings as structured markdown:
- Group by severity (High, Medium, Low)
- For each issue:
  - File and line number
  - Description of violation
  - What pattern/principle is violated (reference CLAUDE.md if applicable)
  - Suggested refactoring
  - Confidence (High/Medium/Low)

## Important

- User's CLAUDE.md guidelines are authoritative - flag violations of those first
- Consider existing codebase patterns before flagging violations
- Not every deviation is bad - use judgment
- Focus on maintainability impact

# Code Quality Review Task

Review code changes for quality, maintainability, and adherence to coding standards.

## User's Coding Guidelines
{claude_md}

Apply the user's stated coding standards, naming conventions, and quality expectations.
User guidelines take precedence over generic best practices.

## Changed Files
{files}

## Focus Areas

1. **Duplication**: Copy-pasted logic that should be extracted
2. **Naming**: Unclear or misleading names for variables, functions, classes
3. **Complexity**: High cyclomatic complexity, deep nesting, long functions
4. **Magic Values**: Hardcoded numbers/strings that should be constants
5. **Dead Code**: Unused code introduced
6. **Comments**: Missing where needed, or misleading/outdated
7. **User Guidelines**: Do changes violate coding standards in CLAUDE.md?

## Output Format

Return findings as structured markdown:
- Group by severity (High, Medium, Low)
- For each issue:
  - File and line number
  - Description of quality issue
  - What standard/principle is violated (reference CLAUDE.md if applicable)
  - Suggested improvement
  - Confidence (High/Medium/Low)

## Important

- User's CLAUDE.md standards are authoritative - flag violations of those first
- Consider context - not all duplication is bad, not all long functions need splitting
- Focus on readability and maintainability impact
- False positives waste time - be confident before reporting

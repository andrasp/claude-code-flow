# Error Handling Review Task

Review code changes for robustness and graceful degradation.

## Changed Files
{files}

## Focus Areas

1. **Unhandled Rejections**: Promises without catch, missing await
2. **Missing Try/Catch**: Fallible operations without error handling
3. **Swallowed Errors**: Empty catch blocks that hide problems
4. **Error Logging**: Missing logs for important failures
5. **User Messages**: Generic or confusing error messages
6. **Fallback Behavior**: Missing graceful degradation
7. **Recovery**: No retry or recovery mechanisms where appropriate
8. **Transactions**: Partial failure without rollback

## Output Format

Return findings as structured markdown:
- Group by severity (High, Medium, Low)
- For each issue:
  - File and line number
  - Description of error handling gap
  - What happens when this fails
  - Suggested fix
  - Confidence (High/Medium/Low)

## Important

- Unhandled promise rejections crash Node.js - High severity
- Swallowed errors make debugging impossible - High severity
- Consider what the user sees when errors occur
- External calls should always have error handling

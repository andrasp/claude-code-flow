# Security Review Task

Review code changes for security vulnerabilities.

## Changed Files
{files}

## Focus Areas

1. **Injection Attacks**: SQL, command, XSS, template injection
2. **Authentication/Authorization**: Bypasses, missing checks, weak validation
3. **Data Exposure**: Logging sensitive data, hardcoded secrets, verbose errors
4. **Input Validation**: Missing or insufficient validation
5. **Cryptography**: Weak algorithms, improper usage
6. **Dependencies**: Known vulnerabilities in added packages

## Output Format

Return findings as structured markdown:
- Group by severity (Critical, High, Medium, Low)
- For each issue:
  - File and line number
  - Description of vulnerability
  - Exploitation scenario (how could this be attacked?)
  - Suggested fix
  - Confidence (High/Medium/Low)

If no issues found, state "No security issues identified" with brief explanation of what was checked.

## Important

- Only report actual vulnerabilities, not theoretical concerns
- Consider the context (internal tool vs. public-facing)
- False positives waste time - be confident before reporting

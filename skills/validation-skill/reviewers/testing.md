# Testing Review Task

Review code changes for test coverage and test quality.

## Changed Files
{files}

## Focus Areas

1. **Coverage Gaps**: New code without corresponding tests
2. **Assertion Quality**: Tests that don't actually assert anything
3. **Edge Cases**: Missing boundary condition tests
4. **Flaky Patterns**: Timing dependencies, ordering assumptions
5. **Test Isolation**: Shared state between tests
6. **Error Paths**: Missing tests for failure scenarios
7. **Mocking**: Over-mocking that hides real behavior
8. **Integration**: Missing integration tests for new integrations

## Output Format

Return findings as structured markdown:
- Group by severity (High, Medium, Low)
- For each issue:
  - File and line number (or "missing test for X")
  - Description of testing gap
  - What could go wrong without this test
  - Suggested test to add
  - Confidence (High/Medium/Low)

## Important

- New business logic without tests is High severity
- Tests without assertions are High severity (false confidence)
- Not every function needs a test - focus on important logic
- Consider existing test patterns in the codebase

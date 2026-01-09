# Scalability Review Task

Review code changes for behavior under load and distributed system concerns.

## Changed Files
{files}

## Focus Areas

1. **Race Conditions**: Concurrent access to shared state
2. **Transactions**: Missing locks/transactions where needed
3. **Stateful Code**: In-memory state that won't work multi-instance
4. **File System**: Assumptions that won't work in containers
5. **Idempotency**: Missing for retryable operations
6. **Queues/Buffers**: Unbounded growth potential
7. **External Calls**: Missing timeouts, no circuit breakers
8. **Configuration**: Hardcoded URLs/hosts

## Output Format

Return findings as structured markdown:
- Group by severity (High, Medium, Low)
- For each issue:
  - File and line number
  - Description of scalability concern
  - What breaks at scale (e.g., "fails with multiple instances")
  - Suggested fix
  - Confidence (High/Medium/Low)

## Important

- Consider whether code needs to scale (internal tool vs. high-traffic service)
- In-memory state and missing timeouts are common issues
- Idempotency is critical for any operation that could be retried

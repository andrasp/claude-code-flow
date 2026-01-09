# Performance Review Task

Review code changes for performance issues and optimization opportunities.

## Changed Files
{files}

## Focus Areas

1. **Algorithmic Complexity**: O(n²) or worse where O(n) is possible
2. **Database Queries**: N+1 patterns, missing indexes, unbounded fetches
3. **Memory**: Leaks, growing collections, unclosed resources
4. **Async Operations**: Blocking calls that should be async
5. **Caching**: Missing opportunities, cache invalidation issues
6. **Hot Paths**: Expensive operations in frequently-called code
7. **Bundle Size**: (Frontend) Large imports, missing tree-shaking

## Output Format

Return findings as structured markdown:
- Group by severity (Critical, High, Medium, Low)
- For each issue:
  - File and line number
  - Description of performance issue
  - Impact estimation (e.g., "1000 orders = 1001 queries")
  - Suggested optimization
  - Confidence (High/Medium/Low)

## Important

- Focus on measurable impact, not micro-optimizations
- Consider the scale at which the code will run
- N+1 queries and O(n²) algorithms are usually High severity
- Missing pagination on unbounded queries is Critical

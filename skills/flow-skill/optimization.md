# Optimization Workflow

**Context:** Improving performance, efficiency, or resource usage of existing code.

## Key Principles

1. **Measure First** - Never optimize without benchmarks
2. **Profile, Don't Guess** - Find actual bottlenecks
3. **One Change at a Time** - Isolate impact of each optimization
4. **Verify Improvements** - Prove optimizations work

## Phase 1: Understanding

### 1.1 Understand the Optimization Target

**Start measuring and profiling before asking questions.**

The user's description indicates what to optimize. Before asking:
- Identify the relevant code/systems
- Look for existing benchmarks or metrics
- Run initial profiling if possible
- Explore the current implementation

Only ask if:
- The optimization target is genuinely ambiguous
- You need specific target numbers the user has in mind
- Multiple optimization strategies exist with different trade-offs

### 1.2 Establish Baselines

**Measure before optimizing.** Don't optimize without evidence.

Create reproducible benchmarks:
```markdown
## Baseline Measurements

| Metric | Current | Target | Method |
|--------|---------|--------|--------|
| Response time | 500ms | <100ms | Load test |
| Memory usage | 2GB | <500MB | Profiler |
| Query count | 50 | <10 | Query log |
| Bundle size | 5MB | <1MB | Build output |
```

Document measurement methodology in `research.md`:
- How measurements were taken
- Test conditions
- Data/load characteristics

### 1.3 Profile and Identify Bottlenecks
Don't guess - profile:

**For CPU/Time:**
- Use profiling tools (Chrome DevTools, perf, etc.)
- Identify hot paths
- Find unexpected slow operations

**For Memory:**
- Heap snapshots
- Memory profilers
- Identify leaks or bloat

**For Database:**
- Query logging
- Explain plans
- N+1 detection

**For Network:**
- Request waterfall
- Payload sizes
- Connection overhead

Document findings:
```markdown
## Bottlenecks Identified

1. **[Location]**: [Description] - contributes [X]% to problem
2. **[Location]**: [Description] - contributes [Y]% to problem
```

## Phase 2: Planning

### 2.1 Prioritize Optimizations
Focus on highest impact first:
- What contributes most to the problem?
- What is easiest to fix?
- What has the best effort/impact ratio?

Use the 80/20 rule - 20% of code often causes 80% of performance issues.

### 2.2 Design Optimizations
For each bottleneck, consider approaches:

**Algorithm Improvements:**
- Better data structures
- Reduced complexity
- Caching

**Query Optimizations:**
- Indexes
- Query restructuring
- Batching
- Denormalization

**Code Optimizations:**
- Lazy loading
- Memoization
- Parallel processing
- Reduced allocations

**Architecture Changes:**
- Caching layers
- Async processing
- Load distribution

### 2.3 Plan Verification
For each optimization:
- How will we verify improvement?
- What could regress?
- How will we test correctness?

## Phase 3: Implementation

### 3.1 One Optimization at a Time
For each optimization:

```
1. Create isolated branch/change
2. Implement the optimization
3. Run correctness tests
4. Run performance benchmarks
5. Compare to baseline
6. Document results
7. Commit or revert
```

### 3.2 Document Each Optimization
```markdown
## Optimization: [Name]

**Target:** [What we're optimizing]
**Approach:** [How we're optimizing]

**Before:**
- Metric: [value]

**After:**
- Metric: [value]

**Improvement:** [X]% / [absolute improvement]

**Trade-offs:** [Any downsides]
```

### 3.3 Watch for Regressions
After each change:
- Verify functionality still correct
- Check other metrics didn't regress
- Monitor for edge cases

### 3.4 Common Optimization Patterns

**Caching:**
```
- Identify repeated expensive operations
- Add appropriate cache layer
- Consider cache invalidation
- Monitor hit rates
```

**Batching:**
```
- Find N+1 patterns
- Combine into batch operations
- Verify correctness with batched data
```

**Indexing:**
```
- Analyze query patterns
- Add appropriate indexes
- Verify query plans improve
- Monitor write performance impact
```

**Lazy Loading:**
```
- Identify eager loading of unused data
- Implement on-demand loading
- Verify UX is acceptable
```

## Phase 4: Completion

### 4.1 Final Benchmarks
Run complete benchmark suite:
```markdown
## Final Measurements

| Metric | Baseline | Target | Achieved | Improvement |
|--------|----------|--------|----------|-------------|
| Response time | 500ms | <100ms | 75ms | 85% |
| Memory usage | 2GB | <500MB | 400MB | 80% |
```

### 4.2 Verify No Regressions
- All functionality tests pass
- No unexpected side effects
- Other metrics stable

### 4.3 Document Optimizations
Update `outcome.md`:
- Summary of improvements achieved
- Each optimization and its impact
- Trade-offs made
- Remaining opportunities
- How to maintain gains
- Lessons learned

## Optimization Checklist

- [ ] Baseline measurements established
- [ ] Bottlenecks identified with profiling
- [ ] Optimizations prioritized by impact
- [ ] Each optimization measured independently
- [ ] Correctness verified after each change
- [ ] No performance regressions introduced
- [ ] Trade-offs documented
- [ ] Final benchmarks show improvement
- [ ] Results documented in outcome.md

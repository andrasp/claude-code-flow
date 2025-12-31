# Greenfield Development Workflow

**Context:** Building a new component, system, or project from scratch.

## Key Principles

1. **Requirements First** - Deeply understand what needs to be built
2. **Architecture Before Code** - Design the structure before implementation
3. **Validate Early** - Get feedback on design before heavy investment
4. **Build for Change** - Expect requirements to evolve

## Phase 1: Understanding

### 1.1 Requirements Discovery

**Start with what's given, explore before asking.**

The user's initial description often contains the core requirements. Before asking questions:
- Analyze the description for implicit requirements
- Explore any referenced systems or integrations
- Look at similar systems in the codebase (if any)
- Research patterns for this type of system

**Ask only for genuinely missing information:**
- Unclear scope or boundaries
- Conflicting requirements
- Critical constraints not mentioned (security, scale, integration)

Greenfield work often requires more clarification than other types, but still prefer discovery over interrogation. A few targeted questions after initial exploration are better than a long upfront questionnaire.

### 1.2 Research Phase
Explore before building:
- Are there similar systems to learn from?
- What libraries/frameworks are candidates?
- What patterns fit this problem?
- What are the risks and unknowns?

Document extensively in `research.md`:
- Options considered
- Trade-offs analyzed
- Decisions made and why

### 1.3 Define Success Criteria
Create clear, measurable acceptance criteria:
```markdown
## Success Criteria

- [ ] [Specific, measurable criterion]
- [ ] [Specific, measurable criterion]
- [ ] Performance: [metric] under [conditions]
- [ ] Security: [requirement]
```

## Phase 2: Planning

### 2.1 Architecture Design
Design the high-level structure:

```
Consider documenting:
- Component/module breakdown
- Data flow diagrams
- API contracts
- Database schema
- Integration points
```

For complex systems, create architecture diagrams in research.md using ASCII or Mermaid.

### 2.2 Technology Decisions
Document technology choices:
- Languages and frameworks
- Libraries and dependencies
- Infrastructure requirements
- Development tools

### 2.3 Phased Delivery Plan
Break into phases:

**Phase 1: Foundation**
- Core infrastructure
- Basic functionality
- Proof of concept

**Phase 2: Core Features**
- Primary use cases
- Essential integrations

**Phase 3: Polish**
- Edge cases
- Performance optimization
- Documentation

### 2.4 Risk Assessment
Identify and mitigate risks:
- Technical unknowns
- Integration challenges
- Performance concerns
- Security vulnerabilities

## Phase 3: Implementation

### 3.1 Foundation First
Start with:
- Project structure
- Build system
- Core types/interfaces
- Basic infrastructure

### 3.2 Vertical Slices
Build complete features end-to-end:
- Proves integration works
- Delivers value early
- Reveals issues quickly

### 3.3 Iterate and Validate
After each slice:
- Validate with requirements
- Get feedback if possible
- Adjust course as needed

### 3.4 Testing Strategy
For greenfield, establish testing patterns early:
- Unit tests for logic
- Integration tests for connections
- End-to-end tests for critical paths

## Phase 4: Completion

### 4.1 Documentation
Greenfield requires comprehensive docs:
- Architecture overview
- Setup instructions
- API documentation
- Operational runbook

### 4.2 Knowledge Transfer
Ensure others can work on it:
- Code is self-documenting
- Complex areas have comments
- Design decisions are recorded

### 4.3 Record Outcome
Document in `outcome.md`:
- What was built
- Architecture decisions and rationale
- Known limitations
- Future enhancement ideas
- Lessons learned

## Greenfield Checklist

Before considering done:
- [ ] All success criteria met
- [ ] Architecture documented
- [ ] Tests provide good coverage
- [ ] Setup/deployment documented
- [ ] Error handling comprehensive
- [ ] Security review completed
- [ ] Performance validated
- [ ] Monitoring/logging in place

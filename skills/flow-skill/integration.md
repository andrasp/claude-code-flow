# Integration Workflow

**Context:** Integrating with external systems, APIs, services, or third-party libraries.

## Key Principles

1. **Understand the External System** - Read docs, explore APIs, understand constraints
2. **Design for Failure** - External systems fail; plan for it
3. **Isolate the Integration** - Keep integration code separate from business logic
4. **Test at Boundaries** - Mock external systems, but also test real connections

## Phase 1: Understanding

### 1.1 Explore First

Before asking questions, investigate:
- Official documentation
- API references and schemas
- Authentication requirements
- Rate limits and quotas
- Example code and SDKs

Document findings in `research.md`:
```markdown
## External System

**Name:** [Service/API name]
**Documentation:** [Links]
**Authentication:** [OAuth, API key, etc.]
**Rate Limits:** [If applicable]

## Key Endpoints/Features

[List the endpoints or features you'll use]

## Constraints

[Any limitations or gotchas discovered]
```

### 1.2 Identify Integration Points

Determine:
- What data flows in each direction?
- What triggers the integration (user action, scheduled, event)?
- What format is data exchanged in?
- What happens when the external system is unavailable?

### 1.3 Authentication and Security

Understand:
- How are credentials managed?
- Token refresh requirements?
- Scopes and permissions needed?
- Secrets storage approach?

## Phase 2: Planning

### 2.1 Design the Integration Layer

Consider:
- Wrapper/client class for the external API
- Data transformation between systems
- Error handling strategy
- Retry logic with backoff
- Circuit breaker patterns

### 2.2 Plan for Failure Modes

External systems can fail in many ways:
- Network timeouts
- Rate limiting
- Authentication expiry
- Schema changes
- Partial failures
- Downtime

For each failure mode, define:
- How to detect it
- How to handle it
- How to recover
- How to notify users/operators

### 2.3 Define Success Criteria

In `plan.md`:
```markdown
## Success Criteria

- [ ] Can authenticate successfully
- [ ] Can perform [primary operation]
- [ ] Handles [failure mode 1] gracefully
- [ ] Handles [failure mode 2] gracefully
- [ ] Integration is isolated behind clear interface
- [ ] Secrets are properly managed
```

## Phase 3: Implementation

### 3.1 Start with Authentication

Get auth working first:
1. Set up credentials securely
2. Implement token refresh if needed
3. Test authentication independently
4. Handle auth failures gracefully

### 3.2 Build the Client Layer

Create a clean abstraction:
```
IntegrationClient
├── authenticate()
├── primaryOperation()
├── handleError()
└── retry logic
```

Keep external system details contained in this layer.

### 3.3 Implement Data Transformation

Map between systems:
- External format → internal format
- Internal format → external format
- Validate data at boundaries
- Handle missing/extra fields gracefully

### 3.4 Add Robust Error Handling

For each external call:
- Set appropriate timeouts
- Catch and categorize errors
- Log enough for debugging
- Return meaningful errors to callers
- Consider retry with exponential backoff

### 3.5 Testing Strategy

**Unit tests:**
- Mock the external API
- Test all error handling paths
- Test data transformations

**Integration tests:**
- Test against real API (staging/sandbox)
- Test authentication flow
- Test actual data flow

**Manual verification:**
- End-to-end test with real system
- Verify in production-like environment

## Phase 4: Completion

### 4.1 Documentation

Document:
- How to configure the integration
- Required environment variables/secrets
- How to test locally
- Troubleshooting common issues

### 4.2 Monitoring and Alerting

Consider:
- Logging for debugging
- Metrics for health monitoring
- Alerts for failures
- Dashboard for visibility

### 4.3 Record Outcome

Document in `outcome.md`:
```markdown
## Integration: [External System Name]

**Purpose:** [What this integration does]

**Key Components:**
- [Client class/module]
- [Configuration]
- [Data models]

**Configuration Required:**
- [Environment variables]
- [Secrets]

**Testing:**
- How to test locally
- Sandbox/staging environment details

**Known Limitations:**
- [Rate limits]
- [Feature gaps]

**Lessons Learned:**
[What we learned about integrating with this system]
```

## Integration Checklist

- [ ] Documentation thoroughly reviewed
- [ ] Authentication working
- [ ] Primary operations implemented
- [ ] Error handling for all failure modes
- [ ] Retry logic with backoff
- [ ] Timeouts configured appropriately
- [ ] Secrets managed securely
- [ ] Unit tests with mocks
- [ ] Integration tests against real API
- [ ] Logging for debugging
- [ ] Documentation for setup and troubleshooting

## Common Integration Patterns

### REST APIs
- Use official SDK if available
- Handle pagination
- Respect rate limits
- Cache when appropriate

### Webhooks
- Verify signatures
- Handle duplicate deliveries (idempotency)
- Acknowledge quickly, process async
- Handle retries from sender

### Message Queues
- Handle message ordering (or lack thereof)
- Implement dead letter handling
- Consider exactly-once vs at-least-once
- Plan for replay scenarios

### OAuth Integrations
- Store refresh tokens securely
- Handle token expiry gracefully
- Request minimal scopes
- Handle revoked access

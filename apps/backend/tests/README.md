# Backend Tests

Test suite for EclipseLink AI backend.

## Test Structure

- `unit/` - Unit tests for individual functions and services
- `integration/` - Integration tests for API endpoints
- `e2e/` - End-to-end tests

## Running Tests

```bash
# Run all tests
npm test

# Run unit tests only
npm run test:unit

# Run integration tests only
npm run test:integration

# Run with coverage
npm run test:coverage

# Run in watch mode
npm run test:watch
```

## Writing Tests

### Unit Tests
Place unit tests in `unit/` directory, organized by module:
- `unit/services/` - Service tests
- `unit/utils/` - Utility function tests
- `unit/middleware/` - Middleware tests

### Integration Tests
Place integration tests in `integration/` directory:
- `integration/auth/` - Authentication endpoint tests
- `integration/handoffs/` - Handoff endpoint tests
- `integration/voice/` - Voice endpoint tests

### E2E Tests
Place end-to-end tests in `e2e/` directory for complete workflows.

## Test Conventions

- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)
- Mock external services (Azure OpenAI, R2, etc.)
- Use factory functions for test data
- Clean up after tests (database, Redis)

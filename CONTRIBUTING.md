# Contributing to EclipseLink AI

Thank you for your interest in contributing to EclipseLink AI! This document provides guidelines for contributing to the project.

## Development Setup

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/rohimaya-ai-eclipselink-product.git
   cd rohimaya-ai-eclipselink-product
   ```
3. **Run the setup script**
   ```bash
   bash scripts/setup.sh
   ```
4. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Git Workflow

We follow the **Git Flow** branching strategy:

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Emergency production fixes

## Commit Message Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Example:**
```bash
git commit -m "feat(voice): add waveform visualization to voice recorder"
```

## Code Style

- **TypeScript**: Use strict mode, proper types
- **ESLint**: Follow configured rules
- **Prettier**: Auto-format before committing
- **Comments**: Use JSDoc for public functions

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage

```bash
npm test
```

## Pull Request Process

1. Update documentation if needed
2. Ensure all tests pass
3. Update CHANGELOG.md
4. Submit PR against `develop` branch
5. Wait for review and approval

## Code Review

All submissions require review. We use GitHub/GitLab for managing pull requests and code reviews.

## Questions?

Feel free to open an issue for questions or discussions.

---

*© 2025 Rohimaya Health AI. All rights reserved.*

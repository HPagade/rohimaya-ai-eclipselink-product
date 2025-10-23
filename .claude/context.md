# EclipseLink AI - Project Context for Claude Code

## Product Overview
EclipseLink AI is a voice-enabled clinical handoff platform that transforms spoken patient reports into structured SBAR (Situation, Background, Assessment, Recommendation) documentation using advanced AI.

## Company
**Rohimaya Health AI**
- **CEO**: Hannah Kraulik Pagade
- **CTO**: Prasad Pagade

## Tech Stack
- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS, shadcn/ui, Zustand, React Query
- **Backend**: Express.js, TypeScript, Supabase, Redis (Upstash), BullMQ
- **AI**: Azure OpenAI (Whisper for speech-to-text, GPT-4 for SBAR generation)
- **Database**: PostgreSQL via Supabase
- **Storage**: Cloudflare R2 for voice recordings and documents
- **Deployment**: Cloudflare Pages (frontend), Railway (backend)

## Code Conventions
- Use TypeScript strict mode
- Follow ESLint + Prettier rules
- Use functional components with hooks (no class components)
- Use Tailwind CSS for styling (no CSS modules)
- Use shadcn/ui components when available
- Follow Conventional Commits format
- Write comprehensive JSDoc comments for functions

## File Organization
- Components go in `apps/frontend/src/components/`
- API routes in `apps/frontend/src/app/api/`
- Backend controllers in `apps/backend/src/controllers/`
- Backend services in `apps/backend/src/services/`
- Shared types in `packages/types/src/`

## Naming Conventions
- Components: PascalCase (VoiceRecorder.tsx)
- Files: camelCase for utilities, PascalCase for components
- Functions: camelCase (createHandoff, generateSBAR)
- Constants: UPPER_SNAKE_CASE (API_BASE_URL)
- Types/Interfaces: PascalCase (User, HandoffData)

## Testing
- Use Jest for unit tests
- Use React Testing Library for component tests
- Test files should be named `*.test.ts` or `*.test.tsx`
- Aim for >80% code coverage

## Documentation
- All public functions should have JSDoc comments
- Complex logic should have inline comments
- Update README.md when adding new features
- Keep API documentation up to date in `docs/api/`

## Brand Colors (Rohimaya Health AI)
```typescript
const colors = {
  peacockTeal: '#1a9b8e',
  phoenixGold: '#f4c430',
  lunarBlue: '#2c3e50',
  moonWhite: '#f8f9fa',
  eclipseNavy: '#1a2332',
  accentCopper: '#b87333'
};
```

## Key Features
1. Voice recording interface
2. Real-time transcription (Azure Whisper)
3. AI-powered SBAR generation (GPT-4)
4. EHR integration (Epic, Cerner, MEDITECH)
5. Multi-facility support
6. HIPAA compliant
7. Progressive Web App (PWA)

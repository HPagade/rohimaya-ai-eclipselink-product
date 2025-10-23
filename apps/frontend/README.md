# EclipseLink AI - Frontend

Next.js 14 Progressive Web App (PWA) for EclipseLink AI clinical handoff platform.

## Tech Stack

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Components**: shadcn/ui + Radix UI
- **State Management**: Zustand + React Query
- **Forms**: React Hook Form + Zod validation
- **PWA**: next-pwa

## Getting Started

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm run start

# Run tests
npm test

# Run linter
npm run lint

# Type check
npm run type-check
```

## Environment Variables

Copy `.env.local.example` to `.env.local` and update with your values:

```bash
cp .env.local.example .env.local
```

Required variables:
- `NEXT_PUBLIC_API_URL` - Backend API URL
- `NEXT_PUBLIC_SUPABASE_URL` - Supabase project URL
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` - Supabase anonymous key

## Project Structure

```
src/
├── app/              # Next.js App Router pages
├── components/       # React components
├── hooks/            # Custom React hooks
├── lib/              # Utility libraries
├── stores/           # Zustand stores
├── types/            # TypeScript types
└── styles/           # Global styles
```

## Development Guidelines

- Use TypeScript strict mode
- Follow ESLint + Prettier rules
- Use functional components with hooks
- Use Tailwind CSS for styling
- Use shadcn/ui components when available
- Write JSDoc comments for public functions

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com)
- [shadcn/ui](https://ui.shadcn.com)

---

*© 2025 Rohimaya Health AI. All rights reserved.*

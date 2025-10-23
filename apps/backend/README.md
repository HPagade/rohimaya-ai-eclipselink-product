# EclipseLink AI - Backend

Express.js API server for EclipseLink AI clinical handoff platform.

## Tech Stack

- **Framework**: Express.js
- **Language**: TypeScript
- **Database**: PostgreSQL via Supabase
- **Cache/Queue**: Redis (Upstash) + BullMQ
- **Storage**: Cloudflare R2 (S3-compatible)
- **AI**: Azure OpenAI (Whisper + GPT-4)
- **Authentication**: JWT + Supabase Auth
- **Logging**: Winston + Logtail
- **Monitoring**: Sentry

## Getting Started

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.example .env

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

# Run background workers
npm run worker
```

## Environment Variables

Update `.env` with your actual values. See `.env.example` for all required variables.

## Project Structure

```
src/
├── config/         # Configuration files
├── controllers/    # Route controllers
├── services/       # Business logic
├── models/         # Database models
├── middleware/     # Express middleware
├── routes/         # API routes
├── utils/          # Utility functions
├── types/          # TypeScript types
├── workers/        # Background workers
├── app.ts          # Express app setup
└── server.ts       # Server entry point
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user

### Handoffs
- `GET /api/handoffs` - List handoffs
- `POST /api/handoffs` - Create handoff
- `GET /api/handoffs/:id` - Get handoff details
- `PUT /api/handoffs/:id` - Update handoff
- `DELETE /api/handoffs/:id` - Delete handoff

### Voice Processing
- `POST /api/voice/upload` - Upload voice recording
- `GET /api/voice/status/:jobId` - Get processing status
- `GET /api/voice/:id` - Get voice recording

### Patients
- `GET /api/patients` - List patients
- `POST /api/patients` - Create patient
- `GET /api/patients/:id` - Get patient details
- `PUT /api/patients/:id` - Update patient

## Development Guidelines

- Use TypeScript strict mode
- Follow ESLint + Prettier rules
- Write comprehensive error handling
- Add logging for important operations
- Write unit tests for services
- Document API endpoints

---

*© 2025 Rohimaya Health AI. All rights reserved.*

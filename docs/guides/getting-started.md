# Getting Started with EclipseLink AI

Quick start guide for developers.

## Prerequisites

- Node.js 18+
- PostgreSQL 15+ or Supabase account
- Redis or Upstash Redis
- Azure OpenAI account
- Cloudflare R2 account

## Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/HPagade/rohimaya-ai-eclipselink-product.git
   cd rohimaya-ai-eclipselink-product
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

4. **Set up database**
   ```bash
   bash database/setup.sh
   ```

5. **Start development servers**
   ```bash
   npm run dev
   ```

For complete setup instructions, see [SETUP.md](../../SETUP.md).

## Next Steps

- Read the [Developer Guide](../../README-DEVELOPERS.md)
- Review the [Architecture Documentation](../architecture/system-overview.md)
- Explore the [API Documentation](../api/authentication.md)

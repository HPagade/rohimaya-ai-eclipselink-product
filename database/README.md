# Database Directory

This directory contains database-related files for EclipseLink AI.

## Structure

- **migrations/** - SQL migration files
- **seeds/** - Seed data files
- **functions/** - PostgreSQL functions and triggers
- **schema.sql** - Complete database schema (to be created)

## Usage

Run migrations:
```bash
npm run migrate
```

Seed database:
```bash
npm run seed
```

## Database

- **Provider**: Supabase (PostgreSQL 15)
- **Connection**: Use `DATABASE_URL` environment variable
- **Features**: Row-level security, real-time subscriptions

---

*Part 3 of documentation (Database Schema & ERD) will provide complete schema details.*

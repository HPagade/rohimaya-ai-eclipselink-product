# EclipseLink AI - Backend Dockerfile
# Multi-stage build for production optimization

# ============================================================
# Stage 1: Base Dependencies
# ============================================================
FROM node:18-alpine AS base

# Install system dependencies
RUN apk add --no-cache \
    libc6-compat \
    openssl \
    curl \
    && rm -rf /var/cache/apk/*

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY apps/backend/package*.json ./apps/backend/
COPY packages ./packages

# ============================================================
# Stage 2: Development Dependencies
# ============================================================
FROM base AS deps

# Install all dependencies (including devDependencies)
RUN npm ci

# ============================================================
# Stage 3: Builder
# ============================================================
FROM base AS builder

WORKDIR /app

# Copy dependencies from deps stage
COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/apps/backend/node_modules ./apps/backend/node_modules
COPY --from=deps /app/packages ./packages

# Copy source code
COPY apps/backend ./apps/backend
COPY tsconfig.json ./

# Build TypeScript
RUN npm run build:backend

# ============================================================
# Stage 4: Production Runner
# ============================================================
FROM base AS runner

WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Copy built files
COPY --from=builder --chown=nodejs:nodejs /app/apps/backend/dist ./apps/backend/dist
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /app/apps/backend/node_modules ./apps/backend/node_modules
COPY --from=builder --chown=nodejs:nodejs /app/packages ./packages

# Copy package.json for scripts
COPY --chown=nodejs:nodejs package*.json ./
COPY --chown=nodejs:nodejs apps/backend/package*.json ./apps/backend/

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:4000/health || exit 1

# Switch to non-root user
USER nodejs

# Expose port
EXPOSE 4000

# Set environment
ENV NODE_ENV=production
ENV PORT=4000

# Start the application
CMD ["node", "apps/backend/dist/index.js"]

# ============================================================
# Stage 5: Development Runner (For docker-compose)
# ============================================================
FROM base AS development

WORKDIR /app

# Copy dependencies from deps stage
COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/apps/backend/node_modules ./apps/backend/node_modules
COPY --from=deps /app/packages ./packages

# Copy source code
COPY apps/backend ./apps/backend
COPY package*.json ./
COPY tsconfig.json ./

# Install TypeScript and ts-node globally for development
RUN npm install -g typescript ts-node nodemon

# Expose port
EXPOSE 4000

# Set environment
ENV NODE_ENV=development
ENV PORT=4000

# Start with nodemon for hot reload
CMD ["npm", "run", "dev:backend"]

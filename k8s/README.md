# Kubernetes Deployment Manifests for EclipseLink AI

This directory contains Kubernetes manifests for deploying EclipseLink AI to production Kubernetes clusters.

## Quick Start

```bash
# 1. Create namespace
kubectl apply -f 00-namespace.yaml

# 2. Create secrets (edit with your values first)
kubectl apply -f 01-secrets.yaml

# 3. Deploy database and cache
kubectl apply -f 02-postgres.yaml
kubectl apply -f 03-redis.yaml

# 4. Deploy application
kubectl apply -f 04-backend.yaml
kubectl apply -f 05-frontend.yaml

# 5. Setup ingress (edit with your domain first)
kubectl apply -f 06-ingress.yaml

# 6. Optional: Deploy monitoring
kubectl apply -f 07-monitoring.yaml
```

## Prerequisites

- Kubernetes cluster (v1.24+)
- kubectl configured
- Helm 3.x (for monitoring)
- Persistent storage provisioner
- Ingress controller (nginx recommended)
- cert-manager (for SSL certificates)

## Files

- `00-namespace.yaml` - Namespace configuration
- `01-secrets.yaml` - Secrets (API keys, passwords) - **NEVER COMMIT WITH REAL VALUES**
- `02-postgres.yaml` - PostgreSQL StatefulSet
- `03-redis.yaml` - Redis Deployment
- `04-backend.yaml` - Backend API Deployment
- `05-frontend.yaml` - Frontend Deployment
- `06-ingress.yaml` - Ingress configuration with SSL
- `07-monitoring.yaml` - Prometheus/Grafana monitoring (optional)
- `kustomization.yaml` - Kustomize configuration

## Configuration

### Secrets

Edit `01-secrets.yaml` and replace all placeholder values:

```yaml
# REQUIRED: Change these values!
POSTGRES_PASSWORD: base64-encoded-password
REDIS_PASSWORD: base64-encoded-password
SECRET_KEY: base64-encoded-secret-key
OPENAI_API_KEY: base64-encoded-api-key
ANTHROPIC_API_KEY: base64-encoded-api-key
```

Generate base64 values:
```bash
echo -n "your-secret-here" | base64
```

### Storage

By default, these manifests use `standard` storage class. Adjust if needed:

```yaml
storageClassName: standard  # Change to your storage class
```

### Resource Limits

Adjust based on your cluster capacity:

```yaml
resources:
  requests:
    cpu: 500m
    memory: 512Mi
  limits:
    cpu: 1000m
    memory: 1Gi
```

## Scaling

```bash
# Scale backend
kubectl scale deployment backend --replicas=3

# Scale frontend
kubectl scale deployment frontend --replicas=2
```

## Monitoring

```bash
# View pods
kubectl get pods

# View logs
kubectl logs -f deployment/backend

# View services
kubectl get svc

# View ingress
kubectl get ingress
```

## Troubleshooting

```bash
# Check pod status
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>

# Check events
kubectl get events --sort-by='.lastTimestamp'

# Shell into pod
kubectl exec -it <pod-name> -- /bin/sh
```

## Backup Strategy

Backup PostgreSQL data:

```bash
# Backup
kubectl exec -it postgres-0 -- pg_dump -U eclipselink_user eclipselink | gzip > backup.sql.gz

# Restore
gunzip -c backup.sql.gz | kubectl exec -i postgres-0 -- psql -U eclipselink_user eclipselink
```

## Security

- All secrets are base64-encoded (not encrypted by default)
- Use sealed-secrets or external-secrets for production
- Enable RBAC and network policies
- Use pod security policies
- Regular security audits

## Support

For issues with Kubernetes deployment, contact: devops@rohimaya.ai

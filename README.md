# Metabase with PostgreSQL

A production-ready Docker Compose stack for Metabase with:

- **PostgreSQL** — application database (required)
- **Metabase** — business intelligence and analytics

---

## Architecture

```
┌─────────────────┐
│    Metabase      │◄── Web UI (port 3000)
│  (BI Platform)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   PostgreSQL     │
│  (App Database)  │
└─────────────────┘
```

All services communicate over the internal `backend` bridge network.

---

## Quick Start

```bash
# 1. Copy the example env file and generate secrets
uv run generate-secrets.py

# 2. Review .env and start
docker compose up -d
```

Metabase will be available at **http://localhost:3000**

---

## Stop & Cleanup

```bash
# Stop containers (preserves volumes)
docker compose stop

# Stop AND remove containers, networks (keeps volumes)
docker compose down

# Full cleanup including volumes ⚠️ DATA LOSS
docker compose down -v
```

---

## Configuration

All configuration lives in `.env` (copy from `.env.example`).

| Variable | Description | Required |
|----------|-------------|----------|
| `METABASE_VERSION` | Metabase image tag (default: `latest`) | ❌ |
| `POSTGRES_VERSION` | PostgreSQL image tag (e.g., `17-alpine`) | ✅ |
| `MB_DB_TYPE` | Database type (default: `postgres`) | ✅ |
| `MB_DB_DBNAME` | Database name (default: `metabase`) | ✅ |
| `MB_DB_PORT` | Database port (default: `5432`) | ✅ |
| `MB_DB_USER` | Database user (default: `metabase`) | ✅ |
| `MB_DB_PASS` | Database password | ✅ |
| `MB_DB_HOST` | Database host (default: `database`) | ✅ |

---

## Persistence

Local bind mounts (survive `docker compose down`):

| Mount | Service | Contents |
|-------|---------|----------|
| `./postgres-data` | database | PostgreSQL data directory |
| `./uploads` | metabase | File uploads |

Backup strategy:

```bash
# Backup database
docker compose exec database pg_dump -U metabase metabase > backup_$(date +%F).sql
```

---

## Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `database` healthcheck fails | Volume permissions | `sudo chown -R 999:999 ./postgres-data` |
| Metabase won't start | Missing secrets | Ensure `MB_DB_PASS` is set in `.env` |
| Slow queries | No indexing | Use Metabase's query caching settings |

---

## Security Notes

- `.env` is **gitignored** — never commit real secrets
- `backend` network is `internal: true` — no external access
- Metabase binds to `127.0.0.1:3000` — localhost only
- PostgreSQL uses dedicated user for Metabase connections

---

## Upgrading Metabase

1. Update `METABASE_VERSION` in `.env`
2. `docker compose pull`
3. `docker compose up -d` (handles rolling restart with healthchecks)

> **Always backup `postgres-data` before major version upgrades.**

---

## License

MIT — use freely, modify, distribute.

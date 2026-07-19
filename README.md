# Metabase with PostgreSQL

A single-host Docker Compose stack for Metabase with:

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
# One command bootstrap
./bootstrap.sh

# Or do it manually
cp .env.example .env
docker compose up -d
```

Metabase will be available at **http://localhost:3000**

To regenerate `.env` directly, run `./generate-secrets.py --force`.

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
| `METABASE_VERSION` | Metabase image tag (default: `v0.63.x`) | ❌ |
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
| `./plugins` | metabase | Optional plugins |

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
| Metabase won't start | Missing secrets | Ensure `MB_DB_PASS` and `MB_ENCRYPTION_SECRET_KEY` are set in `.env` |
| Slow queries | No indexing | Use Metabase's query caching settings |

---

## Security Notes

- `.env` is **gitignored** — never commit real secrets
- `backend` network is `internal: true` — no external access
- Metabase binds to `127.0.0.1:3000` — localhost only
- PostgreSQL uses a dedicated writable user for Metabase’s application database

---

## Production checklist

Use these before exposing it to the internet:

- Put Metabase behind a reverse proxy with TLS.
- Set `MB_SITE_URL` to your real HTTPS URL.
- Back up `postgres-data`, `uploads`, and `plugins`.
- Keep `MB_ENABLE_TEST_ENDPOINTS` off.
- Monitor `docker compose logs` and disk space.

---

## Upgrading Metabase

1. Update `METABASE_VERSION` in `.env`
2. `docker compose pull`
3. `docker compose up -d` (handles rolling restart with healthchecks)

> **Always backup `postgres-data` before major version upgrades.**

---

## License

MIT — use freely, modify, distribute.

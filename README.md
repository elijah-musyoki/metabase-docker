# Metabase with PostgreSQL

A single-host Docker Compose stack for Metabase.

It includes:
- PostgreSQL for the application database
- Metabase for analytics and dashboards

---

## Layout

```
Metabase   →  Web UI on port 3000
PostgreSQL → Application database
```

All services use the internal `backend` network.

---

## Quick start

```bash
./bootstrap.sh
```

If you want to do it by hand:

```bash
cp .env.example .env
docker compose up -d
```

Open:
- `http://localhost:3000`

To regenerate `.env`, run:
- `./generate-secrets.py --force`

---

## Stop

```bash
docker compose stop
```

To remove containers and networks:

```bash
docker compose down
```

To remove everything, including volumes:

```bash
docker compose down -v
```

---

## Configure

Edit `.env`.
Copy it from `.env.example`.

Set these values:

| Variable | Meaning |
|---|---|
| `METABASE_VERSION` | Metabase image tag |
| `POSTGRES_VERSION` | PostgreSQL image tag |
| `MB_DB_TYPE` | Database type |
| `MB_DB_DBNAME` | Database name |
| `MB_DB_PORT` | Database port |
| `MB_DB_USER` | Database user |
| `MB_DB_PASS` | Database password |
| `MB_DB_HOST` | Database host |
| `MB_SITE_URL` | Public URL |
| `MB_ENCRYPTION_SECRET_KEY` | Encryption key |

Other values:
- `MB_JETTY_HOST`
- `MB_JETTY_MAXTHREADS`
- `MB_ASYNC_QUERY_THREAD_POOL_SIZE`
- `JAVA_TOOL_OPTIONS`
- `MAX_SESSION_AGE`
- `MB_QUERY_CACHING_MAX_TTL`
- `MB_APPLICATION_DB_MAX_CONNECTION_POOL_SIZE`

---

## Secrets

Generate or refresh `.env` with:

```bash
./generate-secrets.py --force
```

---

## Persistent data

Bind mounts survive `docker compose down`.

| Mount | Service | Use |
|---|---|---|
| `./postgres-data` | database | PostgreSQL data |
| `./uploads` | metabase | File uploads |
| `./plugins` | metabase | Optional plugins |

Backup:

```bash
docker compose exec database pg_dump -U metabase metabase > backup_$(date +%F).sql
```

---

## Common issues

| Symptom | Cause | Fix |
|---|---|---|
| `database` healthcheck fails | Volume permissions | `sudo chown -R 999:999 ./postgres-data` |
| Metabase will not start | Missing secrets | Set `MB_DB_PASS` and `MB_ENCRYPTION_SECRET_KEY` |
| Slow queries | No indexing | Use Metabase query caching |

---

## Security notes

- `.env` is gitignored.
- Do not commit real secrets.
- The `backend` network is internal.
- Metabase binds to `127.0.0.1:3000`.
- PostgreSQL uses a dedicated writable user.

---

## Production checklist

Use these before you put it on the internet:

- Put Metabase behind TLS.
- Set `MB_SITE_URL` to your real HTTPS URL.
- Back up `postgres-data`, `uploads`, and `plugins`.
- Keep `MB_ENABLE_TEST_ENDPOINTS` off.
- Watch `docker compose logs` and disk use.

---

## Upgrade

1. Change `METABASE_VERSION` in `.env`.
2. Run `docker compose pull`.
3. Run `docker compose up -d`.

Always back up `postgres-data` before a major upgrade.

---

## License

MIT. Use it, change it, share it.

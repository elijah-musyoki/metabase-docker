# Agent Instructions

## Package manager
None. This project uses Docker Compose.

## Commands

| Task | Command |
|---|---|
| Start | `./bootstrap.sh` |
| Start only | `docker compose up -d` |
| Stop | `docker compose down` |
| Stop and keep volumes | `docker compose stop` |
| Remove everything | `docker compose down -v` |
| Pull images | `docker compose pull` |
| Logs | `docker compose logs -f` |

## Key files

| Need | File |
|---|---|
| Config | `.env.example` |
| Research | `research/README.md` |
| Services | `docker-compose.yml` |
| Secrets | `generate-secrets.py` |
| Bootstrap | `bootstrap.sh` |

## Key rules

- Keep secrets in `.env`.
- Do not commit `.env`.
- Use `./bootstrap.sh` on first run.
- It creates `.env` if it is missing.
- It creates the bind-mount directories.
- It validates Compose before start.
- Metabase does not use Redis.
- Its cache is database-backed.
- The health check is `curl --fail -I http://localhost:3000/api/health`.
- First boot takes time for migrations.
- Wait 2 to 5 minutes on the first run.

## Commit attribution

```
Co-Authored-By: opencode <support@opencode.ai>
```

# Agent Instructions

## Package Manager
N/A — Docker Compose project.

## Commands
| Task | Command |
|------|---------|
| Start | `docker compose up -d` |
| Stop | `docker compose down` |
| Stop (preserve volumes) | `docker compose stop` |
| Full cleanup (data loss) | `docker compose down -v` |
| Pull images | `docker compose pull` |
| Logs | `docker compose logs -f` |

## External References
| Need | File |
|------|------|
| Config | `.env.example` |
| Research | `research/README.md` |
| Services | `docker-compose.yml` |
| Secrets | `generate-secrets.py` |

## Key Conventions
- Secrets in `.env` — gitignored, never commit.
- First deploy: `uv run generate-secrets.py`, then `docker compose up -d`.
- Metabase does NOT use Redis — caching is database-backed.
- Health check: `curl --fail -I http://localhost:3000/api/health`.
- First boot runs migrations (2-5 minutes) — normal.
- Agent notes and quirks live in `agent-notes/` (gitignored).

## Commit Attribution
```
Co-Authored-By: opencode <support@opencode.ai>
```

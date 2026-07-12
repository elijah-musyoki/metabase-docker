#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["structlog"]
# ///
"""Generate secure secrets for Metabase Docker Compose."""

import secrets
import sys
from pathlib import Path

try:
    import structlog
except ImportError:
    print("Run with: uv run generate-secrets.py", file=sys.stderr)
    sys.exit(1)

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer(),
    ],
)
log = structlog.get_logger()


def generate_secret(length: int = 32) -> str:
    return secrets.token_urlsafe(length)


def main() -> None:
    env_file = Path(".env")
    env_example = Path(".env.example")

    if not env_example.exists():
        log.error("Missing .env.example — run from repo root")
        sys.exit(1)

    if env_file.exists():
        answer = input(".env already exists. Overwrite? [y/N] ").strip().lower()
        if answer != "y":
            log.info("Aborted")
            sys.exit(0)

    secrets_to_generate = {
        "MB_DB_PASS": generate_secret(24),
        "MB_ENCRYPTION_SECRET_KEY": generate_secret(32),
    }

    log.info("Generated secrets", secrets=list(secrets_to_generate.keys()))

    content = env_example.read_text()
    for key, value in secrets_to_generate.items():
        content = content.replace(f"{key}=", f"{key}={value}", 1)

    env_file.write_text(content)
    log.info("Wrote .env", path=str(env_file))
    log.info("Done — review .env and run: docker compose up -d")


if __name__ == "__main__":
    main()

# RuneSeal Architecture Guide 🧱

This document outlines the internal architecture, component breakdown, and system responsibilities of the RuneSeal vault.

---

## ⚙️ Core Components

| Layer         | Responsibility |
|---------------|----------------|
| **FastAPI**   | Auth, secret access, user lifecycle, audit tracking |
| **PostgreSQL**| Durable state: users, secrets, tokens, logs |
| **Typer CLI** | `runeseal` + `rs` commands to interface with the API |
| **Docker Compose** | Orchestration of services, persistent volumes |
| **Cloudflare Tunnel** (optional) | Public-facing secure API exposure |

---

## 🔐 Auth & Security

- **Hashed Passwords**: Argon2 + salt per user (no plaintext ever)
- **JWT Tokens**: Per-session with TTL and scope checks
- **API Token**: Global `X-API-Key` check before request routing
- **Rate-limiting**: Brute-force safe; user lockouts
- **Audit Logs**: Actor, action, time, IP, device

---

## 📦 CLI Flow

1. Authenticate via `runeseal login`
2. Store session token and API key in `~/.runesealrc`
3. Use CLI commands (`secret add`, `user delete`, etc.)
4. Logs auto-generated for every action

---

## 🧼 User Lifecycle

- First user created becomes `admin`
- All passwords provided at setup (manual or YAML-based)
- No impersonation feature—everything fully attributable
- Users can be soft-deleted or purged

---

## 🔐 Secret Lifecycle

- Owners control write/delete access to their secrets
- Secrets are encrypted before storage
- Historical versions retained unless purged
- Admins can restore or force-delete secrets

---

## 📡 Deployment

- API exposed on configurable port (default: 8443)
- Mounted volumes: DB data, vault config, optional backup scripts
- Compatible with Unraid via standard Docker setup

---

Crafted to be tight, testable, auditable — and yours.

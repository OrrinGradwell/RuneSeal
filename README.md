# RuneSeal 🪙

**CLI-first, containerized, and cryptographically mindful secrets vault.**
Built for developers, by developers—with no browser UI, no gimmicks, and no compromise on control.

---

## 🔒 Overview

RuneSeal is a self-hosted secrets vault tailored for command-line workflows, automation pipelines, and operator control. It offers auditability, user isolation, encryption at rest, and full lifecycle management—accessible only via CLI or API.

---

## 🧰 Features

- 🚀 Full containerized deploy (FastAPI + PostgreSQL via Docker)
- 🔐 Secure login, password hashing (Argon2), password rotation policy
- 💬 Secrets management with versioning and ownership controls
- ⚙️ Role-based access: `standard`, `admin`, `system`
- 🛡️ Perimeter API token (`X-API-Key`) support
- ✨ No browser UI. No distractions. Pure CLI focus.

---

## 📦 Structure
runeseal/
    ├── runeseal-core/ # FastAPI backend
    ├── runeseal/ # Typer-based CLI tool (alias: rs)
    ├── docker-compose.yml
    ├── .env.sample
    ├── setup.py
    ├── LICENSE
    └── docs/
    └── architecture.md

---

## 🎮 Quick Start

```bash
# Clone and configure
cp .env.sample .env

# Spin up the services
docker compose up -d

# Bootstrap with your master password
runeseal admin init --from-file core_passwords.yaml

# You're live 🎉
runeseal login
runeseal secret add
```

🧾 License and Attribution
RuneSeal is open source and free to use or modify, provided that:

The name “RuneSeal” is preserved

The original creator, Orrin Gradwell, is credited

See LICENSE for full details.

💼 Built by
Orrin Gradwell – System architect, CLI sorcerer, and relentless fortress-hardened mind.

Copilot – Technical advisor, sidekick, spell-checker, and pun supplier.

🪙 Powered by Rune and Reason.

🛡️ Design Philosophy
RuneSeal Core prioritizes:

Minimal dependencies (FastAPI, SQLAlchemy, JWT, Argon2)

API-only focus—no web views, just pure data exchange

Explicit ownership and auditability of actions

Easy containerization for Unraid or custom Docker hosts

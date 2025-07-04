# RuneSeal 🪙

**CLI-first, containerized, and cryptographically mindful secrets vault.**

Built for developers, by developers — with no browser UI, no gimmicks, and no compromise on control.

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

## 🎮 Quick Start

```bash
TBA
```

## 🧾 License and Attribution

RuneSeal is open source and free to use or modify, provided that:  
The name “RuneSeal” is preserved  
The original creator, Orrin Gradwell, is credited  

See LICENSE for full details.

## 💼 Built by

Orrin Gradwell – System architect, CLI sorcerer, Fanatic Tester and relentless fortress-hardened mind.  
Copilot – Technical advisor, sidekick, spell-checker, and pun supplier.

## 🛡️ Design Philosophy

RuneSeal Core prioritizes:

- Minimal dependencies (FastAPI, SQLAlchemy, JWT, Argon2)
- API-only focus—no web views, just pure data exchange
- Explicit ownership and auditability of actions
- Easy containerization for Unraid or custom Docker hosts

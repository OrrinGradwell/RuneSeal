# 🔐 RuneSeal Core

This is the FastAPI backend service for [RuneSeal](../README.md)—a CLI-first, containerized secrets vault system.

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.10+
- PostgreSQL instance (containerized or external)
- Optional: Docker + Docker Compose

---

### 2. Environment Configuration

Create a `.env` in the project root (or use the one provided at `/../.env.sample`) with:

```env
POSTGRES_USER=runeseal_user
POSTGRES_PASSWORD=runeseal_secure_pass
POSTGRES_DB=runeseal_db
JWT_SECRET=supersecurevaulttoken
X_API_KEY=manual-dev-key
SYSTEM_PASSWORD=rune-based-encryption-secret

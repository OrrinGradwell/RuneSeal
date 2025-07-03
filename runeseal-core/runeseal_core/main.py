from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from runeseal_core.database import init_db
from runeseal_core.routers import admin, auth, secrets

app = FastAPI(title="RuneSeal API", version="1.0.0")

# Allow CORS if needed (adjust origins in production!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize database on startup
@app.on_event("startup")
def startup():
    init_db()


# Mount API route modules
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(secrets.router, prefix="/secrets", tags=["secrets"])

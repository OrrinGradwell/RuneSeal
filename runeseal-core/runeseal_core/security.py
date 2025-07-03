from fastapi.security import APIKeyHeader

oauth2_scheme = APIKeyHeader(name="Authorization")

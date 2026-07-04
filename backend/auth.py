from fastapi import Header, HTTPException

from backend.config import ADMIN_API_KEY


def require_admin(x_admin_key: str | None = Header(default=None)) -> None:
    if not ADMIN_API_KEY:
        return
    if x_admin_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing admin API key")

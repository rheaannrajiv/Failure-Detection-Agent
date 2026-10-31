"""Session ownership and Supabase access-token verification."""
from __future__ import annotations
import base64, hashlib, hmac, os, time
from typing import Optional
from uuid import UUID, uuid4
import requests
from fastapi import HTTPException


def _config():
    url = os.getenv("SUPABASE_URL", "").strip().rstrip("/")
    service = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()
    anon = os.getenv("SUPABASE_ANON_KEY", "").strip()
    secret = os.getenv("GUEST_SESSION_SECRET", "").strip()
    if not url or not service:
        raise HTTPException(503, "Supabase persistence is not configured.")
    return url, service, anon, secret


def _db_headers(service: str):
    return {"apikey": service, "Authorization": f"Bearer {service}", "Content-Type": "application/json"}


def _guest_token(session_id: str, secret: str) -> str:
    if len(secret) < 32:
        raise HTTPException(503, "GUEST_SESSION_SECRET must contain at least 32 characters.")
    expires = int(time.time()) + 60 * 60 * 24 * 30
    body = f"{session_id}.{expires}"
    sig = hmac.new(secret.encode(), body.encode(), hashlib.sha256).digest()
    return base64.urlsafe_b64encode(body.encode()).decode().rstrip("=") + "." + base64.urlsafe_b64encode(sig).decode().rstrip("=")


def _verify_guest(token: str, session_id: str, secret: str) -> bool:
    try:
        body64, sig64 = token.split(".", 1)
        body = base64.urlsafe_b64decode(body64 + "=" * (-len(body64) % 4)).decode()
        sig = base64.urlsafe_b64decode(sig64 + "=" * (-len(sig64) % 4))
        expected = hmac.new(secret.encode(), body.encode(), hashlib.sha256).digest()
        sid, exp = body.split(".", 1)
        return hmac.compare_digest(sig, expected) and sid == session_id and int(exp) > int(time.time())
    except Exception:
        return False


def _supabase_user(access_token: str, url: str, anon: str) -> str:
    if not anon:
        raise HTTPException(503, "SUPABASE_ANON_KEY is required for user authentication.")
    try:
        r = requests.get(f"{url}/auth/v1/user", headers={"apikey": anon, "Authorization": f"Bearer {access_token}"}, timeout=10)
        if r.status_code != 200:
            raise HTTPException(401, "Invalid or expired Supabase access token.")
        return str(UUID(r.json()["id"]))
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(503, f"Could not verify Supabase access token: {exc}") from exc


def create_guest_session() -> dict:
    url, service, _, secret = _config()
    sid = str(uuid4())
    token = _guest_token(sid, secret)
    digest = hashlib.sha256(token.encode()).hexdigest()
    r = requests.post(f"{url}/rest/v1/diagnostic_sessions", headers={**_db_headers(service), "Prefer": "return=minimal"}, json={"session_id": sid, "guest_token_hash": digest}, timeout=12)
    if r.status_code >= 400:
        raise HTTPException(503, f"Could not create guest session ({r.status_code}). Check the Milestone 7 SQL migration.")
    return {"session_id": sid, "guest_token": token, "expires_in": 2592000, "mode": "guest"}


def create_user_session(access_token: str) -> dict:
    url, service, anon, _ = _config()
    owner = _supabase_user(access_token, url, anon)
    sid = str(uuid4())
    r = requests.post(f"{url}/rest/v1/diagnostic_sessions", headers={**_db_headers(service), "Prefer": "return=minimal"}, json={"session_id": sid, "owner_user_id": owner}, timeout=12)
    if r.status_code >= 400:
        raise HTTPException(503, f"Could not create user session ({r.status_code}).")
    return {"session_id": sid, "mode": "authenticated"}


def require_session_owner(session_id: str, authorization: Optional[str], guest_token: Optional[str]) -> str:
    url, service, anon, secret = _config()
    try:
        sid = str(UUID(session_id))
    except Exception as exc:
        raise HTTPException(422, "A valid session_id is required.") from exc
    owner = None
    digest = None
    if authorization and authorization.lower().startswith("bearer "):
        owner = _supabase_user(authorization.split(" ", 1)[1].strip(), url, anon)
    elif guest_token:
        if not secret or not _verify_guest(guest_token, sid, secret):
            raise HTTPException(401, "Invalid or expired guest session token.")
        digest = hashlib.sha256(guest_token.encode()).hexdigest()
    else:
        raise HTTPException(401, "Provide a Supabase Bearer token or X-Guest-Token.")
    params = {"session_id": f"eq.{sid}", "select": "session_id,owner_user_id,guest_token_hash", "limit": "1"}
    r = requests.get(f"{url}/rest/v1/diagnostic_sessions", headers=_db_headers(service), params=params, timeout=12)
    if r.status_code >= 400:
        raise HTTPException(503, "Could not verify diagnostic session ownership.")
    rows = r.json()
    if not rows:
        raise HTTPException(404, "Diagnostic session not found.")
    row = rows[0]
    if owner and row.get("owner_user_id") != owner:
        raise HTTPException(403, "This diagnostic session belongs to another user.")
    if digest and not hmac.compare_digest(row.get("guest_token_hash") or "", digest):
        raise HTTPException(403, "This guest token does not own the diagnostic session.")
    return sid

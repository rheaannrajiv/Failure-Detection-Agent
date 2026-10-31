"""Optional server-side conversation persistence through Supabase REST.
Only the backend service-role key is used; never expose it to browser clients."""
from __future__ import annotations
import os
from typing import Any
import requests

class MemoryUnavailable(RuntimeError):
    pass

class SupabaseMemory:
    def __init__(self) -> None:
        self.url = os.getenv("SUPABASE_URL", "").strip().rstrip("/")
        self.key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()

    @property
    def enabled(self) -> bool:
        return bool(self.url and self.key)

    def _headers(self) -> dict[str, str]:
        return {"apikey": self.key, "Authorization": f"Bearer {self.key}", "Content-Type": "application/json", "Prefer": "return=minimal"}

    def load_history(self, session_id: str, limit: int = 8) -> list[dict[str, str]]:
        if not self.enabled:
            return []
        params = {"session_id": f"eq.{session_id}", "select": "role,content", "order": "created_at.desc", "limit": str(max(1, min(limit, 20)))}
        response = requests.get(f"{self.url}/rest/v1/diagnostic_messages", headers=self._headers(), params=params, timeout=12)
        if response.status_code >= 400:
            raise MemoryUnavailable(f"Supabase history read failed ({response.status_code}): {response.text[:300]}")
        rows = response.json()
        return [{"role": row["role"], "content": row["content"]} for row in reversed(rows) if row.get("role") in {"user", "assistant"}]

    def append_turn(self, session_id: str, user_message: str, assistant_message: str, metadata: dict[str, Any] | None = None) -> None:
        if not self.enabled:
            return
        rows = [
            {"session_id": session_id, "role": "user", "content": user_message[:12000], "metadata": {}},
            {"session_id": session_id, "role": "assistant", "content": assistant_message[:12000], "metadata": metadata or {}},
        ]
        response = requests.post(f"{self.url}/rest/v1/diagnostic_messages", headers=self._headers(), json=rows, timeout=12)
        if response.status_code >= 400:
            raise MemoryUnavailable(f"Supabase history write failed ({response.status_code}): {response.text[:300]}")

memory_store = SupabaseMemory()

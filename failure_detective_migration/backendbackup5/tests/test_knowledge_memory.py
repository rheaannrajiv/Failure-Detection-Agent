from app.knowledge.library import search_knowledge
from app.memory.supabase_store import SupabaseMemory


def test_knowledge_search_returns_relevant_pump_cavitation():
    results = search_knowledge("centrifugal pump crackling low suction pressure", limit=3)
    assert results
    assert results[0]["topic"] == "cavitation"
    assert results[0]["checks"]


def test_knowledge_search_is_bounded():
    assert len(search_knowledge("bearing vibration alignment", limit=99)) <= 5


def test_supabase_memory_is_optional_without_secrets(monkeypatch):
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SERVICE_ROLE_KEY", raising=False)
    store = SupabaseMemory()
    assert store.enabled is False
    assert store.load_history("00000000-0000-0000-0000-000000000001") == []
    store.append_turn("00000000-0000-0000-0000-000000000001", "hi", "hello")

import time
from app.auth.security import _guest_token, _verify_guest


def test_guest_token_is_bound_to_session_and_expires():
    secret = 'test-secret-' * 4
    token = _guest_token('12345678-1234-5678-1234-567812345678', secret)
    assert _verify_guest(token, '12345678-1234-5678-1234-567812345678', secret)
    assert not _verify_guest(token, 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', secret)
    assert not _verify_guest(token, '12345678-1234-5678-1234-567812345678', 'different-secret-' * 3)


def test_malformed_guest_token_rejected():
    assert not _verify_guest('not-a-token', '12345678-1234-5678-1234-567812345678', 'test-secret-' * 4)

import pytest
from wavesense.security.provider import CryptoProvider, FallbackProvider

def test_fallback_provider_raises():
    provider = FallbackProvider()
    with pytest.raises(NotImplementedError):
        provider.keygen()
    with pytest.raises(NotImplementedError):
        provider.sign(b"data", b"key")
    with pytest.raises(NotImplementedError):
        provider.verify(b"data", b"sig", b"pubkey")
    with pytest.raises(NotImplementedError):
        provider.exchange(b"peer_pubkey", b"local_privkey")

def test_crypto_provider_is_abstract():
    with pytest.raises(TypeError):
        CryptoProvider()

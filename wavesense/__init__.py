from wavesense.security.provider import CryptoProvider, FallbackProvider

__version__ = "0.1.0"

def init(crypto: CryptoProvider | None = None) -> dict:
    return {"crypto": crypto or FallbackProvider()}

__all__ = ["init", "CryptoProvider", "FallbackProvider"]

from abc import ABC, abstractmethod
from typing import Tuple

class CryptoProvider(ABC):
    @abstractmethod
    def keygen(self) -> Tuple[bytes, bytes]:
        """Retorna (private_key, public_key)"""

    @abstractmethod
    def sign(self, data: bytes, private_key: bytes) -> bytes:
        """Assina dados"""

    @abstractmethod
    def verify(self, data: bytes, signature: bytes, public_key: bytes) -> bool:
        """Verifica assinatura"""

    @abstractmethod
    def exchange(self, peer_public_key: bytes, local_private_key: bytes) -> bytes:
        """Deriva chave de sessão"""

class FallbackProvider(CryptoProvider):
    def keygen(self) -> Tuple[bytes, bytes]:
        raise NotImplementedError("Implementar provider criptográfico")
    def sign(self, data: bytes, private_key: bytes) -> bytes:
        raise NotImplementedError
    def verify(self, data: bytes, signature: bytes, public_key: bytes) -> bool:
        raise NotImplementedError
    def exchange(self, peer_public_key: bytes, local_private_key: bytes) -> bytes:
        raise NotImplementedError

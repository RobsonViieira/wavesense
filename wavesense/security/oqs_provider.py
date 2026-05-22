import oqs
from .provider import CryptoProvider
from typing import Tuple

class OQSCryptoProvider(CryptoProvider):
    """Implementação PQC usando Kyber768 (KEM) + Dilithium (assinatura)."""
    
    def __init__(self, kem_alg: str = "Kyber768", sig_alg: str = "Dilithium3"):
        self.kem = oqs.KeyEncapsulation(kem_alg)
        self.sig = oqs.Signature(sig_alg)
    
    def keygen(self) -> Tuple[bytes, bytes]:
        public_key = self.sig.generate_keypair()
        return (b"<private_key_placeholder>", public_key)
    
    def sign(self, data: bytes, private_key: bytes) -> bytes:
        return self.sig.sign(data)
    
    def verify(self, data: bytes, signature: bytes, public_key: bytes) -> bool:
        return self.sig.verify(data, signature, public_key)
    
    def exchange(self, peer_public_key: bytes, local_private_key: bytes) -> bytes:
        ctxt, shared_secret = self.kem.encap_secret(peer_public_key)
        return shared_secret

from typing import Protocol, Dict, List, Any, Optional
from dataclasses import dataclass

class QuantumOffload(Protocol):
    def simulate_rf(self, env_config: Dict[str, Any]) -> Dict[str, Any]: ...
    def optimize_pipeline(self, constraints: Dict[str, Any]) -> Dict[str, Any]: ...
    def verify_privacy(self, updates: List[bytes]) -> bool: ...

@dataclass
class QuantumResult:
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class ClassicalFallback:
    def simulate_rf(self, env_config: Dict[str, Any]) -> QuantumResult:
        return QuantumResult(success=False, error="Quantum simulation not available")
    def optimize_pipeline(self, constraints: Dict[str, Any]) -> QuantumResult:
        return QuantumResult(success=True, data=constraints)
    def verify_privacy(self, updates: List[bytes]) -> QuantumResult:
        return QuantumResult(success=len(updates) > 0)

def get_quantum_offload(use_quantum: bool = False) -> QuantumOffload:
    if use_quantum:
        try:
            from .qiskit_adapter import QiskitOffload
            return QiskitOffload()
        except ImportError:
            pass
    return ClassicalFallback()

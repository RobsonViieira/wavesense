import asyncio
from typing import AsyncIterator, Optional, Callable
from dataclasses import dataclass
from collections import deque
import numpy as np

@dataclass
class CSISample:
    timestamp: float
    csi_matrix: np.ndarray  # [subcarriers, antennas, complex]
    metadata: dict

class CSICapture:
    """Leitura assíncrona de CSI com buffer circular e backpressure."""
    
    def __init__(self, buffer_size: int = 1024, sample_rate: float = 100.0):
        self.buffer = deque(maxlen=buffer_size)
        self.sample_rate = sample_rate
        self._running = False
        self._callbacks: list[Callable[[CSISample], None]] = []
    
    async def start(self, device: str = "/dev/esp32_csi"):
        """Inicia captura assíncrona do dispositivo."""
        self._running = True
        # Em produção: conectar ao ESP32 via UART/USB/WiFi
        while self._running:
            sample = await self._read_sample(device)
            if sample:
                self.buffer.append(sample)
                for cb in self._callbacks:
                    cb(sample)
            await asyncio.sleep(1 / self.sample_rate)
    
    async def _read_sample(self, device: str) -> Optional[CSISample]:
        """Stub: substituir por leitura real do firmware ESP32."""
        return CSISample(
            timestamp=asyncio.get_event_loop().time(),
            csi_matrix=np.random.randn(56, 3, 2) + 1j*np.random.randn(56, 3, 2),
            metadata={"rssi": -45, "device": device}
        )
    
    def stop(self):
        self._running = False
    
    def register_callback(self, cb: Callable[[CSISample], None]):
        self._callbacks.append(cb)
    
    def get_recent(self, count: int = 10) -> list[CSISample]:
        return list(self.buffer)[-count:]

#!/usr/bin/env python3
"""
wavesense — Demonstração básica do pipeline completo

Este exemplo mostra:
1. Inicialização do SDK com injeção de provedor criptográfico
2. Captura assíncrona simulada de CSI (substituir por ESP32 real)
3. Processamento, classificação e dispatch com callbacks
4. Uso de configuração via variáveis de ambiente

Execução:
    python examples/basic_demo.py

Pré-requisitos:
    pip install -e .[dev]  # ou uv pip install -e .[dev] --system --break-system-packages
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Optional

# Adicionar raiz do projeto ao path para imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from wavesense import init, CryptoProvider, FallbackProvider
from wavesense.core.capture import CSICapture, CSISample
from wavesense.security.provider import CryptoProvider

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("wavesense.demo")


def get_crypto_provider() -> Optional[CryptoProvider]:
    """
    Retorna o provedor criptográfico configurado.
    Prioridade: OQSCryptoProvider (se pyoqs instalado) > FallbackProvider.
    """
    # Tentar importar OQS (pós-quântico)
    try:
        from wavesense.security.oqs_provider import OQSCryptoProvider        logger.info("✅ Usando OQSCryptoProvider (Kyber768 + Dilithium)")
        return OQSCryptoProvider()
    except ImportError:
        logger.warning("⚠️ pyoqs não instalado — usando FallbackProvider")
        logger.warning("   Para PQC: pip install pyoqs cryptography")
        return FallbackProvider()


async def on_csi_sample(sample: CSISample):
    """Callback chamado a cada nova amostra de CSI capturada."""
    logger.debug(
        f"📡 CSI: ts={sample.timestamp:.3f} | "
        f"shape={sample.csi_matrix.shape} | "
        f"rssi={sample.metadata.get('rssi', 'N/A')}dBm"
    )
    # Em produção: enviar para processamento, classificar, etc.


async def on_classification_result(result: dict):
    """Callback chamado quando uma classificação é concluída."""
    action = result.get("action", "unknown")
    confidence = result.get("confidence", 0.0)
    logger.info(f"🎯 Classificação: {action} (confiança: {confidence:.2%})")
    
    # Dispatch: executar ação baseada no resultado
    if action == "fall_detected" and confidence > 0.85:
        logger.critical("🚨 ALERTA: Queda detectada! Acionando protocolo de emergência.")
        # Aqui: enviar webhook, MQTT, notificação, etc.


async def run_demo(duration_seconds: float = 10.0, sample_rate: float = 10.0):
    """
    Executa a demonstração completa do pipeline wavesense.
    
    Args:
        duration_seconds: Tempo de execução da demo em segundos.
        sample_rate: Frequência de amostragem simulada (Hz).
    """
    logger.info("🚀 Iniciando wavesense demo...")
    
    # 1. Inicializar SDK com provedor criptográfico
    crypto = get_crypto_provider()
    sdk = init(crypto=crypto)
    logger.info(f"🔐 Crypto provider: {type(sdk['crypto']).__name__}")
    
    # 2. Configurar captura de CSI
    capture = CSICapture(buffer_size=256, sample_rate=sample_rate)
    capture.register_callback(on_csi_sample)
    
    # 3. Simular loop de processamento/classificação    async def processing_loop():
        while capture._running:
            recent = capture.get_recent(count=5)
            if len(recent) >= 3:
                # Simular classificação (substituir por modelo real)
                result = {
                    "action": "walking" if len(recent) % 2 == 0 else "stationary",
                    "confidence": 0.92,
                    "timestamp": recent[-1].timestamp
                }
                await asyncio.sleep(0)  # Yield para async
                await on_classification_result(result)
            await asyncio.sleep(1.0 / sample_rate)
    
    # 4. Executar captura e processamento em paralelo
    try:
        await asyncio.wait_for(
            asyncio.gather(
                capture.start(device="mock_esp32"),
                processing_loop()
            ),
            timeout=duration_seconds
        )
    except asyncio.TimeoutError:
        logger.info("⏱️ Tempo de demo concluído.")
    finally:
        capture.stop()
        logger.info("🛑 Demo finalizada.")


def main():
    """Entry point para execução direta."""
    # Configuração via environment variables
    duration = float(os.getenv("WAVESENSE_DEMO_DURATION", "10.0"))
    rate = float(os.getenv("WAVESENSE_DEMO_RATE", "10.0"))
    
    logger.info(f"⚙️ Config: duration={duration}s, rate={rate}Hz")
    
    try:
        asyncio.run(run_demo(duration_seconds=duration, sample_rate=rate))
    except KeyboardInterrupt:
        logger.info("👋 Interrompido pelo usuário.")
    except Exception as e:
        logger.exception(f"❌ Erro na demo: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

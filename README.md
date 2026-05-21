# wavesense

> Transform any WiFi router into a behavioral sensing platform — no cameras, no wearables, no new hardware.

[![Status](https://img.shields.io/badge/status-in%20development-yellow)](https://github.com/RobsonViieira/wavesense)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![Hardware](https://img.shields.io/badge/hardware-ESP32-red)](https://www.espressif.com/)

---

## O que é

**wavesense** é um SDK Python open source que transforma sinais WiFi comuns em dados comportamentais — detectando presença, movimento, gestos, padrão de caminhada e sinais vitais passivos usando apenas um ESP32 e o roteador que já existe no ambiente.

A tecnologia se baseia em **CSI (Channel State Information)** — cada pacote WiFi transmitido carrega uma impressão física do ambiente. Corpos humanos alteram amplitude, fase e frequência desse sinal de formas mensuráveis e repetíveis.

Sem câmera. Sem wearable. Sem instalar nada novo.

---

## Como funciona

```
ESP32 (captura CSI)
    ↓
wavesense.capture()   — lê dados raw do sinal WiFi
wavesense.process()   — filtra ruído e extrai features
wavesense.classify()  — classifica com modelo ML
wavesense.dispatch()  — executa ação (webhook, MQTT, pyautogui)
```

---

## Casos de uso

| Vertical | Aplicação |
|---|---|
|  **AirControl** | Controle gestual sem hardware — smart home, acessibilidade |
|  **CareWave** | Monitoramento passivo de idosos — queda, rotina, anomalia |
|  **SleepWave** | Frequência respiratória e qualidade de sono passivos |
|  **GaitKey** | Autenticação biométrica pelo padrão de caminhada |
|  **IndustrialSens** | Presença e fadiga em ambiente industrial com EPI |
|  **CityBreath** | Fluxo e densidade urbana via WiFi público |

---

## Requisitos

- Python 3.9+
- ESP32 com firmware CSI habilitado
- Linux / macOS / WSL2

---

## Instalação

```bash
# Clone o repositório
git clone https://github.com/RobsonViieira/wavesense.git
cd wavesense

# Instale as dependências
pip install -r requirements.txt
```

---

## Quickstart

```python
import wavesense as ws

# Inicializa captura via ESP32
sensor = ws.capture(port="/dev/ttyUSB0", rate=100)

# Classifica gesto em tempo real
@sensor.on("gesture")
def handle(event):
    print(f"Gesto detectado: {event.label} ({event.confidence:.0%})")

sensor.start()
```

---

## Roadmap

- [ ] `v0.1` — Captura CSI raw via ESP32
- [ ] `v0.2` — Pipeline de processamento e extração de features
- [ ] `v0.3` — Modelo de gestos (AirControl) — 8 gestos, 90%+ acurácia
- [ ] `v0.4` — Modelo de presença e detecção de queda (CareWave)
- [ ] `v0.5` — SDK público com documentação completa
- [ ] `v1.0` — Release estável + marketplace de modelos ML

---

## Arquitetura

```
wavesense/
├── capture.py       # Leitura CSI do ESP32
├── process.py       # Filtro e extração de features
├── classify.py      # Inferência com modelo TFLite
└── dispatch.py      # Ações: MQTT, webhook, pyautogui

models/
└── gesture_v1.tflite

examples/
├── aircontrol.py    # Controle gestual
├── presence.py      # Detecção de presença
└── smart_home.py    # Integração Home Assistant

docs/
└── quickstart.md
```

---

## Base acadêmica

- Geng et al. (2023) — *DensePose From WiFi* — Carnegie Mellon University
- IEEE 802.11bf-2025 — WiFi Sensing como protocolo padrão
- Karlsruhe Institute of Technology (2025) — Identificação por gait via WiFi

---

## Licença

MIT License — veja [LICENSE](LICENSE) para detalhes.

---

## Autor

**Robson V.** — [@RobsonViieira](https://github.com/RobsonViieira)  
Itatiba, SP — Brasil  

---

* Em desenvolvimento ativo — contribuições e feedback são bem-vindos.*

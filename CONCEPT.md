# CONCEPT.md — wavesense

> Documento de visão fundadora. Registra o insight original, a arquitetura pretendida e a direção estratégica do projeto.

---

## O Insight

WiFi não é apenas tecnologia de internet. **WiFi é radar.**

Todo sinal WiFi que trafega num ambiente toca objetos, paredes e corpos humanos — e retorna alterado. Essas alterações físicas estão codificadas nos dados CSI (Channel State Information) que qualquer ESP32 consegue capturar. Frequência cardíaca, padrão de respiração, posição corporal, velocidade de movimento, gait (padrão de caminhada único por indivíduo) — tudo isso está presente nos sinais que os roteadores já emitem agora, 24 horas por dia.

O mundo físico inteiro já está sendo escaneado. Falta o software pra ler.

---

## O Problema que resolve

Os sistemas de monitoramento existentes têm limitações estruturais:

- **Câmeras** — invasivas, pontuais, exigem infraestrutura cara, rejeitadas em ambientes privados
- **Wearables** — dependem de adesão do usuário, dados insuficientes, bateria limitada
- **Sensores IoT** — precisam ser instalados, mantidos e calibrados por ambiente
- **GPS** — só funciona fora de edificações, requer dispositivo ativo com o usuário

**wavesense resolve isso usando o que já existe:** o roteador WiFi já instalado no ambiente, transformado em sensor comportamental passivo via ESP32 de R$25.

---

## Como funciona tecnicamente

### CSI — Channel State Information

Cada pacote WiFi transmitido carrega uma matriz CSI com informações sobre como o sinal se propagou pelo ambiente. Quando um corpo humano está presente, ele altera:

- **Amplitude** — intensidade do sinal refletido
- **Fase** — deslocamento temporal da onda
- **Frequência** — efeito Doppler causado por movimento

Capturando essas variações em alta frequência (100Hz+) e processando com ML, é possível classificar comportamentos com precisão superior a 90%.

### Pipeline

```
[ESP32]
Captura matriz CSI raw — 64 subportadoras a 100Hz
Transmite via serial/UDP para processador edge

[Python — Edge]
Filtro Butterworth — remove ruído ambiental
Extração de features — amplitude, fase, variância, FFT
Janelamento temporal — segmentos de 200ms

[Modelo ML]
LSTM ou CNN 1D treinada em séries temporais de CSI
Classificação: gesto / presença / gait / vital signs
TFLite Micro — roda no próprio ESP32 (<500KB)

[Dispatch]
Ação baseada no evento classificado
MQTT, webhook REST, pyautogui, Home Assistant
```

---

## Verticais planejadas

### v0.1 — AirControl (gesto)
Controle gestual de dispositivos sem hardware adicional. Substitui Kinect, Leap Motion e Google Soli com ESP32 de R$25. Foco em acessibilidade para pessoas com mobilidade reduzida.

### v0.2 — CareWave (saúde / idosos)
Monitoramento passivo de idosos. Detecta quedas, anomalias de rotina e padrões de movimento associados a declínio cognitivo precoce. Sem câmera no quarto, sem wearable, sem fricção.

### v0.3 — SleepWave (sono / respiração)
Monitoramento de frequência respiratória e fases do sono via padrão de movimento do peito. Detecção de apneia sem máscara ou eletrodo.

### v0.4 — GaitKey (autenticação biométrica)
Autenticação pelo padrão de caminhada — único por indivíduo como impressão digital, impossível de falsificar remotamente.

### v0.5 — IndustrialSens (indústria)
Controle gestual em ambiente industrial com EPI. Confirmação de presença em postos de trabalho. Detecção de fadiga por padrão de movimento.

### v1.0 — CityBreath (cidades)
Sensing urbano via WiFi público existente. Fluxo pedestre, aglomerações, comportamento anômalo em espaços públicos.

---

## Modelo de negócio pretendido

**SDK open source + SaaS pago por volume.**

```
Free tier      — até 1.000 chamadas/mês
Developer      — R$97/mês
Commercial     — R$490/mês
Enterprise     — R$1.900/mês + suporte
Modelos ML     — R$197 por modelo pré-treinado (pagamento único)
```

Canal de aquisição principal: GitHub orgânico → dev adota → empresa paga.

---

## Stack técnica

| Camada | Tecnologia |
|---|---|
| Hardware | ESP32 + firmware CSI (ESP32-CSI-Tool) |
| Edge | Python 3.9+, scipy, numpy, TFLite |
| Cloud | AWS IoT Core, Lambda, SageMaker, DynamoDB |
| API | FastAPI, API Gateway |
| Interface | MQTT, webhooks REST |

---

## Base acadêmica

- Geng et al. (2023) — *DensePose From WiFi* — Carnegie Mellon University — [arXiv:2301.00250](https://arxiv.org/abs/2301.00250)
- IEEE 802.11bf-2025 — WiFi Sensing como protocolo padrão em novos chipsets
- Karlsruhe Institute of Technology (Out/2025) — Identificação de indivíduos por gait via WiFi com 90%+ de precisão
- MIT Media Lab — Detecção de frequência cardíaca passiva via sinais de rádio

---

## Visão de longo prazo

O padrão IEEE 802.11bf vai embutir capacidade de sensing em todos os novos roteadores. Quando isso acontecer, o mundo inteiro terá sido retrofitado com sensores sem perceber.

**wavesense quer ser o SDK de referência que lê esses dados** — antes que as BigTechs transformem isso em produto fechado e proprietário.

A infraestrutura já está instalada. O software é o produto.

---

## Status

 **Pré-desenvolvimento** — PoC em andamento com ESP32 e ESP32-CSI-Tool.

---

*Criado por Robson V. — Itatiba, SP — Brasil — 2026*

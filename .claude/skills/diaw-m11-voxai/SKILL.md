---
name: diaw-m11-voxai
description: >
  VOX-AI: AI-powered voice technology module. Builds voice assistants, IVR
  systems, speech-to-text transcription, text-to-speech synthesis, voice
  authentication, call center automation, and conversational AI for Arabic
  and English. Activates on VOX-AI, voice, speech, IVR, call center,
  transcription, text-to-speech, voice assistant, conversational AI.
user-invocable: true
context: fork
effort: high
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebSearch
  - mcp__ruflo__*
---

# VOX-AI: Voice AI Module v3.0

## Agent Swarm Configuration
- **Topology**: Pipeline | **Max Agents**: 4 | **Quality Gate**: 0.95
- **Agents**: Voice Coordinator, NLU Agent, TTS Agent, Integration Agent

## Core Capabilities

### Arabic + English Voice Processing
- **ASR (Automatic Speech Recognition)**: Arabic (MSA + Gulf dialect), English
- **TTS (Text-to-Speech)**: Natural-sounding Arabic and English voices
- **NLU**: Intent detection, entity extraction, sentiment analysis in Arabic
- **Dialect Support**: Gulf Arabic (UAE, Saudi, Kuwait), Egyptian, Levantine

### Voice Assistant Framework
```python
# Voice pipeline architecture
pipeline = [
    AudioCapture(format='PCM', sample_rate=16000),
    VAD(threshold=0.5),           # Voice Activity Detection
    ASR(model='whisper-large-v3', language=['ar', 'en']),
    NLU(intents=custom_intents, entities=custom_entities),
    DialogManager(context_window=10, memory='session'),
    ResponseGenerator(model='claude-haiku-4', language=detected_lang),
    TTS(voice='Zeina-Arabic' or 'Joanna-English', speed=1.0),
    AudioPlayback()
]
```

### IVR System Builder
```
IVR Flow Design:
  Welcome message (branded, professional)
  → Main menu (numbered options, DTMF or voice)
  → Sub-menus (nested up to 3 levels)
  → Intent routing (AI-detected intent → agent/department)
  → Queue management (estimated wait, callback option)
  → Escalation (human handoff with context transfer)
  → Post-call survey (automated 30-second satisfaction check)
```

### Call Center Automation
| Feature | Description |
|---------|-------------|
| Auto-attendant | 24/7 first-line handling |
| Sentiment Analysis | Real-time customer sentiment scoring |
| Agent Assist | Real-time suggestions during live calls |
| Call Summarization | Auto-generated call notes in CRM |
| Quality Monitoring | Compliance keyword detection |
| Voicemail AI | Transcription + priority classification |

### UAE/MENA Specializations
- Arabic RTL text processing and display
- UAE business hours and public holiday handling
- Integration with Etisalat/du/Virgin Mobile UAE SIP trunks
- TDRA compliance for IVR systems
- Multi-dialect switching within single conversation

## Revenue Model
- **Subscription**: $160/mo
- **Per-Minute**: $0.01-$0.05 for ASR/TTS processing
- **IVR Setup**: $1,000-$3,000 per system
- **Credits**: 15-50 per voice system build

## Example Invocations
- "VOX-AI: Build an Arabic/English IVR for a UAE bank's customer service line"
- "Create a voice assistant that transcribes customer calls and auto-fills CRM fields"
- "VOX-AI: Implement real-time agent assist that suggests responses during calls"

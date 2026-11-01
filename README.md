# U-AI - Unified AI Platform

A multi-API platform that integrates:
- **Background Removal** (birefnet API)
- **AI Council** (multi-AI consensus)
- **Image Generation** (ComfyUI + Qwen for non-food items)
- **Image Downloading** (Pinterest + web search)
- **Audio Generation** (ComfyUI workflows)
- **QR Code Generation** (external API)

## Setup

### 1. Configure API Keys

Create a `.env` file or edit `u_ai_config.json`:

```env
# Background Removal (birefnet)
BACKGROUND_REMOVAL_API_URL=https://api.birefnet.com/remove
BACKGROUND_REMOVAL_API_KEY=your_key_here

# AI Council
AI_COUNCIL_API_URL=https://api.aicouncil.com/consensus
AI_COUNCIL_API_KEY=your_key_here

# ComfyUI (local or remote)
COMFYUI_API_URL=http://localhost:8188
COMFYUI_API_KEY=

# Qwen (for food items)
QWEN_API_URL=https://api.qwen.com/generate
QWEN_API_KEY=your_key_here

# Pinterest
PINTEREST_API_URL=https://api.pinterest.com/search
PINTEREST_API_KEY=your_key_here

# QR Code
QR_CODE_API_URL=https://tzprasantofficial-ai.github.io/U-DESIGN-QR-
```

### 2. Install Dependencies

```bash
pip install google-genai requests urllib3
```

### 3. Run the Platform

```bash
# Run supervisor (main interface)
python u_ai_supervisor.py

# Run worker (individual tasks)
python u_ai_worker.py
```

## Usage Examples

### Remove Background

```python
from u_ai_worker import remove_background

result = remove_background("uploads/photo.jpg")
# Result: "uploads/photo_nobg.png"
```

### AI Council Consensus

```python
from u_ai_worker import ai_council_consensus

result = ai_council_consensus(
    topic="What is the future of AI?",
    max_time_minutes=5
)
# Result: Consensus from multiple AIs
```

### Generate Image

```python
from u_ai_worker import generate_image

result = generate_image(
    prompt="A beautiful sunset over mountains",
    width=512,
    height=512
)
# Result: "assets/generated/image_YYYYMMDD_HHMMSS.png"
```

### Download Image

```python
from u_ai_worker import download_image

result = download_image(
    query="ocean sunset",
    source="pinterest"  # or "web"
)
# Result: "assets/stock/pinterest_ocean_sunset.jpg"
```

### Generate Audio

```python
from u_ai_worker import generate_audio

result = generate_audio(
    prompt="Peaceful ocean waves",
    category="Music",
    duration=180
)
# Result: "assets/generated/audio_YYYYMMDD_HHMMSS.mp3"
```

### Generate QR Code

```python
from u_ai_worker import generate_qr_code

result = generate_qr_code("https://example.com")
# Result: "assets/generated/qr_YYYYMMDD_HHMMSS.png"
```

## Memory & Learning

U-AI learns from errors and stores fixes in `u_ai_memory.json`:

```json
{
  "learned_fixes": [
    {
      "timestamp": "2026-01-15T10:30:00",
      "error_signature": "ComfyUI timeout",
      "rating": 9,
      "fixed_code": "..."
    }
  ],
  "last_run": "2026-01-15T10:30:00"
}
```

## Architecture

```
u_ai_supervisor.py  - Main supervisor with healing loop
u_ai_worker.py      - Task execution with API integrations
u_ai_config.json    - API configuration
u_ai_memory.json    - Learning & error storage
logs/               - Error logs
uploads/            - Workflow files
assets/             - Generated outputs
  - generated/      - Images, audio, QR codes
  - stock/          - Downloaded images
```

## API Integration Rules

1. **Background Removal**: Uses birefnet API or falls back to local ComfyUI
2. **AI Council**: Multi-AI consensus with configurable timeout
3. **Image Generation**: 
   - ComfyUI for non-food items
   - Qwen API for food/drink items (per user preference)
4. **Image Download**: Pinterest first, web search fallback
5. **Audio Generation**: ComfyUI workflows
6. **QR Codes**: External API integration

## Error Handling

- All API calls have timeouts and fallbacks
- Errors are logged to `logs/error_YYYYMMDD_HHMMSS.log`
- Fixes are cached in `u_ai_memory.json`
- Self-healing loop applies cached fixes automatically

## License

MIT License - See LICENSE file

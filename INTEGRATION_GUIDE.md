# U-AI API Integration Guide

## Overview

U-AI is a unified platform that integrates multiple AI services:

1. **Background Removal** - Remove backgrounds from images
2. **AI Council** - Multi-AI consensus for better answers
3. **Image Generation** - ComfyUI + Qwen (for food items)
4. **Image Download** - Pinterest + web search
5. **Audio Generation** - ComfyUI workflows
6. **QR Code Generation** - External API

## Setup Instructions

### Step 1: Configure API Keys

Create a `.env` file in the project root:

```bash
# Background Removal API
BACKGROUND_REMOVAL_API_URL=https://api.birefnet.com/remove
BACKGROUND_REMOVAL_API_KEY=your_background_removal_key_here

# AI Council API
AI_COUNCIL_API_URL=https://api.aicouncil.com/v1/consensus
AI_COUNCIL_API_KEY=your_ai_council_key_here

# ComfyUI (local server)
COMFYUI_API_URL=http://localhost:8188
COMFYUI_API_KEY=  # Optional, leave empty for local auth

# Qwen API (for food items)
QWEN_API_URL=https://api.qwen.com/generate
QWEN_API_KEY=your_qwen_key_here

# Pinterest API
PINTEREST_API_URL=https://api.pinterest.com/v5/search
PINTEREST_API_KEY=your_pinterest_key_here
```

### Step 2: Environment Variables

Alternatively, set environment variables:

```bash
export BACKGROUND_REMOVAL_API_KEY="your_key"
export AI_COUNCIL_API_KEY="your_key"
export COMFYUI_API_URL="http://localhost:8188"
export QWEN_API_KEY="your_key"
export PINTEREST_API_KEY="your_key"
```

### Step 3: Install Dependencies

```bash
pip install google-genai requests urllib3 pillow
```

### Step 4: Start ComfyUI

```bash
# Start ComfyUI server
python -m comfyui.server --listen 0.0.0.0:8188
```

## Usage Examples

### 1. Remove Background

```python
from u_ai_worker import remove_background

# Remove background from uploaded image
result = remove_background(
    image_path="uploads/photo.jpg",
    api_key=os.getenv("BACKGROUND_REMOVAL_API_KEY")
)

# Result: "uploads/photo_nobg.png"
print(f"Background removed: {result}")
```

**Workflow:**
1. User uploads image or image appears in chat
2. User requests: "remove background"
3. System calls birefnet API
4. Returns processed image
5. Shows in app with download option

### 2. AI Council Consensus

```python
from u_ai_worker import ai_council_consensus

# Get consensus from multiple AIs
result = ai_council_consensus(
    topic="What is the best approach to climate change?",
    max_time_minutes=5,
    api_key=os.getenv("AI_COUNCIL_API_KEY")
)

# Result: Consensus answer from multiple AIs
print(f"AI Council result: {result}")
```

**Workflow:**
1. User asks question and says "use AI Council"
2. System sends topic to AI Council API
3. Multiple AIs discuss for max 5 minutes
4. Returns consensus answer
5. Shows result to user

### 3. Generate Image

```python
from u_ai_worker import generate_image

# Generate image using ComfyUI
result = generate_image(
    prompt="A beautiful sunset over mountains",
    width=512,
    height=512,
    api_key=os.getenv("COMFYUI_API_KEY")
)

# Result: "assets/generated/image_YYYYMMDD_HHMMSS.png"
print(f"Image generated: {result}")
```

**Special Case - Food Items:**
```python
# For food/drink items, use Qwen instead
from u_ai_worker import generate_image_with_qwen

food_result = generate_image_with_qwen(
    prompt="A delicious pizza",
    api_key=os.getenv("QWEN_API_KEY")
)
```

### 4. Download Image

```python
from u_ai_worker import download_image

# Download from Pinterest
result = download_image(
    query="ocean sunset",
    source="pinterest",
    api_key=os.getenv("PINTEREST_API_KEY")
)

# Result: "assets/stock/pinterest_ocean_sunset.jpg"
print(f"Image downloaded: {result}")
```

### 5. Generate Audio

```python
from u_ai_worker import generate_audio

# Generate music/audio
result = generate_audio(
    prompt="Peaceful ocean waves",
    category="Music",
    duration=180,
    api_key=os.getenv("COMFYUI_API_KEY")
)

# Result: "assets/generated/audio_YYYYMMDD_HHMMSS.mp3"
print(f"Audio generated: {result}")
```

### 6. Generate QR Code

```python
from u_ai_worker import generate_qr_code

# Generate QR code
result = generate_qr_code(
    text="https://example.com",
    api_url=os.getenv("QR_CODE_API_URL")
)

# Result: "assets/generated/qr_YYYYMMDD_HHMMSS.png"
print(f"QR code generated: {result}")
```

## API Integration Architecture

```
User Request
    ↓
U-AI Worker
    ↓
API Router
    ├─ Background Removal → birefnet API
    ├─ AI Council → Multi-AI consensus
    ├─ Image Gen → ComfyUI (non-food) / Qwen (food)
    ├─ Image Download → Pinterest / Web Search
    ├─ Audio Gen → ComfyUI workflows
    └─ QR Code → External API
    ↓
Result + Download Option
```

## Error Handling

All API calls include:

- **Timeout handling** - Prevents hanging requests
- **Fallback mechanisms** - Try alternative APIs
- **Error logging** - Logs to `logs/error_*.log`
- **Memory learning** - Stores fixes in `u_ai_memory.json`

Example error handling:

```python
try:
    result = generate_image(prompt, ...)
except TimeoutError:
    print("ComfyUI timeout, trying Qwen...")
    result = generate_image_with_qwen(prompt, ...)
except APIError as e:
    log_error(e)
    return None
```

## Mobile App Integration

For mobile apps (Android/iOS):

1. **Background Removal**: Show processed image in gallery
2. **Download**: Use native share/download APIs
3. **Audio**: Play or save to device storage
4. **QR Code**: Display in app or save to gallery

Example Android integration:

```kotlin
// Share generated image
val shareIntent = Intent(Intent.ACTION_SEND).apply {
    type = "image/*"
    putExtra(Intent.EXTRA_STREAM, uri)
}
startActivity(shareIntent)
```

## Testing

Run the test suite:

```bash
python test_integrations.py
```

## Monitoring

Check logs:

```bash
# View recent errors
tail -f logs/error_*.log

# Check memory
cat u_ai_memory.json
```

## Troubleshooting

### ComfyUI not responding

```bash
# Check if ComfyUI is running
curl http://localhost:8188/

# If not, start it
python -m comfyui.server --listen 0.0.0.0:8188
```

### API key missing

```bash
# Set environment variable
export BACKGROUND_REMOVAL_API_KEY="your_key"

# Or use config file
python -c "import json; config = json.load(open('u_ai_config.json')); print(config)"
```

### Qwen for food items

The system automatically detects food items and uses Qwen:

```python
# System auto-detects "pizza", "cake", "coffee" etc.
result = generate_image("delicious pizza")
# Automatically uses Qwen API
```

## Security Notes

- Never commit API keys to version control
- Use environment variables or secure config files
- Rotate keys regularly
- Use HTTPS for all API calls

## License

MIT License

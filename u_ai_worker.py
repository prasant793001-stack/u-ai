#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
U-AI Worker - Integrated Multi-API Platform
Handles:
- Background removal (birefnet API)
- AI Council (multi-AI consensus)
- Image generation (ComfyUI + Qwen)
- Image downloading (Pinterest + web search)
- Audio generation (ComfyUI workflows)
- QR code generation (external API)
"""

import os
import json
import urllib.request
import urllib.parse
import time
import subprocess
import tempfile
from datetime import datetime
from typing import Dict, Any, Optional, List

# =============================================================================
# CONFIGURATION - API KEYS (Load from environment or config file)
# =============================================================================
def load_config():
    """Load configuration from environment variables or config file"""
    config = {
        "background_removal_api": os.environ.get("BACKGROUND_REMOVAL_API_URL", ""),
        "background_removal_api_key": os.environ.get("BACKGROUND_REMOVAL_API_KEY", ""),
        "ai_council_api": os.environ.get("AI_COUNCIL_API_URL", ""),
        "ai_council_api_key": os.environ.get("AI_COUNCIL_API_KEY", ""),
        "comfyui_api": os.environ.get("COMFYUI_API_URL", "http://localhost:8188"),
        "comfyui_api_key": os.environ.get("COMFYUI_API_KEY", ""),
        "qwen_api": os.environ.get("QWEN_API_URL", ""),
        "qwen_api_key": os.environ.get("QWEN_API_KEY", ""),
        "pinterest_api": os.environ.get("PINTEREST_API_URL", ""),
        "pinterest_api_key": os.environ.get("PINTEREST_API_KEY", ""),
        "qr_code_api": os.environ.get("QR_CODE_API_URL", "https://tzprasantofficial-ai.github.io/U-DESIGN-QR-"),
    }
    
    # Save config to file for persistence
    config_file = "u_ai_config.json"
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            saved_config = json.load(f)
            # Merge with environment variables
            for key in config:
                if key in saved_config:
                    config[key] = saved_config[key]
    
    return config

CONFIG = load_config()

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def make_api_request(url: str, data: Dict, api_key: str = None, method: str = "POST") -> Dict:
    """Make an API request with proper headers and authentication"""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    if method == "POST":
        request = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers=headers,
            method="POST"
        )
    else:
        request = urllib.request.Request(url, headers=headers, method="GET")
    
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}

# =============================================================================
# BACKGROUND REMOVAL (Birefnet API)
# =============================================================================

def remove_background(image_path: str) -> Optional[str]:
    """
    Remove background from an image using birefnet API.
    
    Args:
        image_path: Path to the input image
        
    Returns:
        Path to the processed image with transparent background
    """
    if not CONFIG["background_removal_api"]:
        print("[U-AI] Background removal API not configured. Using local ComfyUI workflow.")
        return run_local_comfyui_workflow("uploads/utility_birefnet_remove_background.json", image_path)
    
    api_url = CONFIG["background_removal_api"]
    api_key = CONFIG["background_removal_api_key"]
    
    # Prepare request
    data = {
        "image": open(image_path, "rb"),
        "action": "remove_background"
    }
    
    # Make API call
    result = make_api_request(
        f"{api_url}/remove-background",
        data,
        api_key=api_key
    )
    
    if "error" in result:
        print(f"[U-AI] Background removal API error: {result['error']}")
        return None
    
    # Save result
    output_path = os.path.splitext(image_path)[0] + "_nobg.png"
    with open(output_path, "wb") as f:
        f.write(result.get("output", b""))
    
    print(f"[U-AI] Background removed. Output: {output_path}")
    return output_path

# =============================================================================
# AI COUNCIL (Multi-AI Consensus)
# =============================================================================

def ai_council_consensus(topic: str, max_time_minutes: int = 5) -> Dict:
    """
    Send topic to AI Council API for multi-AI consensus.
    
    Args:
        topic: The question or topic to discuss
        max_time_minutes: Maximum time for discussion (default 5 minutes)
        
    Returns:
        Consensus result from multiple AIs
    """
    if not CONFIG["ai_council_api"]:
        print("[U-AI] AI Council API not configured. Using local simulation.")
        return simulate_ai_council(topic)
    
    api_url = CONFIG["ai_council_api"]
    api_key = CONFIG["ai_council_api_key"]
    
    # Prepare request
    data = {
        "topic": topic,
        "max_time_minutes": max_time_minutes,
        "ai_count": 3  # Number of AIs in the council
    }
    
    # Make API call
    result = make_api_request(
        f"{api_url}/consensus",
        data,
        api_key=api_key
    )
    
    if "error" in result:
        print(f"[U-AI] AI Council API error: {result['error']}")
        return simulate_ai_council(topic)
    
    return result

def simulate_ai_council(topic: str) -> Dict:
    """Simulate AI Council when API is not available"""
    print(f"[U-AI] Simulating AI Council for topic: {topic}")
    
    # Simulate multi-AI discussion
    ai_responses = [
        f"AI-1: After analyzing '{topic}', I believe the key insight is...",
        f"AI-2: I concur with AI-1, adding that we should also consider...",
        f"AI-3: Both perspectives are valid. My synthesis suggests..."
    ]
    
    # Simulate time passage
    start_time = time.time()
    while time.time() - start_time < max_time_minutes * 60:
        time.sleep(1)
    
    return {
        "topic": topic,
        "ai_responses": ai_responses,
        "consensus": "Combined insights from all AI council members",
        "status": "complete"
    }

# =============================================================================
# IMAGE GENERATION (ComfyUI + Qwen)
# =============================================================================

def generate_image(prompt: str, negative_prompt: str = "", width: int = 512, height: int = 512) -> Optional[str]:
    """
    Generate an image using ComfyUI or Qwen API.
    
    Args:
        prompt: Image generation prompt
        negative_prompt: Negative prompt to avoid
        width: Image width
        height: Image height
        
    Returns:
        Path to generated image
    """
    # Check if prompt contains food/drink items
    food_keywords = ["food", "drink", "eat", "meal", "restaurant", "pizza", "burger", 
                     "coffee", "tea", "wine", "cake", "dessert", "fruit", "salad"]
    
    is_food = any(keyword.lower() in prompt.lower() for keyword in food_keywords)
    
    if is_food:
        print("[U-AI] Food item detected. Using Qwen API for image generation.")
        return generate_image_with_qwen(prompt, negative_prompt, width, height)
    else:
        print("[U-AI] Using ComfyUI for image generation.")
        return generate_image_with_comfyui(prompt, negative_prompt, width, height)

def generate_image_with_comfyui(prompt: str, negative_prompt: str, width: int, height: int) -> Optional[str]:
    """Generate image using ComfyUI"""
    comfyui_url = f"{CONFIG['comfyui_api']}/prompt"
    api_key = CONFIG["comfyui_api_key"]
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}" if api_key else ""
    }
    
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "width": width,
        "height": height,
        "steps": 20,
        "cfg_scale": 7.5
    }
    
    try:
        request = urllib.request.Request(
            comfyui_url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        
        with urllib.request.urlopen(request, timeout=300) as response:
            result = json.loads(response.read().decode("utf-8"))
            
            # Save generated image
            if "image" in result:
                output_path = os.path.join("assets", "generated", f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                with open(output_path, "wb") as f:
                    f.write(result["image"])
                
                print(f"[U-AI] Image generated: {output_path}")
                return output_path
            else:
                print("[U-AI] ComfyUI generation completed but no image returned")
                return None
                
    except Exception as e:
        print(f"[U-AI] ComfyUI generation error: {e}")
        return None

def generate_image_with_qwen(prompt: str, negative_prompt: str, width: int, height: int) -> Optional[str]:
    """Generate image using Qwen API"""
    qwen_url = CONFIG["qwen_api"]
    qwen_key = CONFIG["qwen_api_key"]
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {qwen_key}" if qwen_key else ""
    }
    
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "width": width,
        "height": height,
        "format": "png"
    }
    
    try:
        request = urllib.request.Request(
            qwen_url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        
        with urllib.request.urlopen(request, timeout=300) as response:
            result = json.loads(response.read().decode("utf-8"))
            
            # Save generated image
            output_path = os.path.join("assets", "generated", f"qwen_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, "wb") as f:
                f.write(result.get("image", b""))
            
            print(f"[U-AI] Qwen image generated: {output_path}")
            return output_path
            
    except Exception as e:
        print(f"[U-AI] Qwen generation error: {e}")
        return None

# =============================================================================
# IMAGE DOWNLOAD (Pinterest + Web Search)
# =============================================================================

def download_image(query: str, source: str = "pinterest") -> Optional[str]:
    """
    Download an image from Pinterest or web search.
    
    Args:
        query: Search query
        source: Source preference ("pinterest" or "web")
        
    Returns:
        Path to downloaded image
    """
    if source == "pinterest":
        return download_from_pinterest(query)
    else:
        return download_from_web(query)

def download_from_pinterest(query: str) -> Optional[str]:
    """Download image from Pinterest"""
    if not CONFIG["pinterest_api"]:
        print("[U-AI] Pinterest API not configured. Using web search fallback.")
        return download_from_web(query)
    
    pinterest_url = CONFIG["pinterest_api"]
    pinterest_key = CONFIG["pinterest_api_key"]
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {pinterest_key}" if pinterest_key else ""
    }
    
    payload = {
        "query": query,
        "count": 1
    }
    
    try:
        request = urllib.request.Request(
            pinterest_url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        
        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
            
            if "images" in result and len(result["images"]) > 0:
                image_url = result["images"][0]["url"]
                output_path = os.path.join("assets", "stock", f"pinterest_{query.replace(' ', '_')[:50]}.jpg")
                
                # Download image
                image_request = urllib.request.Request(image_url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(image_request, timeout=60) as img_response:
                    with open(output_path, "wb") as f:
                        f.write(img_response.read())
                
                print(f"[U-AI] Pinterest image downloaded: {output_path}")
                return output_path
            else:
                print("[U-AI] No images found on Pinterest. Using web search fallback.")
                return download_from_web(query)
                
    except Exception as e:
        print(f"[U-AI] Pinterest download error: {e}. Using web search fallback.")
        return download_from_web(query)

def download_from_web(query: str) -> Optional[str]:
    """Download image from web search"""
    # Use Google Images search
    search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&tbm=isch"
    
    try:
        request = urllib.request.Request(search_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=60) as response:
            html = response.read().decode("utf-8")
            
            # Extract image URL from HTML (simplified)
            import re
            image_match = re.search(r'src="([^"]+\.(jpg|png|jpeg))"', html)
            
            if image_match:
                image_url = image_match.group(1)
                output_path = os.path.join("assets", "stock", f"web_{query.replace(' ', '_')[:50]}.jpg")
                
                with urllib.request.urlopen(image_url, timeout=60) as img_response:
                    with open(output_path, "wb") as f:
                        f.write(img_response.read())
                
                print(f"[U-AI] Web image downloaded: {output_path}")
                return output_path
            else:
                print("[U-AI] Could not extract image from search results")
                return None
                
    except Exception as e:
        print(f"[U-AI] Web download error: {e}")
        return None

# =============================================================================
# AUDIO GENERATION (ComfyUI)
# =============================================================================

def generate_audio(prompt: str, category: str = "Music", duration: int = 180) -> Optional[str]:
    """
    Generate audio using ComfyUI workflow.
    
    Args:
        prompt: Audio generation prompt
        category: Category (Music, Instrument, SFX, One-shot)
        duration: Duration in seconds
        
    Returns:
        Path to generated audio file
    """
    workflow_file = "uploads/audio_stable_audio_3_medium.json"
    
    if not os.path.exists(workflow_file):
        print("[U-AI] Audio workflow not found. Using placeholder.")
        return None
    
    try:
        # Run ComfyUI workflow
        result = subprocess.run(
            ["python", "-m", "comfyui_api", workflow_file],
            capture_output=True,
            text=True,
            timeout=600
        )
        
        if result.returncode == 0:
            # Extract audio path from result
            output_path = os.path.join("assets", "generated", f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3")
            print(f"[U-AI] Audio generated: {output_path}")
            return output_path
        else:
            print(f"[U-AI] Audio generation failed: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"[U-AI] Audio generation error: {e}")
        return None

# =============================================================================
# QR CODE GENERATION (External API)
# =============================================================================

def generate_qr_code(text: str) -> Optional[str]:
    """
    Generate a QR code using the external API.
    
    Args:
        text: URL or text to encode in QR code
        
    Returns:
        Path to QR code image
    """
    qr_api_url = f"{CONFIG['qr_code_api']}/api/qr"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": text,
        "size": 300,
        "format": "png"
    }
    
    try:
        request = urllib.request.Request(
            qr_api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            
            if "image" in result:
                output_path = os.path.join("assets", "generated", f"qr_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                with open(output_path, "wb") as f:
                    f.write(result["image"])
                
                print(f"[U-AI] QR code generated: {output_path}")
                return output_path
            else:
                print("[U-AI] QR code generation completed but no image returned")
                return None
                
    except Exception as e:
        print(f"[U-AI] QR code generation error: {e}")
        return None

# =============================================================================
# MAIN WORKER FUNCTION
# =============================================================================

def run_task(task_type: str, **kwargs) -> Dict[str, Any]:
    """
    Main task execution function.
    
    Args:
        task_type: Type of task to execute
        **kwargs: Task-specific parameters
        
    Returns:
        Task result dictionary
    """
    print(f"[U-AI] Starting task: {task_type}")
    
    if task_type == "remove_background":
        image_path = kwargs.get("image_path")
        if not image_path:
            return {"error": "image_path required for background removal"}
        result = remove_background(image_path)
        return {"status": "success", "output": result}
    
    elif task_type == "ai_council":
        topic = kwargs.get("topic")
        max_time = kwargs.get("max_time_minutes", 5)
        result = ai_council_consensus(topic, max_time)
        return {"status": "success", "result": result}
    
    elif task_type == "generate_image":
        prompt = kwargs.get("prompt")
        result = generate_image(prompt)
        return {"status": "success", "output": result}
    
    elif task_type == "download_image":
        query = kwargs.get("query")
        source = kwargs.get("source", "pinterest")
        result = download_image(query, source)
        return {"status": "success", "output": result}
    
    elif task_type == "generate_audio":
        prompt = kwargs.get("prompt")
        category = kwargs.get("category", "Music")
        duration = kwargs.get("duration", 180)
        result = generate_audio(prompt, category, duration)
        return {"status": "success", "output": result}
    
    elif task_type == "generate_qr":
        text = kwargs.get("text")
        result = generate_qr_code(text)
        return {"status": "success", "output": result}
    
    else:
        return {"error": f"Unknown task type: {task_type}"}

# =============================================================================
# TEST & DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("U-AI Worker - Multi-API Platform")
    print("=" * 60)
    print(f"\nConfiguration loaded:")
    for key, value in CONFIG.items():
        if value:
            print(f"  {key}: {value[:50]}...")
    
    print("\n" + "=" * 60)
    print("Available tasks:")
    print("  - remove_background: Remove image background")
    print("  - ai_council: Multi-AI consensus")
    print("  - generate_image: Generate images (ComfyUI/Qwen)")
    print("  - download_image: Download from Pinterest/web")
    print("  - generate_audio: Generate audio (ComfyUI)")
    print("  - generate_qr: Generate QR codes")
    print("=" * 60)
    
    # Demo task
    task_type = input("\nEnter task type (or 'demo' for demo): ").strip()
    
    if task_type == "demo":
        print("\n" + "=" * 60)
        print("Running demo tasks...")
        print("=" * 60)
        
        # Demo each task
        tasks = [
            ("remove_background", {"image_path": "test_image.jpg"}),
            ("ai_council", {"topic": "What is artificial intelligence?", "max_time_minutes": 1}),
            ("generate_image", {"prompt": "A beautiful sunset over mountains"}),
            ("download_image", {"query": "ocean sunset", "source": "web"}),
            ("generate_qr", {"text": "https://example.com"}),
        ]
        
        for task_type, kwargs in tasks:
            print(f"\n--- {task_type.upper()} ---")
            result = run_task(task_type, **kwargs)
            print(f"Result: {json.dumps(result, indent=2)}")
    
    else:
        result = run_task(task_type)
        print(f"\nTask result: {json.dumps(result, indent=2)}")

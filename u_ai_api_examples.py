#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
U-AI API Integration Examples
Demonstrates how to use each API
"""

import os
import json
import requests
from datetime import datetime

# Load configuration
CONFIG_FILE = "u_ai_config.json"

def load_config():
    """Load API configuration"""
    if not os.path.exists(CONFIG_FILE):
        # Create default config
        config = {
            "background_removal_api": "",
            "background_removal_api_key": "",
            "ai_council_api": "",
            "ai_council_api_key": "",
            "comfyui_api": "http://localhost:8188",
            "comfyui_api_key": "",
            "qwen_api": "",
            "qwen_api_key": "",
            "pinterest_api": "",
            "pinterest_api_key": "",
            "qr_code_api": "https://tzprasantofficial-ai.github.io/U-DESIGN-QR-"
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
        return config
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def remove_background(image_path, api_key=None):
    """
    Remove background from an image using birefnet API
    
    Args:
        image_path: Path to the image file
        api_key: API key for the background removal service
    
    Returns:
        Path to the processed image
    """
    config = load_config()
    api_url = config.get("background_removal_api", "")
    
    if not api_url:
        # Fallback: use local ComfyUI workflow
        print("Using local ComfyUI for background removal")
        # Implementation would call ComfyUI API
        return image_path  # Placeholder
    
    # API call implementation
    # response = requests.post(api_url, files={"image": open(image_path, "rb")}, headers={"Authorization": f"Bearer {api_key}"})
    # return response.json()
    return image_path

def ai_council_consensus(topic, api_key=None):
    """
    Use AI Council to get consensus from multiple AI models
    
    Args:
        topic: The question or topic to discuss
        api_key: API key for the council service
    
    Returns:
        Consensus answer from multiple AIs
    """
    config = load_config()
    api_url = config.get("ai_council_api", "")
    
    if not api_url:
        print("AI Council API not configured")
        return "Please configure AI Council API key"
    
    # Implementation would call the council API
    # response = requests.post(api_url, json={"topic": topic, "timeout": 300}, headers={"Authorization": f"Bearer {api_key}"})
    # return response.json()
    return f"AI Council would discuss: {topic}"

def generate_image(prompt, use_comfyui=True, api_key=None):
    """
    Generate an image using ComfyUI or Qwen
    
    Args:
        prompt: Image generation prompt
        use_comfyui: Use ComfyUI (default True)
        api_key: API key
    
    Returns:
        Path to generated image
    """
    config = load_config()
    
    if use_comfyui:
        comfyui_url = config.get("comfyui_api", "http://localhost:8188")
        print(f"Using ComfyUI at {comfyui_url}")
        # Implementation would call ComfyUI API
        return "generated_image.png"
    else:
        # Use Qwen for non-food items
        print("Using Qwen for image generation")
        # Implementation would call Qwen API
        return "generated_image_qwen.png"

def download_image(query, use_pinterest=True, api_key=None):
    """
    Download images from Pinterest or web search
    
    Args:
        query: Search query
        use_pinterest: Use Pinterest (default True)
        api_key: API key
    
    Returns:
        Path to downloaded image
    """
    config = load_config()
    
    if use_pinterest:
        print(f"Searching Pinterest for: {query}")
        # Implementation would call Pinterest API
        return "downloaded_image.png"
    else:
        print(f"Web searching for: {query}")
        # Implementation would use web search
        return "downloaded_image_web.png"

def generate_audio(prompt, category="Music", api_key=None):
    """
    Generate audio using ComfyUI workflow
    
    Args:
        prompt: Audio generation prompt
        category: Music, Instrument, SFX, or One-shot
        api_key: API key
    
    Returns:
        Path to generated audio
    """
    config = load_config()
    workflow_file = "uploads/audio_stable_audio_3_medium.json"
    
    print(f"Generating audio: {prompt} ({category})")
    # Implementation would call ComfyUI API with workflow
    return "generated_audio.mp3"

def generate_qr_code(text, api_key=None):
    """
    Generate QR code using external API
    
    Args:
        text: URL or text to encode
        api_key: API key
    
    Returns:
        Path to QR code image
    """
    config = load_config()
    qr_api = config.get("qr_code_api", "https://tzprasantofficial-ai.github.io/U-DESIGN-QR-")
    
    print(f"Generating QR code for: {text}")
    # Implementation would call QR code API
    return "qr_code.png"

# Example usage
if __name__ == "__main__":
    print("U-AI API Integration Examples")
    print("=" * 50)
    
    # Example 1: Remove background
    print("\n1. Background Removal:")
    result = remove_background("uploads/photo.jpg")
    print(f"   Result: {result}")
    
    # Example 2: AI Council
    print("\n2. AI Council Consensus:")
    result = ai_council_consensus("What is the best way to learn Python?")
    print(f"   Result: {result}")
    
    # Example 3: Image Generation
    print("\n3. Image Generation:")
    result = generate_image("A beautiful sunset over mountains")
    print(f"   Result: {result}")
    
    # Example 4: Image Download
    print("\n4. Image Download:")
    result = download_image("neon city night rain")
    print(f"   Result: {result}")
    
    # Example 5: Audio Generation
    print("\n5. Audio Generation:")
    result = generate_audio("Soft piano music for meditation")
    print(f"   Result: {result}")
    
    # Example 6: QR Code
    print("\n6. QR Code Generation:")
    result = generate_qr_code("https://example.com")
    print(f"   Result: {result}")
    
    print("\n" + "=" * 50)
    print("All examples completed!")

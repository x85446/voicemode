"""Whisper model registry and utilities."""

import os
from pathlib import Path
from typing import Dict, List, Optional, TypedDict


class ModelInfo(TypedDict):
    """Information about a Whisper model."""
    size_mb: int  # Download size in MB
    languages: str  # Language support description
    description: str  # Brief description
    filename: str  # Expected filename when downloaded


# Registry of all available Whisper models
WHISPER_MODELS: Dict[str, ModelInfo] = {
    "tiny": {
        "size_mb": 39,
        "languages": "Multilingual",
        "description": "Fastest, least accurate",
        "filename": "ggml-tiny.bin"
    },
    "tiny.en": {
        "size_mb": 39,
        "languages": "English only",
        "description": "Fastest English model",
        "filename": "ggml-tiny.en.bin"
    },
    "base": {
        "size_mb": 142,
        "languages": "Multilingual",
        "description": "Good balance of speed and accuracy",
        "filename": "ggml-base.bin"
    },
    "base.en": {
        "size_mb": 142,
        "languages": "English only",
        "description": "Good English model",
        "filename": "ggml-base.en.bin"
    },
    "small": {
        "size_mb": 466,
        "languages": "Multilingual",
        "description": "Better accuracy, slower",
        "filename": "ggml-small.bin"
    },
    "small.en": {
        "size_mb": 466,
        "languages": "English only",
        "description": "Better English accuracy",
        "filename": "ggml-small.en.bin"
    },
    "medium": {
        "size_mb": 1500,
        "languages": "Multilingual",
        "description": "High accuracy, slow",
        "filename": "ggml-medium.bin"
    },
    "medium.en": {
        "size_mb": 1500,
        "languages": "English only",
        "description": "High English accuracy",
        "filename": "ggml-medium.en.bin"
    },
    "large-v1": {
        "size_mb": 2900,
        "languages": "Multilingual",
        "description": "Original large model",
        "filename": "ggml-large-v1.bin"
    },
    "large-v2": {
        "size_mb": 2900,
        "languages": "Multilingual",
        "description": "Improved large model (recommended)",
        "filename": "ggml-large-v2.bin"
    },
    "large-v3": {
        "size_mb": 3100,
        "languages": "Multilingual",
        "description": "Latest large model",
        "filename": "ggml-large-v3.bin"
    },
    "large-v3-turbo": {
        "size_mb": 1600,
        "languages": "Multilingual",
        "description": "Faster large model with good accuracy",
        "filename": "ggml-large-v3-turbo.bin"
    }
}


def get_model_directory() -> Path:
    """Get the directory where Whisper models are stored."""
    # Check environment variable first
    model_dir = os.getenv("VOICEMODE_WHISPER_MODEL_DIR")
    if model_dir:
        return Path(model_dir).expanduser()
    
    # Check if whisper.cpp is installed
    whisper_dir = os.getenv("VOICEMODE_WHISPER_DIR")
    if whisper_dir:
        return Path(whisper_dir).expanduser() / "models"
    
    # Default to ~/.voicemode/whisper.cpp/models
    return Path.home() / ".voicemode" / "whisper.cpp" / "models"


def get_current_model() -> str:
    """Get the currently selected Whisper model."""
    # Read from environment variable
    model = os.getenv("VOICEMODE_WHISPER_MODEL", "large-v2")
    
    # Validate it's a known model
    if model not in WHISPER_MODELS:
        return "large-v2"  # Default fallback
    
    return model


def is_model_installed(model_name: str) -> bool:
    """Check if a model is installed."""
    if model_name not in WHISPER_MODELS:
        return False
    
    model_dir = get_model_directory()
    model_info = WHISPER_MODELS[model_name]
    model_path = model_dir / model_info["filename"]
    
    return model_path.exists()


def get_installed_models() -> List[str]:
    """Get list of installed models."""
    installed = []
    for model_name in WHISPER_MODELS:
        if is_model_installed(model_name):
            installed.append(model_name)
    return installed


def get_total_size(models: Optional[List[str]] = None) -> int:
    """Get total size of models in MB.
    
    Args:
        models: List of model names. If None, uses all models.
    
    Returns:
        Total size in MB
    """
    if models is None:
        models = list(WHISPER_MODELS.keys())
    
    total = 0
    for model in models:
        if model in WHISPER_MODELS:
            total += WHISPER_MODELS[model]["size_mb"]
    
    return total


def format_size(size_mb: int) -> str:
    """Format size in MB to human-readable string."""
    if size_mb < 1000:
        return f"{size_mb} MB"
    else:
        size_gb = size_mb / 1000
        return f"{size_gb:.1f} GB"
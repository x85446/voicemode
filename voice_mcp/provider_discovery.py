"""
Provider discovery and registry management for voice-mcp.

This module handles automatic discovery of TTS/STT endpoints, including:
- Health checks
- Model discovery
- Voice discovery
- Dynamic registry management
"""

import asyncio
import logging
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

import httpx
from openai import AsyncOpenAI

from .config import TTS_BASE_URLS, STT_BASE_URLS, OPENAI_API_KEY

logger = logging.getLogger("voice-mcp")


@dataclass
class EndpointInfo:
    """Information about a discovered endpoint."""
    url: str
    healthy: bool
    models: List[str]
    voices: List[str]  # Only for TTS
    last_health_check: str  # ISO format timestamp
    response_time_ms: Optional[float] = None
    error: Optional[str] = None


class ProviderRegistry:
    """Manages discovery and selection of voice service providers."""
    
    def __init__(self):
        self.registry: Dict[str, Dict[str, EndpointInfo]] = {
            "tts": {},
            "stt": {}
        }
        self._discovery_lock = asyncio.Lock()
        self._initialized = False
    
    async def initialize(self):
        """Initialize the registry by discovering all configured endpoints."""
        if self._initialized:
            return
        
        async with self._discovery_lock:
            if self._initialized:  # Double-check after acquiring lock
                return
            
            logger.info("Initializing provider registry...")
            
            # Discover TTS endpoints
            await self._discover_endpoints("tts", TTS_BASE_URLS)
            
            # Discover STT endpoints
            await self._discover_endpoints("stt", STT_BASE_URLS)
            
            self._initialized = True
            logger.info(f"Provider registry initialized with {len(self.registry['tts'])} TTS and {len(self.registry['stt'])} STT endpoints")
    
    async def _discover_endpoints(self, service_type: str, base_urls: List[str]):
        """Discover all endpoints for a service type."""
        tasks = []
        for url in base_urls:
            if url not in self.registry[service_type]:
                tasks.append(self._discover_endpoint(service_type, url))
        
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for url, result in zip(base_urls, results):
                if isinstance(result, Exception):
                    logger.error(f"Failed to discover {service_type} endpoint {url}: {result}")
                    self.registry[service_type][url] = EndpointInfo(
                        url=url,
                        healthy=False,
                        models=[],
                        voices=[],
                        last_health_check=datetime.utcnow().isoformat() + "Z",
                        error=str(result)
                    )
    
    async def _discover_endpoint(self, service_type: str, base_url: str) -> None:
        """Discover capabilities of a single endpoint."""
        logger.debug(f"Discovering {service_type} endpoint: {base_url}")
        start_time = time.time()
        
        try:
            # Create OpenAI client for the endpoint
            client = AsyncOpenAI(
                api_key=OPENAI_API_KEY or "dummy-key-for-local",
                base_url=base_url,
                timeout=10.0
            )
            
            # Try to list models
            models = []
            try:
                model_response = await client.models.list()
                models = [model.id for model in model_response.data]
                logger.debug(f"Found models at {base_url}: {models}")
            except Exception as e:
                logger.debug(f"Could not list models at {base_url}: {e}")
                # Not all endpoints support /v1/models, that's OK
            
            # For TTS, discover voices
            voices = []
            if service_type == "tts":
                voices = await self._discover_voices(base_url, client)
                logger.debug(f"Found voices at {base_url}: {voices}")
            
            # Calculate response time
            response_time = (time.time() - start_time) * 1000
            
            # Store endpoint info
            self.registry[service_type][base_url] = EndpointInfo(
                url=base_url,
                healthy=True,
                models=models,
                voices=voices,
                last_health_check=datetime.utcnow().isoformat() + "Z",
                response_time_ms=response_time
            )
            
            logger.info(f"Successfully discovered {service_type} endpoint {base_url} with {len(models)} models and {len(voices)} voices")
            
        except Exception as e:
            logger.warning(f"Endpoint {base_url} discovery failed: {e}")
            self.registry[service_type][base_url] = EndpointInfo(
                url=base_url,
                healthy=False,
                models=[],
                voices=[],
                last_health_check=datetime.utcnow().isoformat() + "Z",
                error=str(e)
            )
    
    async def _discover_voices(self, base_url: str, client: AsyncOpenAI) -> List[str]:
        """Discover available voices for a TTS endpoint."""
        # If it's OpenAI, use known voices
        if "openai.com" in base_url:
            return ["alloy", "echo", "fable", "nova", "onyx", "shimmer"]
        
        # Try Kokoro-style voices endpoint
        try:
            # Use httpx directly for non-standard endpoint
            async with httpx.AsyncClient(timeout=5.0) as http_client:
                response = await http_client.get(f"{base_url}/audio/voices")
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, dict) and "voices" in data:
                        return data["voices"]
                    elif isinstance(data, list):
                        return data
        except Exception as e:
            logger.debug(f"Could not fetch voices from {base_url}/audio/voices: {e}")
        
        # If we can't determine voices but the endpoint is healthy, assume OpenAI voices
        # This allows compatibility with OpenAI-compatible APIs that don't expose voices
        return ["alloy", "echo", "fable", "nova", "onyx", "shimmer"]
    
    async def check_health(self, service_type: str, base_url: str) -> bool:
        """Check the health of a specific endpoint and update registry."""
        logger.debug(f"Health check for {service_type} endpoint: {base_url}")
        
        # Re-discover the endpoint
        await self._discover_endpoint(service_type, base_url)
        
        # Return health status
        endpoint_info = self.registry[service_type].get(base_url)
        return endpoint_info.healthy if endpoint_info else False
    
    def get_healthy_endpoints(self, service_type: str) -> List[EndpointInfo]:
        """Get all healthy endpoints for a service type."""
        endpoints = []
        
        # Return endpoints in the order they were configured
        base_urls = TTS_BASE_URLS if service_type == "tts" else STT_BASE_URLS
        
        for url in base_urls:
            info = self.registry[service_type].get(url)
            if info and info.healthy:
                endpoints.append(info)
        
        return endpoints
    
    def find_endpoint_with_voice(self, voice: str) -> Optional[EndpointInfo]:
        """Find the first healthy TTS endpoint that supports a specific voice."""
        for endpoint in self.get_healthy_endpoints("tts"):
            if voice in endpoint.voices:
                return endpoint
        return None
    
    def find_endpoint_with_model(self, service_type: str, model: str) -> Optional[EndpointInfo]:
        """Find the first healthy endpoint that supports a specific model."""
        for endpoint in self.get_healthy_endpoints(service_type):
            if model in endpoint.models:
                return endpoint
        return None
    
    def get_registry_for_llm(self) -> Dict[str, Any]:
        """Get registry data formatted for LLM inspection."""
        return {
            "tts": {
                url: {
                    "healthy": info.healthy,
                    "models": info.models,
                    "voices": info.voices,
                    "response_time_ms": info.response_time_ms,
                    "last_check": info.last_health_check,
                    "error": info.error
                }
                for url, info in self.registry["tts"].items()
            },
            "stt": {
                url: {
                    "healthy": info.healthy,
                    "models": info.models,
                    "response_time_ms": info.response_time_ms,
                    "last_check": info.last_health_check,
                    "error": info.error
                }
                for url, info in self.registry["stt"].items()
            }
        }
    
    async def mark_unhealthy(self, service_type: str, base_url: str, error: str):
        """Mark an endpoint as unhealthy after a failure."""
        if base_url in self.registry[service_type]:
            self.registry[service_type][base_url].healthy = False
            self.registry[service_type][base_url].error = error
            self.registry[service_type][base_url].last_health_check = datetime.utcnow().isoformat() + "Z"
            logger.warning(f"Marked {service_type} endpoint {base_url} as unhealthy: {error}")


# Global registry instance
provider_registry = ProviderRegistry()
"""
Utility functions for CryptoFund agents.
"""
import json
import logging
import time
import asyncio
from typing import Any, Dict, Optional, Callable
import requests
from uagents import Context

from .config import Config
from .errors import APIError, async_retry

logger = logging.getLogger(__name__)


def load_json_file(file_path: str) -> dict:
    """
    Load JSON data from a file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Parsed JSON data as a dictionary
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"JSON file not found: {file_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_path}: {e}")
        raise


def save_json_file(file_path: str, data: dict) -> None:
    """
    Save dictionary data to a JSON file.
    
    Args:
        file_path: Path to the JSON file
        data: Dictionary to save
        
    Raises:
        PermissionError: If writing to the file fails
    """
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    except PermissionError:
        logger.error(f"Permission denied when writing to {file_path}")
        raise
    except Exception as e:
        logger.error(f"Error saving JSON to {file_path}: {e}")
        raise


def make_api_request(url: str, 
                     method: str = "GET", 
                     headers: Optional[Dict[str, str]] = None,
                     params: Optional[Dict[str, Any]] = None,
                     data: Optional[Dict[str, Any]] = None,
                     timeout: Optional[int] = None) -> Dict[str, Any]:
    """
    Make an API request with proper error handling and timeouts.
    
    Args:
        url: API endpoint URL
        method: HTTP method (GET, POST, etc.)
        headers: Request headers
        params: URL parameters
        data: Request body data
        timeout: Request timeout in seconds
        
    Returns:
        JSON response as a dictionary
        
    Raises:
        APIError: If the request fails or returns an error status
    """
    timeout = timeout or Config.API_TIMEOUT
    
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=data,
            timeout=timeout
        )
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        raise APIError(f"API request failed: {e}")


class AsyncEventHandler:
    """Helper class for managing asynchronous events and timeouts."""
    
    def __init__(self, timeout: float = 30.0):
        """
        Initialize the event handler.
        
        Args:
            timeout: Default timeout in seconds
        """
        self.timeout = timeout
        self._events = {}
        
    def create_event(self, event_id: str) -> asyncio.Event:
        """
        Create a new event.
        
        Args:
            event_id: Unique identifier for the event
            
        Returns:
            An asyncio Event object
        """
        event = asyncio.Event()
        self._events[event_id] = event
        return event
    
    def set_event(self, event_id: str) -> None:
        """
        Set an event, indicating it has occurred.
        
        Args:
            event_id: Identifier of the event to set
        """
        if event_id in self._events:
            self._events[event_id].set()
    
    async def wait_for_event(self, event_id: str, timeout: Optional[float] = None) -> bool:
        """
        Wait for an event to be set.
        
        Args:
            event_id: Identifier of the event to wait for
            timeout: How long to wait in seconds
            
        Returns:
            True if the event was set, False if timeout occurred
        """
        timeout = timeout or self.timeout
        if event_id not in self._events:
            self._events[event_id] = asyncio.Event()
            
        try:
            await asyncio.wait_for(self._events[event_id].wait(), timeout)
            return True
        except asyncio.TimeoutError:
            logger.warning(f"Timeout waiting for event {event_id}")
            return False
    
    def clear_event(self, event_id: str) -> None:
        """
        Clear an event so it can be waited for again.
        
        Args:
            event_id: Identifier of the event to clear
        """
        if event_id in self._events:
            self._events[event_id].clear()
    
    def clear_all_events(self) -> None:
        """Clear all events."""
        for event in self._events.values():
            event.clear()


@async_retry()
async def send_message_with_retry(ctx: Context, 
                                 target_address: str, 
                                 message: Any,
                                 event_handler: Optional[AsyncEventHandler] = None,
                                 event_id: Optional[str] = None,
                                 timeout: Optional[float] = None) -> bool:
    """
    Send a message to another agent with retries and wait for response.
    
    Args:
        ctx: Agent context
        target_address: Address of the target agent
        message: Message to send
        event_handler: Optional event handler for response tracking
        event_id: Optional event ID for tracking the response
        timeout: How long to wait for a response
        
    Returns:
        True if message was sent and response received, False otherwise
    """
    try:
        await ctx.send(target_address, message)
        
        if event_handler and event_id:
            # If event handler and event ID are provided, wait for response
            return await event_handler.wait_for_event(event_id, timeout)
        
        return True
        
    except Exception as e:
        logger.error(f"Error sending message to {target_address}: {e}")
        return False 
"""
Error handling utilities for CryptoFund agents.
"""
import logging
import time
import functools
import asyncio
from typing import Callable, Any, TypeVar, Optional

from .config import Config

logger = logging.getLogger(__name__)

T = TypeVar('T')


class AgentError(Exception):
    """Base exception for all agent-related errors."""
    pass


class CommunicationError(AgentError):
    """Error in agent-to-agent communication."""
    pass


class APIError(AgentError):
    """Error during API calls."""
    pass


class TransactionError(AgentError):
    """Error during blockchain transactions."""
    pass


def retry(max_retries: Optional[int] = None, 
          delay: Optional[float] = None,
          exceptions: tuple = (Exception,)):
    """
    Retry decorator for synchronous functions.
    
    Args:
        max_retries: Maximum number of retries, defaults to Config.MAX_RETRIES
        delay: Delay between retries in seconds, defaults to Config.RETRY_DELAY
        exceptions: Tuple of exceptions to catch and retry
        
    Returns:
        Decorated function
    """
    max_retries = max_retries or Config.MAX_RETRIES
    delay = delay or Config.RETRY_DELAY
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    logger.warning(
                        f"Retry {attempt+1}/{max_retries} for {func.__name__} "
                        f"due to {e.__class__.__name__}: {e}"
                    )
                    if attempt < max_retries - 1:
                        time.sleep(delay)
            
            logger.error(f"Failed after {max_retries} retries: {last_exception}")
            raise last_exception
            
        return wrapper
    return decorator


def async_retry(max_retries: Optional[int] = None, 
                delay: Optional[float] = None,
                exceptions: tuple = (Exception,)):
    """
    Retry decorator for asynchronous functions.
    
    Args:
        max_retries: Maximum number of retries, defaults to Config.MAX_RETRIES
        delay: Delay between retries in seconds, defaults to Config.RETRY_DELAY
        exceptions: Tuple of exceptions to catch and retry
        
    Returns:
        Decorated async function
    """
    max_retries = max_retries or Config.MAX_RETRIES
    delay = delay or Config.RETRY_DELAY
    
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    logger.warning(
                        f"Async retry {attempt+1}/{max_retries} for {func.__name__} "
                        f"due to {e.__class__.__name__}: {e}"
                    )
                    if attempt < max_retries - 1:
                        await asyncio.sleep(delay)
            
            logger.error(f"Failed after {max_retries} async retries: {last_exception}")
            raise last_exception
            
        return wrapper
    return decorator


def safe_execute(default_value: Any = None):
    """
    Decorator for safely executing functions with proper error handling.
    
    Args:
        default_value: Value to return if function fails
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {e}")
                return default_value
                
        return wrapper
    return decorator 
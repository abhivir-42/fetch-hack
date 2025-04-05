"""
Service registry for agent discovery and management.
"""
import logging
import json
import os
from typing import Dict, Optional, List, Any
import requests

from .config import Config
from .errors import APIError, retry

logger = logging.getLogger(__name__)


class ServiceRegistry:
    """
    Service registry for agent discovery and management.
    Centralizes agent addresses and provides discovery functionality.
    """
    
    def __init__(self, registry_file: Optional[str] = None):
        """
        Initialize the service registry.
        
        Args:
            registry_file: Path to the registry JSON file
        """
        self._registry_file = registry_file or os.path.join(
            os.path.dirname(__file__), "..", "data", "agent_registry.json"
        )
        self._registry = self._load_registry()
    
    def _load_registry(self) -> Dict[str, str]:
        """
        Load the registry from file.
        
        Returns:
            Dictionary mapping agent names to addresses
        """
        try:
            with open(self._registry_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If file doesn't exist or is invalid, start with hardcoded values
            return Config.AGENT_ADDRESSES
    
    def _save_registry(self) -> None:
        """Save the registry to file."""
        os.makedirs(os.path.dirname(self._registry_file), exist_ok=True)
        
        with open(self._registry_file, 'w') as f:
            json.dump(self._registry, f, indent=2)
    
    def get_agent_address(self, agent_name: str) -> Optional[str]:
        """
        Get an agent address by name.
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            Agent address if found, None otherwise
        """
        return self._registry.get(agent_name.upper())
    
    def register_agent(self, agent_name: str, address: str) -> None:
        """
        Register an agent.
        
        Args:
            agent_name: Name of the agent
            address: Agent address
        """
        self._registry[agent_name.upper()] = address
        self._save_registry()
        logger.info(f"Registered agent {agent_name} with address {address}")
    
    def unregister_agent(self, agent_name: str) -> None:
        """
        Unregister an agent.
        
        Args:
            agent_name: Name of the agent
        """
        if agent_name.upper() in self._registry:
            del self._registry[agent_name.upper()]
            self._save_registry()
            logger.info(f"Unregistered agent {agent_name}")
    
    def list_registered_agents(self) -> Dict[str, str]:
        """
        List all registered agents.
        
        Returns:
            Dictionary mapping agent names to addresses
        """
        return dict(self._registry)
    
    @retry(max_retries=3, delay=2)
    def discover_agents_by_tag(self, tag: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Discover agents by tag using the Agentverse API.
        
        Args:
            tag: Tag to search for
            limit: Maximum number of agents to return
            
        Returns:
            List of agent information dictionaries
            
        Raises:
            APIError: If the API request fails
        """
        api_url = "https://agentverse.ai/v1/search/agents"
        
        payload = {
            "search_text": f"tag:{tag}",
            "sort": "relevancy",
            "direction": "asc",
            "offset": 0,
            "limit": limit,
        }
        
        try:
            response = requests.post(api_url, json=payload)
            response.raise_for_status()
            
            data = response.json()
            return data.get("agents", [])
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Agent discovery failed: {e}")
            raise APIError(f"Agent discovery failed: {e}")
    
    def register_discovered_agents(self, agents: List[Dict[str, Any]]) -> None:
        """
        Register agents discovered from the Agentverse API.
        
        Args:
            agents: List of agent information dictionaries from discover_agents_by_tag
        """
        for agent in agents:
            agent_name = agent.get("name", "").upper().replace(" ", "_")
            agent_address = agent.get("address")
            
            if agent_name and agent_address:
                self.register_agent(agent_name, agent_address)


# Singleton instance
registry = ServiceRegistry() 
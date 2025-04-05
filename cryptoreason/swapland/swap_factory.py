"""
Factory for creating swap execution agents for different blockchains and token pairs.
"""
import logging
import os
from enum import Enum
from typing import Dict, Any, Optional, Tuple
from web3 import Web3

from cryptoreason.common.errors import TransactionError, retry

logger = logging.getLogger(__name__)


class SwapDirection(Enum):
    """Enum for swap directions."""
    ETH_TO_USDC = "eth_to_usdc"
    USDC_TO_ETH = "usdc_to_eth"


class BlockchainNetwork(Enum):
    """Enum for supported blockchain networks."""
    BASE = "base"
    ETHEREUM = "ethereum"
    POLYGON = "polygon"


class SwapAgent:
    """
    Base class for swap execution agents.
    Handles token swaps on various blockchain networks.
    """
    
    # Contract addresses for each network and token
    CONTRACT_ADDRESSES = {
        BlockchainNetwork.BASE.value: {
            "router": "0x4752ba5DBc23F9092F8A6635BB749a7e26f84bEF",
            "usdc": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
        },
        BlockchainNetwork.ETHEREUM.value: {
            "router": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
            "usdc": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
        },
        BlockchainNetwork.POLYGON.value: {
            "router": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
            "usdc": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
        }
    }
    
    # RPC endpoints for each network
    RPC_ENDPOINTS = {
        BlockchainNetwork.BASE.value: "https://mainnet.base.org",
        BlockchainNetwork.ETHEREUM.value: "https://mainnet.infura.io/v3/your-infura-key",
        BlockchainNetwork.POLYGON.value: "https://polygon-rpc.com"
    }
    
    def __init__(self, 
                network: str, 
                direction: str, 
                private_key: str,
                amount: float):
        """
        Initialize the swap agent.
        
        Args:
            network: Blockchain network (e.g., "base", "ethereum")
            direction: Swap direction (e.g., "eth_to_usdc", "usdc_to_eth")
            private_key: Private key for transaction signing
            amount: Amount to swap
        """
        self.network = network
        self.direction = direction
        self.private_key = private_key
        self.amount = amount
        
        # Validate inputs
        self._validate_inputs()
        
        # Set up web3 connection
        self.web3 = Web3(Web3.HTTPProvider(self.RPC_ENDPOINTS[self.network]))
        
        # Set up account from private key
        self.account = self.web3.eth.account.privateKeyToAccount(private_key)
        
        # Load contract addresses
        self.contract_addresses = self.CONTRACT_ADDRESSES[self.network]
    
    def _validate_inputs(self) -> None:
        """
        Validate initialization inputs.
        
        Raises:
            ValueError: If any input is invalid
        """
        if self.network not in self.RPC_ENDPOINTS:
            raise ValueError(f"Unsupported network: {self.network}")
        
        if self.direction not in [d.value for d in SwapDirection]:
            raise ValueError(f"Unsupported swap direction: {self.direction}")
        
        if not self.private_key or not self.private_key.startswith("0x"):
            raise ValueError("Invalid private key format")
        
        if self.amount <= 0:
            raise ValueError(f"Invalid amount: {self.amount}")
    
    def get_token_balance(self, token_address: str, address: Optional[str] = None) -> int:
        """
        Get token balance for an address.
        
        Args:
            token_address: Token contract address
            address: Address to check balance for, defaults to account address
            
        Returns:
            Token balance as integer
        """
        address = address or self.account.address
        
        # ERC20 ABI for balanceOf function
        abi = [
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function"
            }
        ]
        
        # Create contract instance
        token_contract = self.web3.eth.contract(address=token_address, abi=abi)
        
        # Call balanceOf function
        return token_contract.functions.balanceOf(address).call()
    
    def get_eth_balance(self, address: Optional[str] = None) -> int:
        """
        Get ETH balance for an address.
        
        Args:
            address: Address to check balance for, defaults to account address
            
        Returns:
            ETH balance in wei
        """
        address = address or self.account.address
        return self.web3.eth.getBalance(address)
    
    @retry(max_retries=3, delay=5)
    def execute_swap(self) -> Dict[str, Any]:
        """
        Execute the token swap.
        
        Returns:
            Dictionary with transaction details
            
        Raises:
            TransactionError: If the swap fails
        """
        try:
            if self.direction == SwapDirection.ETH_TO_USDC.value:
                return self._swap_eth_to_usdc()
            elif self.direction == SwapDirection.USDC_TO_ETH.value:
                return self._swap_usdc_to_eth()
            else:
                raise ValueError(f"Unsupported swap direction: {self.direction}")
        
        except Exception as e:
            logger.error(f"Swap execution failed: {e}")
            raise TransactionError(f"Swap execution failed: {e}")
    
    def _swap_eth_to_usdc(self) -> Dict[str, Any]:
        """
        Swap ETH to USDC.
        
        Returns:
            Dictionary with transaction details
        """
        # Implementation details for ETH to USDC swap
        # Would include contract interaction, transaction signing, and sending
        logger.info(f"Swapping {self.amount} ETH to USDC on {self.network}")
        
        # Example implementation (simplified)
        tx_hash = "0x" + "0" * 64  # Placeholder for actual transaction
        
        return {
            "status": "success",
            "tx_hash": tx_hash,
            "from_amount": self.amount,
            "from_token": "ETH",
            "to_token": "USDC",
            "network": self.network
        }
    
    def _swap_usdc_to_eth(self) -> Dict[str, Any]:
        """
        Swap USDC to ETH.
        
        Returns:
            Dictionary with transaction details
        """
        # Implementation details for USDC to ETH swap
        # Would include contract interaction, transaction signing, and sending
        logger.info(f"Swapping {self.amount} USDC to ETH on {self.network}")
        
        # Example implementation (simplified)
        tx_hash = "0x" + "0" * 64  # Placeholder for actual transaction
        
        return {
            "status": "success",
            "tx_hash": tx_hash,
            "from_amount": self.amount,
            "from_token": "USDC",
            "to_token": "ETH",
            "network": self.network
        }


class SwapAgentFactory:
    """Factory for creating swap agents."""
    
    @staticmethod
    def create_swap_agent(network: str, 
                         signal: str, 
                         amount: float, 
                         private_key: str) -> SwapAgent:
        """
        Create a swap agent based on network and signal.
        
        Args:
            network: Blockchain network (e.g., "base", "ethereum")
            signal: Swap signal ("buy" or "sell")
            amount: Amount to swap
            private_key: Private key for transaction signing
            
        Returns:
            Configured SwapAgent instance
            
        Raises:
            ValueError: If parameters are invalid
        """
        # Convert signal to swap direction
        direction = SwapAgentFactory._signal_to_direction(signal)
        
        # Validate network
        if network not in [n.value for n in BlockchainNetwork]:
            raise ValueError(f"Unsupported network: {network}")
        
        # Create and return swap agent
        return SwapAgent(network, direction, private_key, amount)
    
    @staticmethod
    def _signal_to_direction(signal: str) -> str:
        """
        Convert buy/sell signal to swap direction.
        
        Args:
            signal: "buy" or "sell"
            
        Returns:
            SwapDirection value
            
        Raises:
            ValueError: If signal is invalid
        """
        signal = signal.lower()
        
        if signal == "buy":
            return SwapDirection.ETH_TO_USDC.value
        elif signal == "sell":
            return SwapDirection.USDC_TO_ETH.value
        else:
            raise ValueError(f"Invalid signal: {signal}")


# Example usage
if __name__ == "__main__":
    # Example parameters
    network = "base"
    signal = "buy"
    amount = 0.1
    private_key = "0x" + "0" * 64  # Replace with actual private key
    
    try:
        # Create swap agent
        agent = SwapAgentFactory.create_swap_agent(network, signal, amount, private_key)
        
        # Execute swap
        result = agent.execute_swap()
        print(f"Swap result: {result}")
        
    except Exception as e:
        print(f"Error: {e}") 
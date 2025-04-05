"""
Configuration management for CryptoFund agents.
"""
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class Config:
    """Centralized configuration management for all agents."""
    
    # API Keys
    ASI1_API_KEY = os.getenv("ASI1_API_KEY")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    CMC_API_KEY = os.getenv("CMC_API_KEY")
    AGENTVERSE_API_KEY = os.getenv("AGENTVERSE_API_KEY")
    
    # Wallet Configuration
    METAMASK_PRIVATE_KEY = os.getenv("METAMASK_PRIVATE_KEY")
    
    # Network Constants
    ONETESTFET = 1000000000000000000  # 1 FET in atestfet
    REWARD = 2000000000000000000  # Expected reward amount
    DENOM = "atestfet"
    
    # Default settings
    DEFAULT_NETWORK = "base"
    DEFAULT_RISK_PROFILE = "moderate"
    DEFAULT_INVESTOR_TYPE = "balanced"
    
    # Agent addresses - will be moved to service registry in future
    AGENT_ADDRESSES = {
        "HEARTBEAT_AGENT": "agent1q0jnt3skqqrpj3ktu23ljy3yx5uvp7lgz2cdku3vdrslh2w8kw7vvstpv73",
        "COIN_AGENT": "agent1qw6cxgq4l8hmnjctm43q97vajrytuwjc2e2n4ncdfpqk6ggxcfmxuwdc9rq",
        "FGI_AGENT": "agent1qgzh245lxeaapd32mxlwgdf2607fkt075hymp06rceknjnc2ylznwdv8up7",
        "REASON_AGENT": "agent1qwlg48h8sstknk7enc2q44227ahq6dr5mjg0p7z62ca6tfueze38kyrtyl2",
        "CRYPTONEWS_AGENT": "agent1q2cq0q3cnhccudx6cym8smvpquafsd99lrwexppuecfrnv90xlrs5lsxw6k",
        "SWAPLAND_AGENT": "agent1q0jnt3skqqrpj3ktu23ljy3yx5uvp7lgz2cdku3vdrslh2w8kw7vvstpv73",
        "TOPUP_AGENT": "agent1q02xdwqwthtv6yeawrpcgpyvh8a002ueeynnltu8n6gxq0hlh8qu7ep5uhu",
        "REWARD_AGENT": "agent1qde8udnttat2mmq3srkrz60wm3248yg43528wy2guwyewtesd73z7x3swru"
    }
    
    # Retry configuration
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds
    
    # Timeouts
    DEFAULT_TIMEOUT = 10  # seconds
    API_TIMEOUT = 30  # seconds
    
    @classmethod
    def get_agent_address(cls, agent_name):
        """Get agent address by name with proper error handling."""
        try:
            return cls.AGENT_ADDRESSES[agent_name]
        except KeyError:
            logger.error(f"Unknown agent name: {agent_name}")
            return None 
import os
import logging
import asyncio
from dotenv import load_dotenv, set_key, find_dotenv
from uagents import Bureau

# Import agents - Ensure these imports work based on your project structure
from src.simulation_manager_agent import simulation_manager_agent
from src.market_data_agent import market_data_agent
from src.sentiment_agent import sentiment_agent

# Configure Logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

async def update_env_with_addresses(agents):
    """Updates the .env file with the addresses of the provided agents."""
    dotenv_path = find_dotenv()
    if not dotenv_path:
        logger.warning("Could not find .env file. Agent addresses will not be saved.")
        # Create one if it doesn't exist?
        # with open(".env", "w") as f:
        #     pass
        # dotenv_path = find_dotenv()
        # if not dotenv_path:
        #     logger.error("Failed to create .env file.")
        #     return
        return # Don't proceed if .env not found

    logger.info(f"Updating agent addresses in: {dotenv_path}")
    try:
        for agent_instance in agents:
            # Use await agent_instance.address if it's an async property, otherwise use it directly
            # Assuming agent.address is a simple property here based on common uagents usage
            address = agent_instance.address
            if agent_instance.name == "MarketDataAgent":
                set_key(dotenv_path, "MARKET_DATA_AGENT_ADDRESS", address)
                logger.info(f"MARKET_DATA_AGENT_ADDRESS set to {address}")
            elif agent_instance.name == "SentimentAgent":
                set_key(dotenv_path, "SENTIMENT_AGENT_ADDRESS", address)
                logger.info(f"SENTIMENT_AGENT_ADDRESS set to {address}")
            # Add elif for other agents if needed later

        # Reload dotenv to make sure the current process sees the changes
        load_dotenv(override=True)

    except Exception as e:
        logger.error(f"Failed to update .env file with agent addresses: {e}")

async def main():
    # List of agents to run in this bureau
    agents_to_run = [simulation_manager_agent, market_data_agent, sentiment_agent]

    # Create a Bureau to run agents concurrently
    bureau = Bureau()

    logger.info("Adding agents to bureau...")
    for agent_instance in agents_to_run:
        logger.info(f"- Adding {agent_instance.name} (Seed: {agent_instance.seed})")
        bureau.add(agent_instance)

    # Update .env file with the addresses *before* running the bureau
    # The addresses are determined once the Agent object is initialized
    await update_env_with_addresses(agents_to_run)

    logger.info("Starting bureau...")
    try:
        await bureau.run()
    except Exception as e:
        logger.error(f"Bureau run failed: {e}")
        # Perform any cleanup if necessary
    finally:
        logger.info("Bureau stopped.")

if __name__ == "__main__":
    logger.info("--- Starting Layer 1 --- ")
    load_dotenv() # Load initial .env if exists
    asyncio.run(main()) 
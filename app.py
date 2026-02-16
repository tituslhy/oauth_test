import chainlit as cl
import logging

from src.on_chat_start import setup_agent
from src.on_message import invoke_agent

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s"
)
logger = logging.getLogger(__name__)

@cl.oauth_callback
async def oauth_callback(
    provider_id: str,
    token: str,
    raw_user_data: dict,
    default_user: cl.User,
):
    email = raw_user_data.get("email")

    if not email.endswith("@gmail.com"): #ideally this should be "@your_company_domain.com"
        return None  # Reject user

    return default_user

#%%
@cl.on_chat_start
async def on_chat_start():
    setup_agent()
    logger.info("Agent setup complete")

@cl.on_message
async def on_message(message: cl.Message):
    # Invoke agent
    response = await invoke_agent(message=message)
    logger.info(f"Agent Response: {response}")
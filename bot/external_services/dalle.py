import asyncio
import os
from openai import OpenAI
from bot.config_data.config import load_config
config = load_config()


async def create_image(prompt: str):
    client = OpenAI(api_key=config.open_ai.api_key, organization=config.open_ai.organization_id)
    response = client.images.generate(
      model="dall-e-3",
      style="vivid", #natural
      prompt=f"{prompt}",
      size="1024x1024",
      quality="standard",
      n=1,
    )
    image_url = response.data[0].url
    return image_url
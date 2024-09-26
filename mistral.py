from aiohttp import ClientSession
import asyncio
import json
import requests
from mistralai import Mistral

api_key = 'X8ahOMkLJytSfLPPuEkPDg8CMSqFOWiE'
model = "mistral-large-latest"

client = Mistral(api_key=api_key)


async def chat_ai(text):
    return await client.chat.stream_async(
        model=model,
        messages=[
            {
                "role": "user",
                "content": text,
            },
        ]
    )


import discord
from discord.ext import commands
import aiohttp
import os
from dotenv import load_dotenv

class AICommandBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

        # Create an aiohttp session for HTTP requests
        self.session = aiohttp.ClientSession()

        # Load or set default configuration
        self.ai_url = os.getenv("AI_ENDPOINT_URL", "http://placeholder.ai:5001/v1/chat/completions")
        self.system_prompt = os.getenv("AI_SYSTEM_PROMPT", "You are Shibebot, an AI made for the Thunderdoge gaming community.")

    async def setup_hook(self):
        # Load cogs or extensions here if you have any
        pass

    async def close(self):
        await super().close()
        await self.session.close()

    async def fetch_ai_response(self, user_content: str):
        payload = {
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.7,
            "max_tokens": 150,
            "stream": False
        }
        async with self.session.post(self.ai_url, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('choices', [{}])[0].get('message', {}).get('content', 'Error: Could not parse AI response.')
            return 'Error: Failed to fetch response from AI.'

# Entry point to run the bot
if __name__ == "__main__":
    load_dotenv() # Load environment variables from .env file

    # Start the bot
    bot = AICommandBot()
    bot.run(os.getenv('DISCORD_TOKEN'))

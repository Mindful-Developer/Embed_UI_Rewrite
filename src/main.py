import os
from disnake.ext import commands
from config import get_config
from dotenv import load_dotenv
from database.setup_db import setup_db

load_dotenv()
setup_db()


if __name__ == '__main__':
    client = commands.InteractionBot(**get_config())
    client.load_extensions('cogs')
    client.run(os.environ.get('DISCORD_TOKEN'))

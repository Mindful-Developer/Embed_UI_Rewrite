import os
from disnake.ext import commands
from config import get_config


token = os.environ.get('DISCORD_TOKEN')


if __name__ == '__main__':
    client = commands.InteractionBot(**get_config())
    client.load_extensions('cogs')
    client.run(token)

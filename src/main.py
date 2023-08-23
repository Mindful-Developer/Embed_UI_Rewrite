import os
import disnake as ds
from disnake.ext import commands
from dotenv import load_dotenv


load_dotenv()

dev_mode = int(os.environ.get('DEV_MODE'))
token = os.environ.get('DISCORD_TOKEN')
test_guilds = list(map(int, os.environ.get('TEST_GUILDS').split(',')))

intents = ds.Intents.default()
intents.members = True

test_config = {
    "intents": intents,
    "test_guilds": test_guilds,
    "command_sync_flags": commands.CommandSyncFlags(
        allow_command_deletion=True,
        sync_commands=True,
        sync_commands_debug=True,
        sync_global_commands=True,
        sync_guild_commands=True,
        sync_on_cog_actions=True,
    ),
    "enable_debug_events": True,
    "reload": True,
}

production_config = {
    "intents": intents,
}

config = test_config if dev_mode else production_config


if __name__ == '__main__':
    client = commands.InteractionBot(**config)
    client.load_extensions('cogs')
    client.run(token)

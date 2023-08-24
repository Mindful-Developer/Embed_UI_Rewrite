import os
import disnake as ds
from disnake.ext import commands
from dotenv import load_dotenv


load_dotenv()


def get_config():
    dev_mode = int(os.environ.get('DEV_MODE') or 0)
    test_guilds = list(map(int, (os.environ.get('TEST_GUILDS') or "").split(',')))

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

    return test_config if dev_mode else production_config

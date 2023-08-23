from disnake.ext.commands import Cog
import time
from utils.register import register_cog
from database.models import Guild, orm


@register_cog
class Connection(Cog):
    def __init__(self, client):
        self.client = client
        self.down_timer = 0

    @Cog.listener()
    async def on_connect(self):
        print('Logging in...')

    @Cog.listener()
    async def on_ready(self):
        print('------------------------')
        print('Logged in as: ' + self.client.user.name)
        print(self.client.slash_commands)
        print('Ready')

    @Cog.listener()
    async def on_disconnect(self):
        self.down_timer = time.perf_counter()
        print('Disconnected')
        print('Attempting reconnection......')

    @Cog.listener()
    async def on_resumed(self):
        self.down_timer = time.perf_counter() - self.down_timer
        print(f'Connection has been restored in {self.down_timer} seconds')

    @orm.db_session
    @Cog.listener()
    async def on_guild_join(self, guild):
        Guild(id=guild.id)

    @orm.db_session
    @Cog.listener()
    async def on_guild_remove(self, guild):
        Guild[guild.id].delete()


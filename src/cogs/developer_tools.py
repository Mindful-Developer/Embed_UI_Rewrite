from disnake.ext.commands import Cog, slash_command, command
from disnake import ApplicationCommandInteraction
from utils.enums import Cogs
from utils.register import register_cog


@register_cog
class DeveloperTools(Cog):
    def __init__(self, client):
        self.client = client

    async def cog_slash_command_check(self, inter: ApplicationCommandInteraction):
        """Only allow the owner of the bot to use the commands in this cog"""
        if inter.author.id == self.client.owner_id:
            return True
        else:
            await inter.response.send_message('You do not have permission to use this command.', ephemeral=True)
            return False

    @command(name="shutdown", description="Shutdown the bot.")
    async def shutdown(self, ctx):
        """Shutdown the bot"""
        await ctx.send('Shutting down...')
        await self.client.close()

    @slash_command(name='ping', description='Check the latency of the bot.')
    async def ping(self, inter: ApplicationCommandInteraction):
        """Pings the bot returning response delay"""
        await inter.response.send_message(f'Statbot responded in {round(self.client.latency * 1000)}ms', ephemeral=True)

    @slash_command(name='servers', description='Displays the bot server count.')
    async def servers(self, inter: ApplicationCommandInteraction):
        """Counts the number of servers the bot is in"""
        await inter.response.send_message(f'I am in {len(self.client.guilds)} servers', ephemeral=True)

    @slash_command(name='load', description='Loads a cog.')
    async def load(self, inter: ApplicationCommandInteraction, cog: Cogs):
        """Loads a cog"""
        try:
            self.client.load_extension(cog)
            await inter.response.send_message(f'Loaded {cog}', ephemeral=True)
        except Exception as e:
            await inter.response.send_message(f'Error loading {cog}: {e}', ephemeral=True)

    @slash_command(name='unload', description='Unloads a cog.')
    async def unload(self, inter: ApplicationCommandInteraction, cog: Cogs):
        """Unloads a cog"""
        if cog != 'cogs.utility':
            try:
                self.client.unload_extension(cog)
                await inter.response.send_message(f'Unloaded {cog}', ephemeral=True)
            except Exception as e:
                await inter.response.send_message(f'Error unloading {cog}: {e}', ephemeral=True)
        else:
            await inter.response.send_message('Cannot unload utility, reload instead', ephemeral=True)

    @slash_command(name='reload', description='Reloads a cog.')
    async def reload(self, inter: ApplicationCommandInteraction, cog: Cogs):
        """Reloads a cog"""
        if cog != 'cogs.utility':
            try:
                self.client.unload_extension(cog)
                self.client.load_extension(cog)
                await inter.response.send_message(f'Reloaded {cog}', ephemeral=True)
            except Exception as e:
                await inter.response.send_message(f'Error reloading {cog}: {e}', ephemeral=True)
        else:
            util2 = DeveloperToolsHelper(self.client)
            await util2.reload_developer_tools(inter)

    @slash_command(name='reloadall', description='Reloads all cogs.')
    async def reloadall(self, inter: ApplicationCommandInteraction):
        """Reloads all cogs"""
        for extension in self.client.extensions.copy():
            if extension != 'cogs.utility':
                try:
                    self.client.unload_extension(extension)
                    self.client.load_extension(extension)
                except Exception as e:
                    await inter.response.send_message(f'Error reloading {extension}: {e}', ephemeral=True)

        util2 = DeveloperToolsHelper(self.client)
        await util2.reload_developer_tools(inter, all_cogs=True)


# This class is used to reload the DeveloperTools cog because it needs a different class to reload itself
class DeveloperToolsHelper:
    def __init__(self, client):
        self.client = client

    async def reload_developer_tools(self, inter: ApplicationCommandInteraction, all_cogs=False):
        try:
            self.client.unload_extension('cogs.dev')
            self.client.load_extension('cogs.dev')
            if all_cogs:
                await inter.response.send_message('Reloaded all cogs', ephemeral=True)
            else:
                await inter.response.send_message('Reloaded utility', ephemeral=True)
        except Exception as e:
            await inter.response.send_message(f'Error reloading cogs.utility: {e}', ephemeral=True)

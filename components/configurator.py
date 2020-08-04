from core.base_classes.command import Command
from core.base_classes.component import Component
from core.utils import discord_logger


class Configurator(Component):

    def __init__(self, client, name, prefix, description='default component', enabled=True):
        super().__init__(client, name, prefix, description, enabled, icon=':gear:')
        self.commands = [set_prefix('prefix', 'Set the bots prefix to a new character', client)]


class set_prefix(Command):
    def __init__(self, cmd, desc, client):
        super().__init__(cmd, desc, client)

    async def run(self, args, message):
        if len(args) == 0:
            await message.channel.send('`A new prefix has to be supplied, for example: !prefix .`')
        else:
            self.client.data_mapper_servers.set_specific_server_data(message.guild, "server_prefix", args[0])
            discord_logger.log("Changed server prefix for server: " + str(message.guild.id), 'red')
            await message.channel.send('`New prefix set`')

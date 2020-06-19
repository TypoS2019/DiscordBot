from core import discord_logger
from core.command import Command
from core.component import Component


class Configurator(Component):

    def __init__(self, client, name, prefix, description='default component', enabled=True):
        super().__init__(client, name, prefix, description, enabled)
        self.commands = [SayHi('hi', 'Say hello', )]

    async def run(self, args, message):
        await message.channel.send('hello')


class SayHi(Command):
    def __init__(self, cmd, desc):
        super().__init__(cmd, desc)

    def run(self, args, message):
        message.channel.send('helloiiii')

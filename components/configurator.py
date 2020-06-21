from core.base_classes.command import Command
from core.base_classes.component import Component


class Configurator(Component):

    def __init__(self, client, name, prefix, description='default component', enabled=True):
        super().__init__(client, name, prefix, description, enabled)
        self.commands = [SayHi('hi', 'Say hello', client)]

    async def run(self, args, message):
        await message.channel.send('hello')


class SayHi(Command):
    def __init__(self, cmd, desc, client):
        super().__init__(cmd, desc, client)

    def run(self, args, message):
        message.channel.send('helloiiii')

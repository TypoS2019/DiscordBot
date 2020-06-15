from core.component import Component


class Configurator(Component):

    def __init__(self, name, prefix, description='default component', enabled=True):
        super().__init__(name, prefix, description, enabled)

    async def run(self, args, message):
        await message.channel.send('hello')
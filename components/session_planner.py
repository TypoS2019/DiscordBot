from core.base_classes.command import Command
from core.base_classes.component import Component
from core.utils import discord_logger


class GameSessions(Component):

    def __init__(self, client, name, prefix, description='default component', enabled=True):
        super().__init__(client, name, prefix, description, enabled, icon=':gear:')
        self.commands = [plan_session('session', 'Plan a session on your server', client)]


class plan_session(Command):
    def __init__(self, cmd, desc, client):
        super().__init__(cmd, desc, client)

    async def run(self, args, message):
        if len(args) == 0:
            await message.channel.send('`Please provide an activity for this session')
        else:
            print(args.index('activity'))
            print(args[args.index('activity')])

import asyncio
import datetime

import discord

from core import discord_logger
from core.command import Command
from core.component import Component


class TimeMessager(Component):
    def __init__(self, client, name, prefix, description='default component', enabled=True):
        super().__init__(client, name, prefix, description, enabled)
        self.commands = [set_channel('here!', ''), unset_channel('bye!',''), get_channel('where?','')]

    def extended_setup(self, client):
        discord_logger.log(self.name + ": starting background process", 'blue')
        client.loop.create_task(self.background_task(client))
        discord_logger.log(self.name + ": started background process", 'blue')

    async def background_task(self, client):
        await client.wait_until_ready()
        last_occurrence_hour = 0
        last_occurrence_minute = 0
        while not client.is_closed():
            time = datetime.datetime.now()
            if time.hour == time.minute and last_occurrence_minute != time.minute and last_occurrence_hour != time.hour:
                discord_logger.log('occurrence: [' + str(time.hour) + ':' + str(time.minute) + ']', 'red')
                for channel in client.get_all_channels():
                    if isinstance(channel, discord.TextChannel):
                        await channel.send(str(time.hour) + ':' + str(time.minute))
                last_occurrence_minute = time.minute
                last_occurrence_hour = time.hour
            await asyncio.sleep(1)


class set_channel(Command):
    def __init__(self, cmd, desc):
        super().__init__(cmd, desc)

    def run(self, args, message):
        message.channel.send('helloiiii')


class unset_channel(Command):
    def __init__(self, cmd, desc):
        super().__init__(cmd, desc)

    def run(self, args, message):
        message.channel.send('helloiiii')


class get_channel(Command):
    def __init__(self, cmd, desc):
        super().__init__(cmd, desc)

    def run(self, args, message):
        message.channel.send('helloiiii')

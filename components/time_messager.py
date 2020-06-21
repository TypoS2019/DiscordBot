import asyncio
import datetime

from core.utils import discord_logger
from core.base_classes.command import Command
from core.base_classes.component import Component


class TimeMessager(Component):
    def __init__(self, client, name, prefix, description='default component', enabled=True):
        super().__init__(client, name, prefix, description, enabled)
        self.commands = [set_channel('here!', '', client), unset_channel('bye!', '', client),
                         get_channel('where?', '', client)]

    def extended_setup(self, client):
        discord_logger.log(self.name + ": starting background process", 'blue')
        client.loop.create_task(self.background_task(client))
        discord_logger.log(self.name + ": started background process", 'blue')

    async def background_task(self, client):
        await client.wait_until_ready()
        last_occurrence_hour = None
        last_occurrence_minute = None
        while not client.is_closed():
            time = datetime.datetime.now()
            if time.hour == time.minute and last_occurrence_minute != time.minute and last_occurrence_hour != time.hour:
                channels = self.client.data_mapper_servers.get_all_specific_server_data("server_kid_channel")
                string = str(time.hour) + ':' + str(time.minute)
                if time.hour < 10 and time.minute < 10:
                    string = '0' + str(time.hour) + ':0' + str(time.minute)
                discord_logger.log('occurrence: [' + string + ']', 'red')
                for channel_id in channels:
                    channel = self.client.get_channel(channel_id['server_kid_channel'])
                    await channel.send(string)
                last_occurrence_minute = time.minute
                last_occurrence_hour = time.hour
            await asyncio.sleep(1)

    async def default_run(self, message):
        time = datetime.datetime.now()
        string = str(time.hour) + ':' + str(time.minute)
        if time.hour < 10 and time.minute < 10:
            string = '0' + str(time.hour) + ':0' + str(time.minute)
        if message.content == string:
            doc = {"member_id": message.author.id,
                   "occurrence": string,
                   "date": time}
            self.client.data_mapper_members.insert_doc(doc)


class set_channel(Command):
    def __init__(self, cmd, desc, client):
        super().__init__(cmd, desc, client)

    async def run(self, args, message):
        self.client.data_mapper_servers.set_specific_server_data(message.guild, "server_kid_channel", message.channel.id)
        await message.channel.send('displaying here!')


class unset_channel(Command):
    def __init__(self, cmd, desc, client):
        super().__init__(cmd, desc, client)

    async def run(self, args, message):
        self.client.data_mapper_servers.set_specific_server_data(message.guild, "server_kid_channel", None)
        await message.channel.send('Not displaying anymore!')


class get_channel(Command):
    def __init__(self, cmd, desc, client):
        super().__init__(cmd, desc, client)

    async def run(self, args, message):
        channel_id = self.client.data_mapper.get_specific_server_data(message.guild, "server_kid_channel")
        if self.client.get_channel(channel_id['server_kid_channel']) is not None:
            await message.channel.send(self.client.get_channel(channel_id['server_kid_channel']).name)
        else:
            await message.channel.send("kid not active yet")

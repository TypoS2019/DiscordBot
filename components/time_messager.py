import asyncio
import datetime
from time import strftime

import discord
import emoji

from core.utils import discord_logger
from core.base_classes.command import Command
from core.base_classes.component import Component


class TimeMessager(Component):
    def __init__(self, client, name, prefix, description='default component', enabled=True):
        super().__init__(client, name, prefix, description, enabled)
        self.commands = [set_channel('here!', 'Display time messages in this channel', client),
                         unset_channel('bye!', 'Stop displaying time messages in this server', client),
                         get_channel('where?', 'Show the channel where time messages are displayed in this server',
                                     client),
                         calc_all_streaks_local('leaderboard',
                                                'Show the leaderboard for the longest streaks in this server', client),
                         calc_all_streaks_global('leaderboard_global',
                                                 'Show the leaderboard for the longest streaks of all time', client)]

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
                channels = self.client.data_mapper_servers.get_all_specific_data("server_kid_channel")
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
            member = self.client.data_mapper_members.collection.find_one(
                {"member_id": message.author.id, "server_id": message.guild.id})
            if member is None:
                doc = {"member_id": message.author.id,
                       "occurrences": [],
                       "server_id": message.guild.id
                       }
                self.client.data_mapper_members.insert_doc(doc)

            self.client.data_mapper_members.collection.update(
                {"member_id": message.author.id, "server_id": message.guild.id},
                {
                    "$push": {
                        "occurrences": {
                            "occurrence": string,
                            "date": time,
                        }
                    }
                }
            )
            await message.add_reaction(emoji.emojize(":thumbs_up:"))


class set_channel(Command):
    def __init__(self, cmd, desc, client):
        super().__init__(cmd, desc, client)

    async def run(self, args, message):
        self.client.data_mapper_servers.set_specific_server_data(message.guild, "server_kid_channel",
                                                                 message.channel.id)
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
        channel_id = self.client.data_mapper_servers.get_specific_server_data(message.guild, "server_kid_channel")
        if self.client.get_channel(channel_id['server_kid_channel']) is not None:
            await message.channel.send(self.client.get_channel(channel_id['server_kid_channel']).name)
        else:
            await message.channel.send("kid not active yet")


class calc_all_streaks_local(Command):
    def __init__(self, cmd, desc, client):
        super().__init__(cmd, desc, client)

    async def run(self, args, message):
        data = self.client.data_mapper_members.get_server_data(message.guild).sort("date")
        streaks = calc_streaks(data)
        embed = discord.Embed()
        for idx, streak in enumerate(sorted(streaks, key=lambda x: x['streak'], reverse=True)):
            try:
                user = await self.client.fetch_user(streak['member_id'])
                name = user.name + "#" + user.discriminator
            except discord.errors.NotFound:
                name = 'Unknown user'
            embed.add_field(name=str(idx + 1) + '. streak: ' + str(streak['streak']),
                            value=name, inline=False)
            if idx > 9:
                break
        embed.title = 'Local leaderboard'
        embed.description = 'The top 10 highest streaks of this server. Get consecutive correct time message approved by the bot and earn your spot! '
        embed.set_footer(
            text='A time message has to be in the hh:mm format, for example: 23:23. When the bot adds a ' + emoji.emojize(
                self.client.approved) + ' reaction to your message it will be counted for your streaks!')
        await message.channel.send(embed=embed)


class calc_all_streaks_global(Command):
    def __init__(self, cmd, desc, client):
        super().__init__(cmd, desc, client)

    async def run(self, args, message):
        data = self.client.data_mapper_members.get_data().sort("date")
        streaks = calc_streaks(data)
        embed = discord.Embed()
        for idx, streak in enumerate(sorted(streaks, key=lambda x: x['streak'], reverse=True)):
            try:
                user = await self.client.fetch_user(streak['member_id'])
                name = user.name + "#" + user.discriminator
            except discord.errors.NotFound:
                name = 'Unknown user'
            embed.add_field(name=str(idx + 1) + '. streak: ' + str(streak['streak']),
                            value=name, inline=False)
            if idx > 9:
                break
        embed.title = 'Global leaderboard'
        embed.description = 'The top 10 highest streaks of all time in any server. Get consecutive correct time message approved by the bot and earn your spot! '
        embed.set_footer(
            text='A time message has to be in the hh:mm format, for example: 23:23. When the bot adds a ' + emoji.emojize(
                self.client.approved) + ' reaction to your message it will be counted for your streaks! for the global streak messages can be in different channels and servers')
        await message.channel.send(embed=embed)


def calc_streaks(data):
    streaks = []
    for member in data:
        highest = 0
        streak = 1
        last_date = None
        last_occurrence = None
        for log in member['occurrences']:
            if last_date is not None:
                if (log['date'] - last_date) < datetime.timedelta(hours=1, minutes=5) and log['occurrence'] != last_occurrence:
                    streak += 1
                else:
                    streak = 1
                print(str(member['member_id']) + ":" + str(streak))
            if streak > highest:
                highest = streak
            last_date = log['date']
            last_occurrence = log['occurrence']
        streaks.append({'member_id': member['member_id'], 'streak': highest})
    return streaks


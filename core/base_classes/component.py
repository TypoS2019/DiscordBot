import discord

from core.utils import discord_logger
from core.utils.Enums import permissions


class Component:
    def __init__(self, client, name, prefix, description='default component', enabled=True, icon=':cd:', security=permissions.Member):
        self.client = client
        self.name = name
        self.icon = icon
        self.prefix = prefix
        self.description = description
        self.enabled = enabled
        self.commands = []
        self.security = security

    async def run(self, args, message, sec_lvl):
        if len(args) == 0:
            await self.default_command(message)
            return
        cmd = args[0]
        for command in self.commands:
            if command.cmd == cmd:
                if command.check_permission(sec_lvl):
                    args.pop(0)
                    await command.run(args, message)
                else:
                    await message.channel.send('`Permission denied`')
                break

    def setup(self, client):
        discord_logger.log("initializing " + self.name, 'blue')
        self.extended_setup(client)
        for command in self.commands:
            discord_logger.log("collected command (cmd: " + self.prefix + ' ' + command.cmd + ")", 'blue')

    def extended_setup(self, client):
        pass

    async def get_help_menu(self, menu_id):
        embed = discord.Embed()
        embed.title = self.name
        embed.description = '```component prefix: ' + self.prefix + '```'
        embed.colour = discord.Colour.from_rgb(252, 3, 127)
        embed.set_footer(text=menu_id)
        embed = self.set_help_menu_fields(embed)
        return embed

    def set_help_menu_fields(self, embed):
        if len(self.commands) > 0:
            for idx, command in enumerate(self.commands):
                embed.add_field(name='`' + command.cmd + '`', value=command.desc, inline=False)
        else:
            embed.add_field(name='This is where i would put my commands,', value='If i had any...')
        return embed

    async def default_run(self, message):
        pass

    async def default_command(self, message):
        await message.channel.send('`Please supply a valid command`')

    def check_permission(self, permission_no):
        return self.security.int() >= permission_no.int()
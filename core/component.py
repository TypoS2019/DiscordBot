import discord

from core import discord_logger


class Component:
    def __init__(self, client, name, prefix, description='default component', enabled=True):
        self.client = client
        self.name = name
        self.prefix = prefix
        self.description = description
        self.enabled = enabled
        self.commands = []

    async def run(self, args, message):
        for command in self.commands:
            if command.cmd == args[0]:
                args.pop(0)
                command.run(args, message)

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
        embed.colour = discord.Colour.from_rgb(252, 3, 127)
        embed.set_footer(text=menu_id)
        embed = self.set_help_menu_fields(embed)
        return embed

    def set_help_menu_fields(self, embed):
        if len(self.commands) > 0:
            for idx, command in enumerate(self.commands):
                embed.add_field(name=str(idx) + '. command: `' + command.cmd + '`', value=command.desc)
        else:
            embed.add_field(name='This is where i would put my commands,', value='If i had any...')
        return embed

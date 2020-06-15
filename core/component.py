import discord


class Component:
    def __init__(self, name, prefix, description='default component', enabled=True):
        self.name = name
        self.prefix = prefix
        self.description = description
        self.enabled = enabled

    async def run(self, args, message):
        print('no actions have been implemented yet')

    async def get_help_menu(self, menu_id):
        embed = discord.Embed()
        embed.title = self.name
        embed.colour = discord.Colour.from_rgb(252, 3, 127)
        embed.set_footer(text=menu_id)
        embed = self.set_help_menu_fields(embed)
        return embed

    def set_help_menu_fields(self, embed):
        embed.add_field(name='This is where i would put my help menu items', value='If i had any...')
        return embed

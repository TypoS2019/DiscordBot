import discord
import emoji


class Menu():
    def __init__(self, items, menu_id, menu_up, menu_down, menu_select, menu_back):
        self.components = items
        self.menu_id = menu_id
        self.menu_up = menu_up
        self.menu_down = menu_down
        self.menu_select = menu_select
        self.menu_back = menu_back

    async def send_menu(self, args, message):
        message = await message.channel.send(embed=self.create_menu())
        await self.add_navigation_root_reactions(message)

    async def add_navigation_root_reactions(self, message):
        await message.clear_reactions()
        await message.add_reaction(emoji.emojize(self.menu_up))
        await message.add_reaction(emoji.emojize(self.menu_down))
        await message.add_reaction(emoji.emojize(self.menu_select))

    async def update_menu(self, message, cmd):
        if isinstance(cmd, str):
            cmd = emoji.demojize(cmd)
            if cmd in [self.menu_up, self.menu_down, self.menu_select]:
                index = 1
                for idx, field in enumerate(message.embeds[0].fields):
                    if '**__' in field.name:
                        index = idx
                if cmd == self.menu_up:
                    index -= 1
                elif cmd == self.menu_down:
                    index += 1
                if cmd == self.menu_select:
                    await message.clear_reactions()
                    await message.edit(embed=await self.components[index].get_help_menu(self.menu_id))
                    await message.add_reaction(emoji.emojize(self.menu_back))
                else:
                    await message.edit(embed=self.create_menu(index=index))
            elif cmd == self.menu_back:
                await message.edit(embed=self.create_menu())
                await self.add_navigation_root_reactions(message)

    def create_menu(self, index=0):
        embed = discord.Embed()
        embed.title = 'help_menu_v0.3b'
        embed.colour = discord.Colour.from_rgb(252, 3, 127)
        self.set_menu_fields(embed, index)
        embed.set_footer(text=self.menu_id)
        return embed

    def set_menu_fields(self, embed, index=0):
        if len(self.components) < index + 1:
            index = len(self.components) - 1
        if index < 0:
            index = 0
        selected = self.components[index].name
        for component in self.components:
            name = component.name
            desc = component.description
            if not component.enabled:
                name = '~~' + name + '~~'
                desc = '~~' + desc + '~~'
            elif selected == name:
                name = '**__' + name + '__**'
                desc = '**__' + desc + '__**'
            embed.add_field(name=name, value=desc, inline=False)

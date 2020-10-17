import discord
import emoji

from core.utils.Enums import reaction


class Menu():
    def __init__(self, items, menu_id):
        self.components = items
        self.menu_id = menu_id
        self.menu_up = reaction.MENU_UP
        self.menu_down = reaction.MENU_DOWN
        self.menu_select = reaction.MENU_SELECT
        self.menu_back = reaction.MENU_BACK

    async def send_menu(self, args, message):
        message = await message.channel.send(embed=self.create_menu())
        await self.add_navigation_root_reactions(message)

    async def add_navigation_root_reactions(self, message):
        await message.clear_reactions()
        await message.add_reaction(emoji.emojize(self.menu_up.value))
        await message.add_reaction(emoji.emojize(self.menu_down.value))
        await message.add_reaction(emoji.emojize(self.menu_select.value))

    async def update_menu(self, message, cmd):
        if isinstance(cmd, str):
            cmd = emoji.demojize(cmd)
            if cmd in [self.menu_up.value, self.menu_down.value, self.menu_select.value]:
                index = 1
                for idx, field in enumerate(message.embeds[0].fields):
                    if '**__' in field.name:
                        index = idx
                if cmd == self.menu_up.value:
                    index -= 1
                elif cmd == self.menu_down.value:
                    index += 1
                if cmd == self.menu_select.value:
                    await message.clear_reactions()
                    await message.edit(embed=await self.components[index].get_help_menu(self.menu_id))
                    await message.add_reaction(emoji.emojize(self.menu_back.value))
                else:
                    await message.edit(embed=self.create_menu(index=index))
            elif cmd == self.menu_back.value:
                await message.edit(embed=self.create_menu())
                await self.add_navigation_root_reactions(message)

    def create_menu(self, index=0):
        embed = discord.Embed()
        embed.title = 'Component menu'
        embed.description = 'Displays the available components. Navigate using the reactions'
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
            desc = '`' + desc + '`'

            if not component.enabled:
                name = '~~' + name + '~~'
                desc = '~~' + desc + '~~'
            elif selected == name:
                name = '**__' + name + '__**'
                desc = '**__' + desc + '__**'
            name = emoji.emojize(component.icon) + ' ' + name
            embed.add_field(name=name, value=desc, inline=False)

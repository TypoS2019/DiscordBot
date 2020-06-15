import configparser
import emoji

import discord

from components.configurator import Configurator
from core.help_menu import Menu


class HackerBot(discord.Client):

    def __init__(self, **options):
        super().__init__(**options)
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.prefix = config.get('GlobalSettings', 'default_prefix')

        self.menu_id = config.get('MenuSettings', 'menu_id')
        self.menu_up = config.get('MenuSettings', 'menu_up_indicator')
        self.menu_down = config.get('MenuSettings', 'menu_down_indicator')
        self.menu_select = config.get('MenuSettings', 'menu_select_indicator')
        self.menu_back = config.get('MenuSettings', 'menu_back_indicator')


        self.components = []
        self.prefixes = []

        self.add_component(Configurator('Config1', 'Config1', ))
        self.add_component(Configurator('Config2', 'Config2', ))
        self.add_component(Configurator('Config3', 'Configs1', ))

        self.add_component(Configurator('Configurator', 'config', 'Edit settings and behavior'))

        self.menu = Menu(self.components, self.menu_id, self.menu_up, self.menu_down, self.menu_select, self.menu_back)

    async def router(self, args, message):
        print(args)
        if args[0] == '':
            await message.channel.send('Invalid Command')
            return
        if args[0] == 'menu':
            await self.menu.send_menu(args, message)
        for component in self.components:
            if args[0] == component.prefix:
                await component.run(args, message)

    async def on_ready(self):
        print('ready')

    async def on_message(self, message):
        if message.content.startswith(self.prefix):
            args = message.content[len(self.prefix):]
            await self.router(args.split(' '), message)

    async def on_reaction_add(self, reaction, user):
        if user.id != self.user.id:
            if reaction.message.embeds[0].footer.text == self.menu_id:
                await self.menu.update_menu(reaction.message, reaction.emoji)
                await reaction.message.remove_reaction(reaction.emoji, user)

    def add_component(self, component):
        self.add_prefix(component.prefix)
        self.components.append(component)

    def add_prefix(self, prefix):
        if prefix in self.prefixes:
            raise Exception('prefixes have to be unique')
        self.prefixes.append(prefix)

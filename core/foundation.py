import configparser

import discord
import emoji

from components.configurator import Configurator
from components.session_planner import GameSessions
from components.time_messager import TimeMessager
from core.utils import discord_logger
from core.data.data_manager import DataMapper
from core.utils.help_menu import Menu


class HackerBot(discord.Client):

    def __init__(self, **options):
        super().__init__(**options)
        config = configparser.ConfigParser()
        config.read('config.ini')
        discord_logger.log("Initializing settings", 'yellow')

        self.prefix = config.get('GlobalSettings', 'default_prefix')
        discord_logger.log("Global prefix: '" + self.prefix + "'", 'header')

        self.data_mapper_servers = DataMapper(config.get("DatabaseSettings", "mongo_uri"),
                                              config.get("DatabaseSettings", "mongo_pass"),
                                              config.get("DatabaseSettings", "mongo_database"),
                                              config.get("DatabaseSettings", "mongo_collection_servers"))
        self.data_mapper_members = DataMapper(config.get("DatabaseSettings", "mongo_uri"),
                                              config.get("DatabaseSettings", "mongo_pass"),
                                              config.get("DatabaseSettings", "mongo_database"),
                                              config.get("DatabaseSettings", "mongo_collection_members"))
        self.menu_id = config.get('MenuSettings', 'menu_id')
        self.menu_up = config.get('MenuSettings', 'menu_up_indicator')
        self.menu_down = config.get('MenuSettings', 'menu_down_indicator')
        self.menu_select = config.get('MenuSettings', 'menu_select_indicator')
        self.menu_back = config.get('MenuSettings', 'menu_back_indicator')
        self.approved = config.get('MenuSettings', 'approved_indicator')

        discord_logger.log("Done initializing settings", 'yellow')

        self.components = []
        self.prefixes = []

        self.add_component(TimeMessager(self, 'Time Messages', 'kid', 'Kid\'s happy time messages'))
        self.add_component(Configurator(self, 'Configurator', 'config', 'Edit settings and bot behavior'))
        self.add_component(GameSessions(self, 'Game Sessions', 'session', 'Plan a session on your server'))

        self.menu = Menu(self.components, self.menu_id, self.menu_up, self.menu_down, self.menu_select, self.menu_back)

    async def router(self, args, message):
        if args[0] == '':
            await message.channel.send('`Please supply a valid component`')
            return
        if args[0] == 'menu':
            await self.menu.send_menu(args, message)
            return
        cmd = args[0]
        for component in self.components:
            if cmd == component.prefix:
                args.pop(0)
                await component.run(args, message)
                break
        else:
            await message.channel.send('`Component not found`')

    async def on_ready(self):
        self.data_mapper_servers.prepare_all_discord_server_data(self)
        string = "No components loaded"
        if len(self.components) > 0:
            string = "loaded components: "
            for component in self.components:
                string += component.name + ", "
            string = string[:-2]
        discord_logger.log(string, 'red')
        discord_logger.log("Ready - waiting for messages...", 'yellow')
        game = discord.Game("tic tac toe")
        await self.change_presence(status=discord.Status.online, activity=game)

    async def on_message(self, message):
        if message.author.id != self.user.id:
            prefix = self.data_mapper_servers.get_specific_server_data(message.guild, "server_prefix")['server_prefix']
            if prefix is None:
                prefix = self.prefix
            if message.content.startswith(prefix):
                args = message.content[len(prefix):]
                await self.router(args.split(' '), message)
            else:
                for component in self.components:
                    await component.default_run(message)

    async def on_reaction_add(self, reaction, user):
        if user.id != self.user.id:
            if reaction.message.embeds[0].footer.text == self.menu_id:
                await self.menu.update_menu(reaction.message, reaction.emoji)
                await reaction.message.remove_reaction(reaction.emoji, user)

    def add_component(self, component):
        discord_logger.log("preparing component (name: " + component.name + ")", 'yellow')
        component.setup(self)
        self.add_prefix(component.prefix)
        self.components.append(component)

    def add_prefix(self, prefix):
        discord_logger.log("preparing prefix (prefix: " + prefix + ")", 'yellow')
        if prefix in self.prefixes:
            raise Exception('prefixes have to be unique')
        self.prefixes.append(prefix)

import asyncio
import configparser

from components.session_planner import GameSessions
from core.foundation import HackerBot

config = configparser.ConfigParser()
config.read('config.ini')
client = HackerBot()
client.run(config.get('Auth', 'token'))

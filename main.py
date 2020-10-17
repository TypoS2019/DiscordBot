import configparser

from core.foundation import HackerBot

config = configparser.ConfigParser()
config.read('config.ini')
client = HackerBot()
client.run(config.get('Auth', 'token'))

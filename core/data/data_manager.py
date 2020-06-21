from pymongo import MongoClient

from core import discord_logger


class DataMapper():
    def __init__(self, uri, password, database, collection):
        discord_logger.log("Starting Data service", 'yellow')
        uri = uri.replace("<password>", password)

        self.client = MongoClient(uri)
        discord_logger.log("Connected to MongoDB cluster", 'yellow')

        self.database = self.client[database]
        self.collection = self.database[collection]

    def prepare_all_discord_server_data(self, client):
        discord_logger.log("preparing data for connected discord servers", 'blue')
        for guild in client.guilds:
            self.prepare_discord_server_data(guild)

    def prepare_discord_server_data(self, guild):
        doc = {"server_id": guild.id,
               "server_name": guild.name,
               "server_kid_channel": None,
               "server_prefix": None}
        if self.collection.find_one({"server_id": guild.id}) is None:
            discord_logger.log("adding discord server to Mongo Collection. name: " + guild.name, 'blue')
            self.collection.insert_one(doc)

    def get_server_data(self, guild):
        return self.collection.find_one({"server_id": guild.id})

    def get_all_specific_server_data(self, specific):
        return self.collection.find({}, {"_id": 0, specific: 1})

    def get_specific_server_data(self, guild, specific):
        query = {"server_id": guild.id}
        return self.collection.find_one(query, {"_id": 0, specific: 1})

    def set_specific_server_data(self, guild, specific, value):
        query = {"server_id": guild.id}
        value = {"$set": {specific: value}}
        self.collection.update_one(query, value)

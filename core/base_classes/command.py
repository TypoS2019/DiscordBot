class Command:
    def __init__(self, cmd, desc, client, enabled=True):
        self.cmd = cmd
        self.desc = desc
        self.enabled = enabled
        self.client = client

    async def run(self, args, message):
        message.channel.send('Hello!')

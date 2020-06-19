class Command:
    def __init__(self, cmd, desc, enabled=True):
        self.cmd = cmd
        self.desc = desc
        self.enabled = enabled

    def run(self, args, message):
        message.channel.send('Hello!')

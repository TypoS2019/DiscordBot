from core.utils.Enums import permissions


class Command:
    def __init__(self, cmd, desc, client, enabled=True, hidden=False, security=permissions.Member):
        self.cmd = cmd
        self.desc = desc
        self.enabled = enabled
        self.client = client
        self.security = security
        self.hidden = hidden

    async def run(self, args, message):
        message.channel.send('Hello!')

    def check_permission(self, permission_no):
        return self.security.int() >= permission_no.int()

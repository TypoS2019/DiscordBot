from core.base_classes.component import Component


class Wholesome(Component):
    def __init__(self, client, name, prefix, description='default component', enabled=True):
        super().__init__(client, name, prefix, description, enabled, icon=':stopwatch:')
        self.commands = []
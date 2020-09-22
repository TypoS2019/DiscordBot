import enum


class log_type(enum.Enum):
    RED = '\033[95m'
    YELLOW = '\033[91m'
    BLUE = '\033[93m'
    HEADER = '\033[94m'

    def color(self):
        return self.value


class permissions(enum.Enum):
    Test = -1
    Dev = 1
    Owner = 2
    Admin = 3
    Member = 4

    def int(self):
        return self.value


class reaction(enum.Enum):
    MENU_UP = ":up_arrow:"
    MENU_DOWN = ":down_arrow:"
    MENU_SELECT = ":OK_button:"
    MENU_BACK = ":left_arrow:"
    APPROVED = ":thumbs_up:"

    def emoji(self):
        return self.value

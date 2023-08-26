from enum import StrEnum, auto, IntEnum


class Cogs(StrEnum):
    CONNECTION_STATUS = auto()
    DEVELOPER_TOOLS = auto()


class EventTypes(IntEnum):
    EMBED = auto()
    MESSAGE = auto()

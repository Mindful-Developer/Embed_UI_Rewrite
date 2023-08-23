from models import EventType, orm
from utils.enums import EventTypes


@orm.db_session
def add_event_type(event_type_name):
    EventType(event_type_name=event_type_name)


def populate_event_types():
    event_type_names = [event_type.name for event_type in EventTypes]
    for event_type_name in event_type_names:
        add_event_type(event_type_name)

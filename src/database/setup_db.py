if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

from models import EventType, orm
from utils.enums import EventTypes


@orm.db_session
def populate_event_types():
    if EventType.select().count() > 0:
        return

    event_type_names = [event_type.name for event_type in EventTypes]
    for event_type_name in event_type_names:
        EventType(event_type_name=event_type_name)


if __name__ == '__main__':
    populate_event_types()

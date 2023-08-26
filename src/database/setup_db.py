from database.models import EventType, orm
from models.enums import EventTypes
import os


@orm.db_session
def populate_event_types():
    if EventType.select().count() > 0:
        return

    event_type_names = [event_type.name for event_type in EventTypes]
    for event_type_name in event_type_names:
        EventType(event_type_name=event_type_name)


def setup_db():
    if int(os.environ.get('DEV_MODE')):
        orm.set_sql_debug(True)
    else:
        orm.set_sql_debug(False)
    populate_event_types()

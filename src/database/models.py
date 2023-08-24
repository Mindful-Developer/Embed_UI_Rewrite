from pony import orm
import os


db = orm.Database()


class Guild(db.Entity):
    guild_id = orm.PrimaryKey(int)
    guild_mbeds = orm.Set('Mbed', cascade_delete=True)
    guild_events = orm.Set('Event', cascade_delete=True)


class User(db.Entity):
    user_id = orm.PrimaryKey(int)
    user_timezone = orm.Optional(str, nullable=True)
    user_mbeds = orm.Set('Mbed', cascade_delete=True)
    user_events = orm.Set('Event', cascade_delete=True)


class MbedField(db.Entity):
    mbed_field_id = orm.PrimaryKey(int, auto=True)
    mbed_field_position = orm.Required(int)
    mbed_field_name = orm.Optional(str, 256, default='\u200b')
    mbed_field_value = orm.Optional(str, 1024, default='\u200b')
    mbed_field_inline = orm.Required(bool)
    mbed_field_mbed = orm.Required('Mbed')

    @property
    def size(self):
        return len(self.mbed_field_name) + len(self.mbed_field_value)

class EventType(db.Entity):
    event_type_id = orm.PrimaryKey(int, auto=True)
    event_type_name = orm.Required(str, unique=True)
    event_type_events = orm.Set('Event', cascade_delete=True)


class Mbed(db.Entity):
    mbed_id = orm.PrimaryKey(int, auto=True)
    mbed_name = orm.Optional(str, nullable=True)
    mbed_color = orm.Optional(str, nullable=True)
    mbed_title = orm.Optional(str, 256, default='\u200b')
    mbed_description = orm.Optional(str, 4096, default='\u200b')
    mbed_footer = orm.Optional(str, 2048, nullable=True)
    mbed_author = orm.Optional(str, 256, nullable=True)
    mbed_author_url = orm.Optional(str, nullable=True)
    mbed_thumbnail_url = orm.Optional(str, nullable=True)
    mbed_image_url = orm.Optional(str, nullable=True)
    mbed_footer_url = orm.Optional(str, nullable=True)
    mbed_guild = orm.Optional(Guild)
    mbed_user = orm.Optional(User)
    mbed_fields = orm.Set(MbedField, cascade_delete=True)

    @property
    def remaining_chars(self):
        chars = 6000
        mbed_contributors = [self.mbed_title, self.mbed_description, self.mbed_author, self.mbed_footer]

        for contributor in mbed_contributors:
            chars -= len(contributor) if contributor else 0

        for field in self.mbed_fields:
            chars -= field.size

        return chars


class Event(db.Entity):
    event_id = orm.PrimaryKey(int, auto=True)
    event_guild = orm.Optional(Guild)
    event_user = orm.Optional(User)
    event_channel_id = orm.Required(int)
    event_timestamp = orm.Required(int)
    event_data = orm.Required(str)
    event_is_dm = orm.Required(bool)
    event_type = orm.Required(EventType)


db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

if int(os.environ.get('DEV_MODE')):
    orm.set_sql_debug(True)

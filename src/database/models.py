from pony import orm
import os


db = orm.Database()


class Guild(db.Entity):
    guild_id = orm.PrimaryKey(int)
    guild_embeds = orm.Set('Embed', cascade_delete=True)
    guild_events = orm.Set('Event', cascade_delete=True)


class User(db.Entity):
    user_id = orm.PrimaryKey(int)
    user_timezone = orm.Optional(str, nullable=True)
    user_embeds = orm.Set('Embed', cascade_delete=True)
    user_events = orm.Set('Event', cascade_delete=True)


class EmbedField(db.Entity):
    embed_field_id = orm.PrimaryKey(int, auto=True)
    embed_field_position = orm.Required(int)
    embed_field_name = orm.Optional(str, 256, default='\u200b')
    embed_field_value = orm.Optional(str, 1024, default='\u200b')
    embed_field_inline = orm.Required(bool)
    embed_field_embed = orm.Required('Embed')

    @property
    def size(self):
        return len(self.embed_field_name) + len(self.embed_field_value)


class EventType(db.Entity):
    event_type_id = orm.PrimaryKey(int, auto=True)
    event_type_name = orm.Required(str, unique=True)
    event_type_events = orm.Set('Event', cascade_delete=True)


class Embed(db.Entity):
    embed_id = orm.PrimaryKey(int, auto=True)
    embed_name = orm.Optional(str, nullable=True)
    embed_colour = orm.Optional(str, nullable=True)
    embed_title = orm.Optional(str, 256, default='\u200b')
    embed_description = orm.Optional(str, 4096, default='\u200b')
    embed_footer = orm.Optional(str, 2048, nullable=True)
    embed_author = orm.Optional(str, 256, nullable=True)
    embed_author_url = orm.Optional(str, nullable=True)
    embed_thumbnail_url = orm.Optional(str, nullable=True)
    embed_image_url = orm.Optional(str, nullable=True)
    embed_footer_url = orm.Optional(str, nullable=True)
    embed_guild = orm.Optional(Guild)
    embed_user = orm.Optional(User)
    embed_fields = orm.Set(EmbedField, cascade_delete=True)

    @property
    def remaining_chars(self):
        chars = 6000
        embed_contributors = [self.embed_title, self.embed_description, self.embed_author, self.embed_footer]

        for contributor in embed_contributors:
            chars -= len(contributor) if contributor else 0

        for field in self.embed_fields:
            chars -= field.size

        return chars

    @property
    def remaining_fields(self):
        return 25 - len(self.embed_fields)


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

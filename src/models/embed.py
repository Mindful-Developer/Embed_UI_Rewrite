from disnake import Embed as DisnakeEmbed
from database.models import Embed as EmbedModel


class Embed(DisnakeEmbed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def from_orm(orm_embed: EmbedModel) -> DisnakeEmbed:
        """Converts an EmbedModel to a Disnake Embed"""
        embed = Embed()
        embed.title = orm_embed.embed_title
        embed.description = orm_embed.embed_description
        embed.colour = int(orm_embed.embed_colour, 16) if orm_embed.embed_colour else None
        embed.set_footer(text=orm_embed.embed_footer, icon_url=orm_embed.embed_footer_url)
        embed.set_author(name=orm_embed.embed_author, url=orm_embed.embed_author_url)
        embed.set_thumbnail(url=orm_embed.embed_thumbnail_url)
        embed.set_image(url=orm_embed.embed_image_url)

        for field in orm_embed.embed_fields:
            embed.add_field(name=field.embed_field_name, value=field.embed_field_value, inline=field.embed_field_inline)

        return embed

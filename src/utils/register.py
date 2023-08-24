import sys


def register_cog(cls):
    """Registers a cog to the bot. (*ONLY SUPPORTS ONE COG PER FILE)"""
    def setup(client):
        client.add_cog(cls(client))
        print(f"{cls.__name__} loaded")
    mod = sys.modules[cls.__module__]
    mod.setup = setup
    return cls

import sys


def register_cog(cls):
    def setup(bot):
        bot.add_cog(cls(bot))
        print(f"{cls.__name__} loaded")
    mod = sys.modules[cls.__module__]
    mod.setup = setup
    return cls

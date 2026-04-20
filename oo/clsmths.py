

# class Settings:
#     _theme = ""
#     _language = ""
#
#     @classmethod
#     def load(cls):
#         cls
#
#     @classmethod
#     def theme(cls):
#         if cls._theme == False:
#             cls.load()
#
#         return cls.theme

# FUNCTIONAL PROGRAMMING
# Logging
from oo.logfac import LoggerFactory

_logger = LoggerFactory.get_logger("clsmths")

def mountain(s: str) -> str:
    return "".join((c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(s)))

print(mountain("Brent Hendricx"))

# OO PROGRAMMING
# logging
class Utils:
    _logger = LoggerFactory.get_logger("Utils")

    @classmethod
    def mountain(cls, s: str) -> str:
        cls._logger.debug("mountain")
        return "".join((c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(s)))

print(Utils.mountain("Brent Hendricx"))
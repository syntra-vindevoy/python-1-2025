from oo.loggerfactory import Loggerfactory
class Utils:
    _logger = Loggerfactory.get_logger("Utils")

    @classmethod
    def mountain(cls, s: str) -> str:
        cls._logger.info("mountain")
        return "".join(c.upper() if i%2 == 0 else c.lower() for i, c in enumerate(s))

print(Utils.mountain("vorsselmans"))

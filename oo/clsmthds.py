from oo.logfac import LoggerFactory



class Utils:
    _logger = LoggerFactory.get_logger("Utils")

    @classmethod
    def mountain(cls, s: str) -> str:
        cls._logger.info("Mountain")
        return "".join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(s))

print(Utils.mountain("vindevogel"))
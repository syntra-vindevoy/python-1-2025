import logging


class LoggerFactory:
    @classmethod
    def get_logger(cls, identifier: str, level: int = logging.INFO):
        logger = logging.getLogger(identifier)
        logger.setLevel(level)

        handler = logging.StreamHandler()
        handler.setLevel(level)

        formatter = logging.Formatter(
            fmt="%(asctime)s.%(msecs)03d %(levelname)8s %(message)s  (%(name)s)",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        handler.setFormatter(formatter)

        logger.addHandler(handler)

        return logger

class LoggingObject:
    def __init__(self):
        self.logger = LoggerFactory.get_logger(self.__class__.__name__)


class Client:
    logger = LoggerFactory.get_logger("Client", logging.DEBUG)

    def __init__(self, name: str):
        self.name = name

    def save(self):
        self.logger.info(f"Saving information for client: {self.name}")


class Supplier(LoggingObject):
    def __init__(self, name: str):
        super().__init__()

        self.name = name

    def save(self):
        self.logger.info(f"Saving information for supplier: {self.name}")

def main():
    c = Client("Yves")
    c.logger.debug(f"name: {c.name}")
    c.save()

    s = Supplier("Syntra")
    s.logger.info(f"name: {s.name}")
    s.save()

if __name__ == "__main__":
    main()

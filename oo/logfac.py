import logging

class LoggerFactory:
    @classmethod # Class methode uses cls instead of self
    def get_logger(cls, indentifier: str, level: int = "logging".INFO):     # Logging can't be used since import is later. "Truk van de foor", Put it between " ".
        logger = logging.getLogger(indentifier)
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()  # Rotating StreamHandler (how many files and how big may they get). IMPORTANT USE
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            fmt="%(asctime)s.%(msecs)03d %(levelname)8s %(message)s",  # 03d (3 decimals cutoff), 8s (8 spaces)
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        handler.setFormatter(formatter)

        logger.addHandler(handler)

        return logger

class LoggingObject:    # Methode 2
    def __init__(self):
        self.logger = LoggerFactory.get_logger(self.__class__.__name__)


class Client:   # Simple class for showing a way to get logger into a class.
    logger = LoggerFactory.get_logger("Client") # Methode 1

    def __init__(self, name: str):
        self.name = name

    def save(self):
        self.logger.info(f"Saving information for client: {self.name}")

class Supplier(LoggingObject):
    def __init__(self):
        super().__init__()


def main():
    # Code when only LoggerFactory was the only class.
    # logger = LoggerFactory.get_logger("my_logger")
    # logger.info("Hello world")

    # Methode 1
    c = Client("Yves")
    c.logger.debug(f"name: {c.name}")
    c.save()



if __name__ == "__main__":
    main()
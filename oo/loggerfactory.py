import logging
class Loggerfactory:
    @classmethod #hierdoor moet je de class niet instantieren
    def get_logger(cls, identifier:str, level: int = logging.INFO):

        logger  = logging.getLogger(identifier)
        logger.setLevel(level)

        handler = logging.StreamHandler()
        handler.setLevel(level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        handler.setFormatter(formatter)

        logger.addHandler(handler)

        return logger

class LoggingObject:
    def __init__(self):
        self.logger = Loggerfactory.get_logger(self.__class__.__name__)

class Client: #composition, je hebt object en al wat je nog nodig hebt, sleur je er gewoon bij, meest eenvoudige/intuitieve manier
    logger = Loggerfactory.get_logger("Client")
    def __init__(self, name:str):
        self.name = name

    def save(self):
        self.logger.info(f"saving information for client {self.name}")

class Supplier(LoggingObject):
    def __init__(self, name):
        super().__init__()
        self.name = name
    def save(self):
        self.logger.info(f"saving information for supplier {self.name}")


def main():
    c = Client("test")
    c.save()

    s = Supplier("Syntra")
    s.logger.info(f"name = {s.name}")
    s.save()

if __name__ == "__main__":
    main()

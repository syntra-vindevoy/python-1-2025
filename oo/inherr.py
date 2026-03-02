
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

# ... existing code ...
formatter = logging.Formatter(
    fmt="%(asctime)s.%(msecs)03d %(levelname)8s %(message)s  (%(name)s)",
    datefmt="%Y-%m-%d %H:%M:%S"
)
# ... existing code ...
handler.setFormatter(formatter)

logger.addHandler(handler)


class TotoValueError(ValueError):
    def __init__(self, message: str):
        super().__init__(message)
        logger.error(message)
def divide(x, y):
    if y == 0:
        raise TotoValueError("y cannot be 0")

class DatabaseException(Exception):
    pass

def main():
    divide(1, 0)

if __name__ == '__main__':
    main()

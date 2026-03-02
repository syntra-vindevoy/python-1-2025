import logging
from inherr import TotoValueError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

# ... existing code ...
formatter = logging.Formatter(
    fmt="%(asctime)s.%(msecs)03d %(levelname)8s %(message)s  (%(name)s)",
    datefmt="%Y-%m-%d %H:%M:%S"
)
# ... existing code ...
handler.setFormatter(formatter)

logger.addHandler(handler)

class MyClass:
    def __init__(self):
        logger.debug("MyClass.__init__")

    def my_method(self):
        logger.debug("MyClass.my_method")



def main():
    my_class = MyClass()
    my_class.my_method()

if __name__ == "__main__":
    main()

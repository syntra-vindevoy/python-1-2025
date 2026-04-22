import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')




class TotoValueError(ValueError):
    def __init__(self, message:str):
        super().__init__(message)
        logger.error(message)


def divide(x,y):
    if y==0:
        raise TotoValueError("y cannot be 0")

class DatabaseException(Exception):
    pass

def main():
    divide(1,0)

if __name__ == '__main__':
    main()
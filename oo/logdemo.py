import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)   # App doesn't work? -> use DEBUG.   Works again? -> Use INFO
# Set the program executing logger level in another file.
# Logger warning levels: NOTSET, (TRACE,) DEBUG, INFO, (SUCCES,) WARNING, ERROR, CRITICAL (,FATAL)
                     #   0,      (5,)     10,    20,   (25,)     30,      40,    40,      (60)
#   () are added by Yves as addons

# Logging to a cue due to the logger locking a file in multithreading when another tries to write to it.
# Change standerd to LogGuru

handler = logging.StreamHandler()   # Rotating StreamHandler (how many files and how big may they get). IMPORTANT USE
handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    fmt="%(asctime)s.%(msecs)03d %(levelname)8s %(message)s",   # 03d (3 decimals cutoff), 8s (8 spaces)
    datefmt="%Y-%m-%d %H:%M:%S"
)

handler.setFormatter(formatter)

logger.addHandler(handler)

class MyClass:
    def __init__(self):
        logger.info("MyClass.__init__")

    def my_method(self):
        logger.info("MyClass.my_method")

def main():
    my_class = MyClass()
    my_class.my_method()

if __name__ == "__main__":
    main()

from logfac import LoggerFactory
from oo_fibo import Fibonacci

logger = LoggerFactory.get_logger(__name__)


def main():
    logger.info("starting main")

    for i in range(10):
        logger.success(f"fibo({i}) = {Fibonacci.fibo(i)}")

    logger.info("finished main")


if __name__ == "__main__":
    logger.info("running logging_fibo as __main__")

    main()
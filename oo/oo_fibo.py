from logfac import LoggingObject


class Fibonacci(LoggingObject):
    @classmethod
    def fibo(cls, n):
        cls.logger.info(f"fibo called with n={n}")

        if n < 0:
            cls.logger.error(f"invalid input: n={n} must be non-negative")
            raise ValueError("n must be non-negative")

        if n == 0:
            cls.logger.debug("n=0, returning 0")
            return 0

        a, b = 0, 1

        for i in range(n - 1):
            a, b = b, a + b
            cls.logger.debug(f"iteration {i}: a={a}, b={b}")

        cls.logger.info(f"fibo({n}) = {b}")
        return b

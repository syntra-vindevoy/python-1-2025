import inspect
from functools import wraps

from shiny_app.core.logfac import LoggerFactory


def trace(func):
    def _resolve(args):
        if args and hasattr(args[0], "logger"):
            return args[0].logger, args[1:]

        return LoggerFactory.get_logger(func.__module__), args

    def _format(params_args, kwargs):
        return ", ".join(
            [repr(a) for a in params_args] + [f"{k}={v!r}" for k, v in kwargs.items()]
        )

    if inspect.iscoroutinefunction(func):

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            logger, params_args = _resolve(args)

            params = _format(params_args, kwargs)

            logger.trace(f"entering {func.__qualname__}({params})")

            result = await func(*args, **kwargs)

            logger.trace(f"exiting {func.__qualname__}")

            return result

        return async_wrapper

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger, params_args = _resolve(args)

        params = _format(params_args, kwargs)

        logger.trace(f"entering {func.__qualname__}({params})")

        result = func(*args, **kwargs)

        logger.trace(f"exiting {func.__qualname__}")

        return result

    return wrapper


def enable_tracing(cls):
    for name, attr in list(vars(cls).items()):
        if isinstance(attr, staticmethod):
            setattr(cls, name, staticmethod(trace(attr.__func__)))
        elif isinstance(attr, classmethod):
            setattr(cls, name, classmethod(trace(attr.__func__)))
        elif inspect.isfunction(attr):
            setattr(cls, name, trace(attr))

    return cls


def enable_logging(cls):
    cls.logger = LoggerFactory.get_logger(cls.__name__)

    return cls

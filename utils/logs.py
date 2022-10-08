import logging
import os
import datetime


def createLogger(level: int = logging.INFO, logPath: str = "logs") -> None:
    """Creates a logging logger

    Args:
        level (int, optional): The verbosity to log. Defaults to logging.INFO.
        logPath (str, optional): Where to save the log. Defaults to 'logs'.
    """

    filename = uniquifyLogName(
        os.path.join(logPath, f"{str(datetime.date.today())}.log")
    )
    ensurePath(logPath)  # Ensure the path exists

    logging.basicConfig(
        filename=filename,
        filemode="w",
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=level,
    )


def uniquifyLogName(path: str) -> str:
    """Ensures that the log name is unique to avoid overwriting.

    Args:
        path (str): the path leading up to the log name.

    Returns:
        str: The unique log path.
    """

    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1

    return path


def ensurePath(path: str) -> str:
    """Enures that the path exists. If it doesn't, it creates it.

    Returns:
        str: the path that was ensured.
    """

    if not os.path.exists(path):
        os.makedirs(path)

    return path


def logBeforeAndAfter(
    before: str = None, after: str = None, level: int = logging.INFO
) -> callable:
    """Decorator to log before and after a function is called.

    Args:
        before (str, optional): Message to log before the function is called. If None, nothing will be logged. Defaults to None.
        after (str, optional): Message to log after the function is called. If None, nothing will be logged. Defaults to None.
        level (int, optional): What level to log the messages at. Defaults to logging.INFO.

    Returns:
        callable: Decorator return.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            if before:
                logging.log(level, before)
            result = func(*args, **kwargs)
            if after:
                logging.log(level, after)
            return result

        return wrapper

    return decorator

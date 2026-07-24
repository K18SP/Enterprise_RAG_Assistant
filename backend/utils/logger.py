# import logging

# logging.basicConfig(
#     level = logging.INFO,
#     format = "%(asctime)s | %(levelname)s | %(message)s"
# )

# logger = logging.getLogger("EnterPriseRAG")
import logging
import sys


def setup_logger(name: str) -> logging.Logger:
    """
    Create and configure a logger.
    """

    logger = logging.getLogger(name) # For providing own logger to each module

    # Prevent duplicate handlers
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO) #Applied log level "INFO"

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger
import logging
import sys

from pythonjsonlogger.json import JsonFormatter


def setup_logging(debug: bool = False, environment: str = "development"):
    """
    Configura logging global:
    - Desarrollo: colores y formato legible
    - Producción: JSON
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    handler = logging.StreamHandler(sys.stdout)

    formatter: logging.Formatter
    if environment == "production":
        formatter = JsonFormatter("%(asctime)s %(name)s %(levelname)s %(message)s")
    else:
        formatter = logging.Formatter(
            "\033[92m[%(asctime)s]\033[0m "  # verde fecha
            "\033[94m%(levelname)s\033[0m "  # azul nivel
            "\033[96m%(name)s\033[0m → "  # cian logger name
            "%(message)s",
            "%Y-%m-%d %H:%M:%S",
        )

    handler.setFormatter(formatter)
    logger.handlers = [handler]

    return logger

import logging
from datetime import datetime
import os

def configurar_logger():
    """Configura el logger para registrar eventos y errores"""
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.DEBUG)

    # Evitar duplicar handlers si se llama varias veces
    if logger.handlers:
        return logger

    # Archivo de logs
    fh = logging.FileHandler("logs/sistema.log", encoding="utf-8")
    fh.setLevel(logging.DEBUG)

    # Consola
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


logger = configurar_logger()
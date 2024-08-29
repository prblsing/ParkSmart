import logging


def setup_logger(log_level='INFO'):
    """
    Set up the logging configuration.

    Args:
        log_level (str): The logging level to set ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
    """
    logging.basicConfig(level=getattr(logging, log_level),
                        format='%(asctime)s - %(levelname)s - %(message)s')


def get_logger(name, log_level='INFO'):
    """
    Get a configured logger.

    Args:
        name (str): Name of the logger.
        log_level (str): The logging level to set ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').

    Returns:
        logging.Logger: Configured logger instance.
    """
    setup_logger(log_level)
    return logging.getLogger(name)

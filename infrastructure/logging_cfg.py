import logging.config


def setup_logging(cfg: dict):
    logging.config.dictConfig(cfg)

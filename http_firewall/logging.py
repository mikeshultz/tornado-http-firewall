import logging

parent_logger = logging.getLogger()


def get_logger(name):
    """ Return a child logger """
    return parent_logger.getChild(name)


def set_debug_logging():
    """ Set debug level loggin """
    parent_logger.setLevel(logging.DEBUG)


def logging_shutdown():
    return logging.shutdown()

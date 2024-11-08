#
# This module contains various helper routines to get things working
# the way I want them
#
import structlog


def configure_logging(logging_level: int) -> object:
    """
    This function configures logging using the structlog module.
    :param logging_level: int logging level to use
    :return: None
    """
    shared_processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
    ]
    level_styles = structlog.dev.ConsoleRenderer().get_default_level_styles()
    level_styles["debug"] = "\x1b[36m"
    processors = [
        *shared_processors,
        structlog.dev.ConsoleRenderer(colors=True, level_styles=level_styles),
    ]
    structlog.configure(
        processors=processors,
        context_class=dict,
        wrapper_class=structlog.make_filtering_bound_logger(logging_level),
        cache_logger_on_first_use=True,
    )

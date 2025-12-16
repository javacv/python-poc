# logging_config.py

import logging
import sys
from flask import g, has_request_context


class ContextFilter(logging.Filter):
    def filter(self, record):
        if has_request_context():
            record.service_name = getattr(g, "service_name", "-")
            record.path = getattr(g, "path", "-")
        else:
            # Logging outside request (startup, tests, etc.)
            record.service_name = "-"
            record.path = "-"
        return True


def setup_logging():
    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | "
        "service=%(service_name)s | path=%(path)s | %(message)s"
    )

    handler.setFormatter(formatter)
    handler.addFilter(ContextFilter())

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers.clear()   # IMPORTANT: avoid duplicate logs
    root.addHandler(handler)

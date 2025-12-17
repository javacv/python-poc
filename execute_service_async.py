# execute_service_async.py

import importlib
import logging

logger = logging.getLogger("execute_service_async")


def execute_service_async(service_name: str, context: dict):
    """
    Runs outside HTTP request lifecycle.
    MUST NOT touch Flask request objects.
    """
    try:
        logger.info("Async execution started for service=%s", service_name)

        module = importlib.import_module(f"services.{service_name}")
        handler = getattr(module, "handle")

        handler(context)

        logger.info("Async execution completed for service=%s", service_name)

    except ModuleNotFoundError:
        logger.error("Service module not found: %s", service_name)

    except AttributeError:
        logger.error("Handler not found for service: %s", service_name)

    except Exception:
        logger.exception("Async execution failed for service=%s", service_name)
        
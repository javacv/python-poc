# interceptor.py

import time
import logging
from flask import request, g, jsonify

logger = logging.getLogger("interceptor")

def pre_handle():
    g.start_time = time.time()

    # Set logging context (MDC-style)
    if request.view_args:
        g.service_name = request.view_args.get("service_name")
        g.path = request.path
    else:
        g.service_name = "NA"
        g.path = "NA"
    

    logger.info("Incoming request")

    # Example: auth check (Spring HandlerInterceptor preHandle vibes)
    if request.path.startswith("/api"):
        token = request.headers.get("Authorization")
        if not token:
            logger.error(
                "Incoming request"
            )
            return jsonify({"error": "Unauthorized"}), 401


def post_handle(response):
    duration_ms = (time.time() - g.start_time) * 1000
    logger.info("Request completed in %.2f ms", duration_ms)
    return response


def after_completion(error=None):
    if error:
        logger.exception("Unhandled exception")

# execute_service_async.py

from flask import Blueprint, jsonify, request
import logging

from background_executor import background_executor
from execute_service_async import execute_service_async

logger = logging.getLogger("controller")

api = Blueprint("api", __name__)


@api.route("/execute/async/<string:service_name>", methods=["POST"])
def execute_async(service_name): 
    logger.info("Execute async service")


@api.route("/execute/sync/<string:service_name>", methods=["GET"])
def dispatch(service_name):
    logger.info("Received async dispatch request")

    context = {
        "service_name": service_name,
        "query_params": request.args.to_dict(),
        "headers": dict(request.headers),
        "method": request.method,
        "path": request.path
    }

    # 🚀 Submit async execution
    background_executor.submit(
        execute_service_async,
        service_name,
        context
    )

    # ✅ Immediate ACK
    return jsonify({
        "status": "ACCEPTED",
        "service": service_name
    }), 202
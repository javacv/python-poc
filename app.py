from flask import Flask, jsonify, request
from interceptor import pre_handle, post_handle, after_completion
from logging_config import setup_logging
import importlib
import logging

# Initialize logging FIRST
setup_logging()

logger = logging.getLogger("app")

app = Flask(__name__)

app.before_request(pre_handle)
app.after_request(post_handle)
app.teardown_request(after_completion)




@app.route("/data/<string:service_name>", methods=["GET"])
def dispatch(service_name):
    logger.info("Dispatching service")
    try:

        context = {
            "service_name": service_name,
            "query_params": request.args.to_dict(),
            "headers": dict(request.headers),
            "method": request.method,
            "path": request.path
        }
        # Dynamically import module at runtime
        module = importlib.import_module(f"services.{service_name}")

        # Dynamically resolve function
        handler = getattr(module, "handle")

        # Execute with map argument
        result = handler(context)
        logger.info("Dispatching service")

        return jsonify(result), 200

    except ModuleNotFoundError:
        return jsonify({"error": "Service module not found"}), 404

    except AttributeError:
        return jsonify({"error": "Handler method not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

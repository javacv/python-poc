# app.py

from flask import Flask
from interceptor import pre_handle, post_handle, after_completion
from logging_config import setup_logging
from controller import api

import logging

# Initialize logging FIRST
setup_logging()

logger = logging.getLogger("app")

app = Flask(__name__)

# Register interceptors
app.before_request(pre_handle)
app.after_request(post_handle)
app.teardown_request(after_completion)

# Register controller
app.register_blueprint(api)

if __name__ == "__main__":
    logger.info("Starting Flask application")
    app.run(debug=True)

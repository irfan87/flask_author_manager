import os
import logging
import sys

from flask import Flask, jsonify

from src.api.utils.database import db
from src.api.utils.responses import response_with

import src.api.utils.responses as resp

from src.api.routes.authors import author_routes
from src.api.routes.books import book_routes

from src.api.config.config import DevelopmentConfig, TestingConfig, ProductionConfig

app = Flask(__name__)

if os.environ.get('WORK_ENV') == 'PROD':
    app_config = ProductionConfig

elif os.environ.get('WORK_ENV') == 'TEST':
    app_config = TestingConfig

else:
    app_config = DevelopmentConfig

app.config.from_object(app_config)

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(author_routes, url_prefix='/api/authors')
app.register_blueprint(book_routes, url_prefix='/api/books')

# GLOBAL CONFIGURATIONS
@app.after_request
def add_header(response):
    return response

@app.errorhandler(400)
def bad_request(error):
    logging.error(error)

    return response_with(resp.BAD_REQUEST_400)

@app.errorhandler(500)
def server_error(error):
    logging.error(error)

    return response_with(resp.SERVER_ERROR_500)

@app.errorhandler(404)
def not_found(error):
    logging.error(error)

    return response_with(resp.SERVER_ERROR_404)

db.init_app(app)

with app.app_context():
    db.create_all()

logging.basicConfig(stream=sys.stdout, format='%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s', level=logging.DEBUG)

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', use_reloader=False)
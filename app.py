from src.flask_app import app
from src.error_handlers import setup_error_handlers
from src.settings import FLASK_HOST, FLASK_PORT, DEBUG

setup_error_handlers(app)

from src.controlers.root import *
from src.controlers.platform.ads import *
from src.controlers.platform.summary import *
from src.controlers.geral.all import *
from src.controlers.geral.summary import *


if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=DEBUG)
    
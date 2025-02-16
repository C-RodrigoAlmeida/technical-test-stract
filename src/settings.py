from os import environ

FLASK_HOST = environ.get("FLASK_HOST", "localhost")
FLASK_PORT = environ.get("FLASK_PORT", None)

DEBUG = environ.get("DEBUG", False)

API_BASE_URL = environ.get("API_BASE_URL", "https://sidebar.stract.to/api/")
API_TOKEN = environ.get("API_TOKEN")

AUTHOR_NAME = environ.get("AUTHOR_NAME", "Rodrigo de Carvalho Almeida")
AUTHOR_EMAIL = environ.get("AUTHOR_EMAIL", "c.almeidarodrigo@example.com")
AUTHOR_LINKEDIN = environ.get("AUTHOR_LINKEDIN", "https://www.linkedin.com/in/c-almeidarodrigo/")
        
if not API_TOKEN:
    raise RuntimeError("No API_TOKEN defined")

# web/backend/app.py
from flask import Flask
from flask_cors import CORS
from web.backend.api import create_api
from db import manager
manager.init_db()

app = Flask(__name__)
CORS(app)

# API 블루프린트 등록
create_api(app)

if __name__ == "__main__":
    app.run(port=5001)
from flask import Blueprint
from flask_socketio import SocketIO
from flask_cors import CORS

bp = Blueprint('tools', __name__)
socketio = SocketIO(cors_allowed_origins="*")

def init_app(app):
    CORS(app)
    socketio.init_app(app, cors_allowed_origins="*")
    app.register_blueprint(bp)
    
    # 注册工具蓝图
    from .duplicate_files import bp as duplicate_files_bp
    app.register_blueprint(duplicate_files_bp) 
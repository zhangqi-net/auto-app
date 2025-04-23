from flask import Blueprint
from flask_socketio import SocketIO

bp = Blueprint('tools', __name__)
socketio = SocketIO()

def init_app(app):
    socketio.init_app(app)
    app.register_blueprint(bp)
    
    # 注册工具蓝图
    from .duplicate_files import bp as duplicate_files_bp
    app.register_blueprint(duplicate_files_bp) 
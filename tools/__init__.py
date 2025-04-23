# Copyright 2024 zhangqi-net
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from tools import init_app, socketio
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # 用于flash消息
    
    # 配置
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    
    # 启用CORS
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # 添加中间件
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # 初始化工具模块
    init_app(app)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/about')
    def about():
        return render_template('about.html')
    
    @app.errorhandler(403)
    def handle_403(e):
        return jsonify({"error": "Forbidden"}), 403
    
    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({"error": "Not Found"}), 404
    
    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({"error": "Internal Server Error"}), 500
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    return app

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5001, allow_unsafe_werkzeug=True)

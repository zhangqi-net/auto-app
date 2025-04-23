from flask import Flask, render_template
from tools import init_app, socketio

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # 用于flash消息
    
    # 初始化工具模块
    init_app(app)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/about')
    def about():
        return render_template('about.html')
    
    return app

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True)

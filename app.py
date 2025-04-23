import os
import hashlib
import time
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from collections import defaultdict
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于flash消息
socketio = SocketIO(app)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # 用于会话安全

# 配置
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def calculate_hash(file_path, block_size=65536):
    """计算文件的MD5哈希值"""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            hasher.update(block)
    return hasher.hexdigest()

def find_duplicate_files(directory):
    """查找目录中的重复文件"""
    file_hashes = defaultdict(list)
    total_files = 0
    scanned_files = 0

    # 计算总文件数
    for root, _, files in os.walk(directory):
        total_files += len(files)
    
    # 扫描文件并计算哈希值
    for root, _, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_hash = calculate_hash(file_path)
            file_hashes[file_hash].append(file_path)
            scanned_files += 1
            # 发送进度更新
            socketio.emit('progress', {
                'total_files': total_files,
                'scanned_files': scanned_files,
                'progress': (scanned_files / total_files) * 100 if total_files > 0 else 0
            })
    
    # 返回最终结果
    duplicates = {hash_val: paths for hash_val, paths in file_hashes.items() if len(paths) > 1}
    socketio.emit('scan_complete', {
        'total_files': total_files,
        'duplicates': duplicates
    })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/scan', methods=['POST'])
def scan():
    directory = request.form.get('directory')
    if not directory or not os.path.exists(directory):
        flash('请选择有效的目录！')
        return redirect(url_for('index'))
    
    # 启动扫描任务
    socketio.start_background_task(target=lambda: find_duplicate_files(directory))
    return jsonify({'status': 'scanning'})

@app.route('/delete', methods=['POST'])
def delete_files():
    selected_files = request.form.getlist('files[]')
    for file_path in selected_files:
        try:
            os.remove(file_path)
            flash(f"已删除文件：{file_path}")
        except Exception as e:
            flash(f"删除文件失败：{file_path} - {str(e)}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    socketio.run(app, debug=True)

import os
import hashlib
from collections import defaultdict
from flask import render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_socketio import emit
from . import bp
from .. import socketio

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
            try:
                file_hash = calculate_hash(file_path)
                file_hashes[file_hash].append(file_path)
                scanned_files += 1
                # 发送进度更新
                socketio.emit('progress', {
                    'total_files': total_files,
                    'scanned_files': scanned_files,
                    'progress': (scanned_files / total_files) * 100 if total_files > 0 else 0
                })
            except Exception as e:
                print(f"Error processing file {file_path}: {str(e)}")
    
    # 返回最终结果
    duplicates = {hash_val: paths for hash_val, paths in file_hashes.items() if len(paths) > 1}
    socketio.emit('scan_complete', {
        'total_files': total_files,
        'duplicates': duplicates
    })

@bp.route('/')
def index():
    return render_template('tools/duplicate_files/index.html')

@bp.route('/scan', methods=['POST'])
def scan():
    try:
        directory = request.form.get('directory')
        if not directory or not os.path.exists(directory):
            response = make_response(jsonify({'error': '请选择有效的目录！'}), 400)
            return response
        
        # 启动扫描任务
        socketio.start_background_task(target=lambda: find_duplicate_files(directory))
        response = make_response(jsonify({'status': 'scanning'}), 200)
        return response
    except Exception as e:
        response = make_response(jsonify({'error': str(e)}), 500)
        return response

@bp.route('/delete', methods=['POST'])
def delete_files():
    try:
        selected_files = request.form.getlist('files[]')
        if not selected_files:
            return jsonify({
                'success': False,
                'error': '请选择要删除的文件！'
            }), 400
        
        deleted_files = []
        failed_files = []
        
        for file_path in selected_files:
            try:
                os.remove(file_path)
                deleted_files.append(file_path)
            except Exception as e:
                failed_files.append({
                    'path': file_path,
                    'error': str(e)
                })
        
        if failed_files:
            return jsonify({
                'success': True,
                'message': f'成功删除 {len(deleted_files)} 个文件，{len(failed_files)} 个文件删除失败',
                'deleted_files': deleted_files,
                'failed_files': failed_files
            })
        else:
            return jsonify({
                'success': True,
                'message': f'成功删除 {len(deleted_files)} 个文件',
                'deleted_files': deleted_files
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 
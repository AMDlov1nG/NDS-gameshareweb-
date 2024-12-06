from flask import Flask, send_from_directory, jsonify, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 需要设置用于闪现消息的密钥

FILE_FOLDER = '/www/wwwroot/ndswwww/game'  # 替换为您要读取的文件夹路径
ALLOWED_EXTENSIONS = {'nds', 'zip', 'rar', '7z'}  # 允许的文件扩展名
ADMIN_USERNAME = 'lov1nG'
ADMIN_PASSWORD = '******'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/files', methods=['GET'])
def get_file_list():
    try:
        files = os.listdir(FILE_FOLDER)
        return jsonify(files)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/files_with_size', methods=['GET'])
def get_files_with_size():
    try:
        files = os.listdir(FILE_FOLDER)
        file_info = []
        for file in files:
            file_path = os.path.join(FILE_FOLDER, file)
            size = os.path.getsize(file_path)
            file_info.append({'name': file, 'size': size})
        return jsonify(file_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/files/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(FILE_FOLDER, filename, as_attachment=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            file.save(os.path.join(FILE_FOLDER, file.filename))
            flash('文件上传成功！')  # 此处使用闪现消息，您可以在 HTML 中显示它
            return redirect('/')
        else:
            flash('无效的文件类型！')
            return redirect('/')

    flash('用户名或密码错误！')
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1206)
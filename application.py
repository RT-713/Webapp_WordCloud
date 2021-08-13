import os
from flask import Flask, render_template, request, redirect,url_for, flash, send_from_directory, session
# データベース関連のモジュール
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
# 自作関数のインポート
from upload_cloud import upload_cloud
from paste_cloud import paste_cloud


# Flaskをインスタンス化
app = Flask(__name__)

### データベース定義 ###
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///text_mining.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # dbの変更時に発せられる警告を非表示
db = SQLAlchemy(app)

# テーブルの設定：db.Modelを継承したクラスを作成
class text_mining(db.Model):
    # テーブル名
    __tablename__ = 'text_mining_tb'
    # テーブルのカラム設定
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True)
    file_path = db.Column(db.String(64))
    date = db.Column(db.DateTime, nullable=False, default=datetime.today())

# データベースの初期化
@app.cli.command('init_DB')
def initialize_DB():
    db.create_all()

# エラーハンドリング
@app.errorhandler(404)
def not_found(error):
    return '404 Not Found'

# TOP画面
@app.route('/')
def index():
    registration_data = text_mining.query.all()
    # secretKeyの設定とセッションの継続
    app.secret_key = os.urandom(20)
    session.get = True
    if session.get == True:
        return render_template('index.html', registration_data=registration_data)

# ファイルアップロード画面
@app.route('/upload')
def upload():
    return render_template('upload.html')

# アップロードされたファイルを取得＋テキストマイニングの実行
@app.route('/upload_register', methods=['POST'])
def upload_register():
    title = request.form['title']
    if title:
        file = request.files['file']
        file_path = secure_filename(file.filename)
        file_path = 'static/'  + file_path
        file.save(file_path)
        # 自作関数：upload_cloud()関数の実装
        result_path = upload_cloud(file_path)
        # データベースへの書き込み
        register_file = text_mining(title=title, file_path=result_path)
        db.session.add(register_file)
        db.session.commit()
        flash('ファイルの生成が完了しました')
        return redirect(url_for('index'))
    else:
        flash('タイトルを入力し，再度アップロードしてください')
        return redirect(url_for('index'))

# テキスト入力画面
@app.route('/paste')
def paste():
    return render_template('paste.html')
    
# 入力データを取得＋テキストマイニングの実行
@app.route('/paste_register', methods=['POST'])
def paste_register():
    title = request.form['title']
    if title:
        paste_data = request.form['paste_data']
        # 自作関数：paste_cloud()関数の実装
        result_path = paste_cloud(title, paste_data)
        # データベースへの書き込み
        register_file = text_mining(title=title, file_path=result_path)
        db.session.add(register_file)
        db.session.commit()
        flash('ファイルの生成が完了しました')
        return redirect(url_for('index'))
    else:
        flash('タイトルを入力し，再度アップロードしてください')
        return redirect(url_for('index'))

# ダウンロード機能
@app.route('/download/<file_path>', methods=['POST'])
def download(file_path):
    # 格納先ディレクトリ, ファイルのパス，ダウンロードボタンの挙動（Trueで押下するとダウンロード）
    return send_from_directory('static', file_path, as_attachment=True)

# 削除機能
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    delete_data = text_mining.query.get(id)
    delete_file = delete_data.file_path
    db.session.delete(delete_data)
    db.session.commit()
    os.remove('static/' + delete_file)
    flash('ファイルの削除が完了しました')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
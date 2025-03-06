from flask import Flask, request, make_response, render_template, redirect
from flask_socketio import SocketIO, emit
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Extensions
socketio = SocketIO(app)
db = SQLAlchemy(app)

# DBモデル
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)  # 投稿ID
    device_id = db.Column(db.String(100), nullable=False)  # 投稿者の一意ID
    content = db.Column(db.Text, nullable=False)  # 投稿内容
    timestamp = db.Column(db.DateTime, default=datetime.now)  # 投稿日時

# DB初期化
with app.app_context():
    db.create_all()

# Cookieに一意のIDを設定
@app.after_request
def assign_device_id(response):
    if 'device_id' not in request.cookies:
        unique_id = str(uuid.uuid4())
        response.set_cookie('device_id', unique_id)
    return response

# チャット制限ロジック
def enforce_chat_limit():
    max_chats = 100 # 最大件数
    post_count = Post.query.count()
    if post_count > max_chats:
        # 古い投稿を削除
        oldest_posts = Post.query.order_by(Post.timestamp.asc()).limit(post_count - max_chats).all()
        for post in oldest_posts:
            db.session.delete(post)
        db.session.commit()

# メインページ（掲示板）
@app.route('/', methods=['GET'])
def board():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('board.html', posts=posts)

# 投稿を受け取るルート
@app.route('/post', methods=['POST'])
def post_message():
    device_id = request.cookies.get('device_id')
    content = request.form.get('content')
    if content and device_id:
        new_post = Post(device_id=device_id, content=content)
        db.session.add(new_post)
        db.session.commit()
        # 最大件数を超えた場合、古いチャットを削除
        enforce_chat_limit()
        # 新しい投稿をSocketIOでクライアントに送信
        socketio.emit('new_message', {
            'content': content,
            'timestamp': new_post.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'device_id': device_id
        }, to=None)
    return redirect('/board')

# ソケットイベント：新しいメッセージを受信した場合
@socketio.on('new_message')
def handle_new_message(data):
    print("New message received: ", data)
    emit('message_received', data, to=None)  # すべてのクライアントに送信

# アプリ起動
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)

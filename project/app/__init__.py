from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config
from app.models import db, User, Product
import os
from werkzeug.security import generate_password_hash
mail = Mail()


def create_app():
    app = Flask(__name__)

    # 設定ファイルの読み込み
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = os.urandom(24)

    # データベースの初期化
    db.init_app(app)
    with app.app_context():
        db.create_all()

        # テストデータを挿入
        init_db()

    # ログインの初期化
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "/login"

    # user_loaderを設定
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # メールの設定
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'hewgroup040@gmail.com'
    app.config['MAIL_PASSWORD'] = 'dpqe vznv rglo aegn'  # アプリパスワードを使用
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_DEFAULT_SENDER'] = 'hewgroup040@gmail.com'
    mail.init_app(app)

    # ルーティングの設定
    from app.routes import bp
    app.register_blueprint(bp)

    return app

# テストデータ挿入の関数


def init_db():
    with db.session.begin():
        # Userデータの挿入
        if not User.query.filter_by(email='1@1').first():  # すでにユーザーが存在するか確認
            user = User(email='1@1', password=generate_password_hash(
                "1", method='pbkdf2:sha256'))
            db.session.add(user)

        # Productデータの挿入
        if not Product.query.filter_by(name='ちょっとワケあり？！濃厚モンブランケーキ').first():  
            apple = Product(name='ちょっとワケあり？！濃厚モンブランケーキ', sale_price=500, category="デザート", defect_reason = """贅沢な和栗をたっぷり使用したモンブランが、ちょっと規格外のお得価格で登場！形が崩れていたり、クリームの巻きが均一でなかったりするだけで、味は正規品とまったく同じ。むしろ、「形なんて気にしない！美味しければOK！」という方にはぴったりの一品です。

サクサクのメレンゲ土台に、なめらかな生クリームと濃厚なマロンクリームがたっぷり。栗の自然な甘さが口いっぱいに広がり、一口ごとに幸せを感じられます。ご自宅用のおやつに、ちょっと贅沢なティータイムにいかがでしょうか？

💡 こんな方におすすめ！
✔︎ 形がちょっと崩れてても気にしない！
✔︎  美味しいモンブランをお得に食べたい！
✔︎家族や友人と気軽に楽しみたい！""")
            db.session.add(apple)

        if not Product.query.filter_by(name='ワケありだけど、味は本格派！「もったいないポテトチップス」').first():  
            apple = Product(name='ワケありだけど、味は本格派！「もったいないポテトチップス」', sale_price=500, category="お菓子", defect_reason = """ちょっと形が不揃いだったり、サイズが小さかったりして規格外になったジャガイモを、美味しく有効活用！素材の味を活かしたポテトチップスに仕上げました。カリッとした食感とジャガイモの自然な甘み・旨みがたまらない、シンプルながら奥深い味わいです。

余計なものは加えず、塩・油・ジャガイモのみのシンプルレシピ。だからこそ、ジャガイモ本来の美味しさがダイレクトに楽しめます。食品ロス削減にも貢献できる、ちょっとエコなポテトチップスをぜひお試しください！

💡 こんな方におすすめ！
✔︎ お得に美味しいポテトチップスを楽しみたい！
✔︎ 素材の味をしっかり感じるシンプルな味が好き！
✔︎ 食品ロス削減に興味がある！

""")
            db.session.add(apple)
        if not Product.query.filter_by(name='見た目はちょっと不揃い！？「もったいないかまぼこ」').first():  
            apple = Product(name='見た目はちょっと不揃い！？「もったいないかまぼこ」', sale_price=500, category="加工品", defect_reason = """形が少し歪んでいたり、端っこが多かったりして規格外になったかまぼこを、美味しく有効活用！厳選した魚のすり身を使用し、ふんわりしながらもしっかり弾力のある食感に仕上げました。見た目はちょっとワイルドですが、味はいつものかまぼこと同じです！
            
そのまま食べても美味しいですが、おでんや炒め物、サラダの具材としてもぴったり！お得に美味しく、食品ロス削減にも貢献できる「もったいないかまぼこ」をぜひお試しください！

💡 こんな方におすすめ！
✔︎ 形が多少違っても気にしない！
✔︎ 美味しいかまぼこをお得に楽しみたい！
✔︎ 食品ロス削減に協力したい！
""")
            db.session.add(apple)
    if not Product.query.filter_by(name='見た目バラバラ？！「もったいない野菜チップス」').first():  
            apple = Product(name='見た目バラバラ？！「もったいない野菜チップス」', sale_price=500, category="お菓子", defect_reason = """ちょっと形が不揃いだったり、小さすぎたりして規格外になった野菜を、美味しくチップスに仕上げました！素材の味を活かし、添加物不使用＆ノンフライ製法でパリッと軽い食感に。野菜本来の甘みと旨みをぎゅっと凝縮しています。

サツマイモ、レンコン、ニンジン、ゴボウ、カボチャなど、色とりどりの野菜を使用。おやつやおつまみ、ヘルシースナックとして、家族みんなで楽しめます！食品ロス削減にもつながる、お得でエコなチップスをぜひお試しください。

💡 こんな方におすすめ！
✔︎ 形が違っても気にしない！
✔︎ ヘルシーなおやつを探している！
✔︎ 食品ロス削減に興味がある！
""")
            
            db.session.add(apple)

    if not Product.query.filter_by(name='ちょっとワケあり？！「もったいないフルーツジャム」').first():  
            apple = Product(name='ちょっとワケあり？！「もったいないフルーツジャム」', sale_price=500, category="加工品", defect_reason = """形が不揃いだったり、小さすぎたりして市場に出せなかったフルーツを、美味しいジャムにしました！味や香りは一級品なのに、見た目の理由だけで規格外になった果物たちを無駄なく活用。砂糖控えめ・無添加製法で、果実本来の甘みと酸味をぎゅっと凝縮しています。

トーストに塗るのはもちろん、ヨーグルトやパンケーキ、紅茶に入れるのもおすすめ！お得でエコな「もったいないフルーツジャム」をぜひお試しください♪

💡 こんな方におすすめ！
✔︎ フルーツの自然な甘さを楽しみたい！
✔︎ 添加物が少ないヘルシーなジャムを探している！
✔︎ 食品ロス削減に興味がある！
""")
            
            db.session.add(apple)

    if not Product.query.filter_by(name='見た目がちょっとワケあり？！「もったいないトマト缶」').first():  
            apple = Product(name='見た目がちょっとワケあり？！「もったいないトマト缶」', sale_price=500, category="加工品", defect_reason = """サイズがバラバラだったり、形が少し歪んでいたりして市場に出せなかった完熟トマトを、美味しいトマト缶にしました！味や栄養価は正規品と変わらず、イタリア産・国産の厳選トマトを100%使用。添加物は一切使わず、トマトの旨みをそのまま閉じ込めています。

パスタソースやスープ、煮込み料理にぴったり！食品ロス削減にもつながる、お得でエコな「もったいないトマト缶」をぜひお試しください♪

💡 こんな方におすすめ！
✔︎ 規格外でも美味しいトマトを楽しみたい！
✔︎ 料理に使うなら見た目は気にしない！
✔︎ 食品ロス削減に貢献したい！
""")
            
            db.session.add(apple)



    if not Product.query.filter_by(name='見た目バラバラ！？「もったいないドライフルーツ」').first():  
            apple = Product(name='見た目バラバラ！？「もったいないドライフルーツ」', sale_price=500, category="デザート", defect_reason = """形が不揃いだったり、サイズが小さかったりして規格外になったフルーツを、美味しくドライフルーツにしました！砂糖・添加物不使用で、果物本来の甘みと香りをギュッと凝縮。噛むたびに自然な甘さが広がる、ヘルシーで栄養満点なおやつです。

マンゴー、イチゴ、バナナ、パイナップル、リンゴなど、さまざまなフルーツが入っているので、食べ比べも楽しい！そのまま食べるのはもちろん、ヨーグルトに入れたり、紅茶に浮かべたりするのもおすすめです。

💡 こんな方におすすめ！
✔︎ 形がバラバラでも気にしない！
✔︎ 自然の甘さを楽しみたい！
✔︎ 食品ロス削減に貢献したい！

""")
            
            db.session.add(apple)


    if not Product.query.filter_by(name='見た目はワケあり！？「もったいない野菜ジュース」').first():  
            apple = Product(name='見た目はワケあり！？「もったいない野菜ジュース」', sale_price=500, category="飲み物", defect_reason = """形がちょっと歪んでいたり、大きさがバラバラだったりして市場に出せなかった規格外の野菜を、栄養たっぷりのジュースにしました！厳選したトマト、ニンジン、ホウレンソウ、セロリ、カボチャなどを使用し、砂糖・保存料・着色料は一切不使用。野菜本来の甘みと旨みをぎゅっと凝縮しています。

毎日の健康習慣にぴったりな「もったいない野菜ジュース」、美味しく飲んで食品ロス削減にも貢献しませんか？

💡 こんな方におすすめ！
✔︎ 野菜不足を手軽に補いたい！
✔︎ 無添加のナチュラルなジュースを探している！
✔︎ 食品ロス削減に興味がある！
""")
            
            db.session.add(apple)


    if not Product.query.filter_by(name='ちょっとワケあり！？「もったいないピーナッツバター」').first():  
            apple = Product(name='ちょっとワケあり！？「もったいないピーナッツバター」', sale_price=500, category="加工品", defect_reason = """サイズが小さかったり、形が不揃いだったりして市場に出せなかった規格外ピーナッツを100％使用！余計な添加物を使わず、砂糖・保存料不使用でピーナッツ本来の香ばしさと濃厚なコクをそのまま楽しめるピーナッツバターに仕上げました。

滑らかなスムースタイプと、ゴロゴロ食感が楽しいクランチタイプをご用意。パンに塗るのはもちろん、スムージーやお菓子作り、料理のコク出しにもぴったり！食品ロス削減にもつながる「もったいないピーナッツバター」、ぜひお試しください♪

💡 こんな方におすすめ！
✔︎ シンプルでピーナッツの味を楽しみたい！
✔︎ 無添加で安心して食べられるピーナッツバターを探している！
✔︎ 食品ロス削減に貢献したい！

""")
            
            db.session.add(apple)

    if not Product.query.filter_by(name='見た目はちょっとワケあり？！「もったいなたくあん」').first():  
            apple = Product(name='見た目はちょっとワケあり？！「もったいなたくあん」', sale_price=500, category="加工品", defect_reason = """形が不揃いだったり、皮が少し傷ついていたりして市場に出せなかった大根を使用した、お得で美味しいたくあんです。手間暇かけて、昔ながらの製法でじっくり漬け込み、無添加・自然発酵で仕上げました。

シャキシャキとした歯ごたえと、ほどよい塩味・甘味が絶妙に絡み合い、ご飯のお供やおつまみにぴったり！少し傷がついているだけで捨てられるのはもったいない、大根本来の旨味がぎゅっと詰まった「もったいなたくあん」をぜひお試しください♪

💡 こんな方におすすめ！
✔︎ お得に美味しいたくあんを楽しみたい！
✔︎ 伝統的な製法で作られたたくあんが好き！
✔︎ 食品ロス削減に貢献したい！
""")
            
            db.session.add(apple)







        # 変更をコミットしてデータを保存
    db.session.commit()

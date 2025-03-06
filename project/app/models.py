from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# Flask-SQLAlchemyを初期化
db = SQLAlchemy()

# ユーザーテーブル（Flask-Login用）


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(25), nullable=False)
    name = db.Column(db.String(50), nullable=True)
    post = db.Column(db.String(), nullable=True)
    ken = db.Column(db.String(10), nullable=True)
    siku = db.Column(db.String(10), nullable=True)
    tyo = db.Column(db.String(10), nullable=True)
    ban = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)


# 商品テーブル
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    defect_reason = db.Column(db.String(1000))
    purchase_price = db.Column(db.Float, nullable=True)
    sale_price = db.Column(db.Float, nullable=True)
    status = db.Column(db.Enum("available", "not_available",
                       name="product_status"), default="available")

# 在庫テーブル


class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)  # 数量

# 販売テーブル


class Sale(db.Model):
    __tablename__ = 'sale'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sale_date = db.Column(db.DateTime, default=datetime.now())
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

# 寄付テーブル


class Donation(db.Model):
    __tablename__ = 'donations'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey(
        'donation_recipients.id'), nullable=False)
    donation_date = db.Column(db.Date, default=datetime.now())
    quantity = db.Column(db.Integer, nullable=False)

# 寄付先テーブル


class DonationRecipient(db.Model):
    __tablename__ = 'donation_recipients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)

# 問い合わせテーブル


class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    text = db.Column(db.Text)

#レビューてーｂ

class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    name = db.Column(db.String(50))
    star = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100))
    describe = db.Column(db.Text, nullable=False)
    review_date = db.Column(db.DateTime, default=datetime.now())

class Fcat(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    flute = db.Column(db.Integer)    

# リレーション設定


Product.inventories = db.relationship("Inventory", backref="product")
Product.sales = db.relationship("Sale", backref="product")
Product.donations = db.relationship("Donation", backref="product")

Donation.recipient = db.relationship("DonationRecipient", backref="donations")
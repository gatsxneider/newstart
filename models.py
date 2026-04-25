from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, default="정보시스템 수석감리원")
    title = db.Column(db.String(120), nullable=False, default="정보시스템 수석감리원 / 前 정보보호 전문가")
    bio = db.Column(db.Text, nullable=True, default="안녕하세요, IT 인프라와 보안의 핵심을 짚어내는 수석감리원입니다. 취미는 바이브코딩입니다.")
    photo_filename = db.Column(db.String(120), nullable=True, default="default_profile.png")

class Career(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.String(20), nullable=False)
    end_date = db.Column(db.String(20), nullable=True) # None means present
    description = db.Column(db.Text, nullable=True)

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    issuer = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(20), nullable=False)

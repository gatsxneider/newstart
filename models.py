from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# SQLAlchemy 객체 초기화
db = SQLAlchemy()

class User(db.Model):
    """
    관리자 계정 정보를 저장하는 모델
    보안: 비밀번호는 평문이 아닌 해시(Hash)된 값으로만 저장되어 DB 유출 시에도 안전합니다.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        """비밀번호를 단방향 암호화(PBKDF2/Bcrypt)하여 저장하는 함수"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """사용자가 입력한 비밀번호와 DB의 해시값을 비교 검증하는 함수"""
        return check_password_hash(self.password_hash, password)

class Profile(db.Model):
    """
    수석감리원님의 기본 프로필 정보를 저장하는 모델
    단일 인스턴스만 사용되어 홈 화면에 정보를 제공합니다.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, default="정보시스템 수석감리원")
    title = db.Column(db.String(120), nullable=False, default="정보시스템 수석감리원 / 前 정보보호 전문가")
    bio = db.Column(db.Text, nullable=True, default="안녕하세요, IT 인프라와 보안의 핵심을 짚어내는 수석감리원입니다. 취미는 바이브코딩입니다.")
    photo_filename = db.Column(db.String(120), nullable=True, default="default_profile.png")

class Career(db.Model):
    """
    경력 이력을 저장하는 모델
    타임라인 형태로 메인 페이지에 표시됩니다.
    """
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(120), nullable=False) # 회사 또는 기관명
    role = db.Column(db.String(120), nullable=False)    # 직급 또는 역할
    start_date = db.Column(db.String(20), nullable=False) # 시작일 (예: 2020.03)
    end_date = db.Column(db.String(20), nullable=True)    # 종료일 (None이면 '현재'로 표시)
    description = db.Column(db.Text, nullable=True)       # 주요 업무 내용 상세 설명

class Certificate(db.Model):
    """
    보유 자격증 이력을 저장하는 모델
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)   # 자격증명 (예: 정보시스템 감리원)
    issuer = db.Column(db.String(120), nullable=False) # 발급기관 (예: 한국지능정보사회진흥원)
    date = db.Column(db.String(20), nullable=False)    # 취득일자

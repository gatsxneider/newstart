import os
import secrets
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from models import db, User, Profile, Career, Certificate
from auth import auth_bp
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

# [보안 설정] 세션 서명 등을 위한 암호화 키. 매 실행 시 무작위 생성되어 탈취가 어렵습니다.
app.secret_key = secrets.token_hex(16)

# [데이터베이스 설정] 파일 기반의 경량 DB인 SQLite를 사용합니다.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# [파일 업로드 설정]
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# [보안 설정] 16MB로 업로드 용량 제한 (대용량 파일로 인한 서비스 거부 공격/DDoS 방지)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

# [보안 설정] CSRF(Cross-Site Request Forgery) 보호 활성화. 모든 POST 요청에 토큰 검증을 강제합니다.
csrf = CSRFProtect(app)

# DB 객체 및 Blueprint(인증 모듈) 등록
db.init_app(app)
app.register_blueprint(auth_bp)

# [보안 설정] 쿠키 및 세션 하이재킹 방어 설정
app.config.update(
    SESSION_COOKIE_HTTPONLY=True, # 자바스크립트를 통한 세션 탈취 방지 (XSS 방어의 연장)
    SESSION_COOKIE_SAMESITE='Lax', # 타 사이트에서의 요청 시 세션 쿠키 전송 제한 (CSRF 방어의 연장)
)

def allowed_file(filename):
    """
    [보안 검증] 업로드된 파일의 확장자가 허용된 이미지 타입인지 검사합니다.
    실행 파일(.exe, .sh)이나 악성 스크립트 업로드를 원천 차단합니다.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.before_request
def setup_db():
    """
    서버 구동 후 최초 요청 시 실행되는 초기화 로직.
    DB 테이블과 업로드 폴더, 그리고 초기 관리자 계정을 생성합니다.
    """
    if not hasattr(app, 'db_initialized'):
        # 파일 저장용 디렉토리 생성
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        with app.app_context():
            db.create_all() # 선언된 모든 스키마(Model)를 DB에 반영
            if not User.query.first():
                # 초기 관리자 계정 생성 (기본값)
                admin_pw = 'admin123!'
                admin = User(username='admin')
                admin.set_password(admin_pw) # 단방향 해시 적용
                db.session.add(admin)
                db.session.commit()
                print(f"[*] 초기 관리자 계정이 생성되었습니다. ID: admin / PW: {admin_pw}")
            
            if not Profile.query.first():
                profile = Profile()
                db.session.add(profile)
                db.session.commit()
        app.db_initialized = True

@app.route('/')
def index():
    """메인 화면(홈) 라우트. 등록된 프로필, 경력, 자격증을 DB에서 불러와 렌더링합니다."""
    profile = Profile.query.first()
    careers = Career.query.order_by(Career.start_date.desc()).all()
    certificates = Certificate.query.order_by(Certificate.date.desc()).all()
    return render_template('index.html', profile=profile, careers=careers, certificates=certificates)

@app.route('/admin', methods=['GET'])
def admin_dashboard():
    """관리자 대시보드 화면. 로그인된 세션이 없을 경우 접근을 차단하고 로그인 페이지로 돌려보냅니다."""
    if 'admin_id' not in session:
        return redirect(url_for('auth.login'))
    
    profile = Profile.query.first()
    careers = Career.query.order_by(Career.start_date.desc()).all()
    certificates = Certificate.query.order_by(Certificate.date.desc()).all()
    return render_template('admin.html', profile=profile, careers=careers, certificates=certificates)

@app.route('/admin/profile', methods=['POST'])
def update_profile():
    """
    프로필 및 사진 변경 라우트.
    파일 시스템 접근 공격(Directory Traversal)을 막기 위한 secure_filename 처리를 포함합니다.
    """
    if 'admin_id' not in session:
        return redirect(url_for('auth.login'))
    
    profile = Profile.query.first()
    profile.name = request.form.get('name')
    profile.title = request.form.get('title')
    profile.bio = request.form.get('bio')
    
    # 이미지 업로드 처리 로직
    if 'photo' in request.files:
        file = request.files['photo']
        if file and file.filename != '' and allowed_file(file.filename):
            # [보안] 파일명에서 악의적인 경로(../ 등)를 제거합니다.
            filename = secure_filename(file.filename)
            # [보안] 고유한 난수를 덧붙여 파일 덮어쓰기 방지 및 파일명 난독화 효과를 줍니다.
            unique_filename = secrets.token_hex(8) + "_" + filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
            profile.photo_filename = unique_filename
            
    db.session.commit()
    flash('프로필이 업데이트 되었습니다.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/career', methods=['POST'])
def add_career():
    """새로운 경력 정보를 DB에 추가합니다."""
    if 'admin_id' not in session: return redirect(url_for('auth.login'))
    career = Career(
        company=request.form.get('company'),
        role=request.form.get('role'),
        start_date=request.form.get('start_date'),
        end_date=request.form.get('end_date'),
        description=request.form.get('description')
    )
    db.session.add(career)
    db.session.commit()
    flash('경력이 추가되었습니다.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/career/<int:id>/delete', methods=['POST'])
def delete_career(id):
    """특정 경력 정보를 DB에서 삭제합니다. (ID 값 사용)"""
    if 'admin_id' not in session: return redirect(url_for('auth.login'))
    career = Career.query.get_or_404(id) # 데이터가 존재하지 않을 경우 404 에러 반환
    db.session.delete(career)
    db.session.commit()
    flash('경력이 삭제되었습니다.', 'info')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/certificate', methods=['POST'])
def add_certificate():
    """새로운 자격증 정보를 DB에 추가합니다."""
    if 'admin_id' not in session: return redirect(url_for('auth.login'))
    cert = Certificate(
        name=request.form.get('name'),
        issuer=request.form.get('issuer'),
        date=request.form.get('date')
    )
    db.session.add(cert)
    db.session.commit()
    flash('자격증이 추가되었습니다.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/certificate/<int:id>/delete', methods=['POST'])
def delete_certificate(id):
    """특정 자격증 정보를 DB에서 삭제합니다."""
    if 'admin_id' not in session: return redirect(url_for('auth.login'))
    cert = Certificate.query.get_or_404(id)
    db.session.delete(cert)
    db.session.commit()
    flash('자격증이 삭제되었습니다.', 'info')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    # 개발 서버 실행 (운영 시에는 gunicorn 등의 WSGI 서버 사용 권장)
    app.run(debug=True, port=5000)

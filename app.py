import os
import secrets
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from models import db, User, Profile, Career, Certificate
from auth import auth_bp
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
# 보안: 무작위 비밀키 생성
app.secret_key = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 파일 업로드 설정
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# 보안: 16MB로 업로드 제한 확장 (사진 용량이 큰 경우 대비)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

# CSRF 보호 활성화
csrf = CSRFProtect(app)

db.init_app(app)
app.register_blueprint(auth_bp)

# 세션 보안 설정
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.before_request
def setup_db():
    if not hasattr(app, 'db_initialized'):
        # static/uploads 폴더 생성
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        with app.app_context():
            db.create_all()
            if not User.query.first():
                # 초기 관리자 생성
                admin_pw = 'admin123!'
                admin = User(username='admin')
                admin.set_password(admin_pw)
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
    profile = Profile.query.first()
    careers = Career.query.order_by(Career.start_date.desc()).all()
    certificates = Certificate.query.order_by(Certificate.date.desc()).all()
    return render_template('index.html', profile=profile, careers=careers, certificates=certificates)

@app.route('/admin', methods=['GET'])
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('auth.login'))
    profile = Profile.query.first()
    careers = Career.query.order_by(Career.start_date.desc()).all()
    certificates = Certificate.query.order_by(Certificate.date.desc()).all()
    return render_template('admin.html', profile=profile, careers=careers, certificates=certificates)

@app.route('/admin/profile', methods=['POST'])
def update_profile():
    if 'admin_id' not in session:
        return redirect(url_for('auth.login'))
    
    profile = Profile.query.first()
    profile.name = request.form.get('name')
    profile.title = request.form.get('title')
    profile.bio = request.form.get('bio')
    
    # 이미지 업로드 처리
    if 'photo' in request.files:
        file = request.files['photo']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 고유한 파일명 생성
            unique_filename = secrets.token_hex(8) + "_" + filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
            profile.photo_filename = unique_filename
            
    db.session.commit()
    flash('프로필이 업데이트 되었습니다.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/career', methods=['POST'])
def add_career():
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
    if 'admin_id' not in session: return redirect(url_for('auth.login'))
    career = Career.query.get_or_404(id)
    db.session.delete(career)
    db.session.commit()
    flash('경력이 삭제되었습니다.', 'info')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/certificate', methods=['POST'])
def add_certificate():
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
    if 'admin_id' not in session: return redirect(url_for('auth.login'))
    cert = Certificate.query.get_or_404(id)
    db.session.delete(cert)
    db.session.commit()
    flash('자격증이 삭제되었습니다.', 'info')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)

from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import check_password_hash
from models import db, User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

# 라우팅을 모듈화하기 위한 Blueprint 객체 생성
auth_bp = Blueprint('auth', __name__)

class LoginForm(FlaskForm):
    """
    WTForms를 활용한 로그인 폼 클래스
    보안: 렌더링 시 자동으로 CSRF 토큰 필드가 생성되어 Cross-Site Request Forgery 공격을 방어합니다.
    """
    username = StringField('아이디', validators=[DataRequired()])
    password = PasswordField('비밀번호', validators=[DataRequired()])
    submit = SubmitField('로그인')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    관리자 로그인 라우트
    GET 요청 시 로그인 화면을 렌더링하고, POST 요청 시 자격 증명을 검증합니다.
    """
    # 이미 로그인된 상태라면 관리자 대시보드로 리다이렉트
    if 'admin_id' in session:
        return redirect(url_for('admin_dashboard'))
    
    form = LoginForm()
    
    # POST 요청이고 CSRF 토큰 및 데이터 검증(Validation)이 통과되었을 때
    if form.validate_on_submit():
        # DB에서 해당 아이디의 사용자 조회 (SQL Injection 방어 처리됨)
        user = User.query.filter_by(username=form.username.data).first()
        
        # 사용자가 존재하고 비밀번호 해시값이 일치하는 경우
        if user and user.check_password(form.password.data):
            # 세션에 고유 식별자 저장 (세션 하이재킹 대비 속성은 app.py에 설정됨)
            session['admin_id'] = user.id
            flash('관리자 로그인에 성공했습니다.', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            # 보안: 존재하지 않는 아이디인지 틀린 비밀번호인지 구체적으로 알려주지 않아 계정 유추(Enumeration) 방지
            flash('아이디 또는 비밀번호가 올바르지 않습니다.', 'danger')
            
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
def logout():
    """
    로그아웃 라우트
    세션에서 인증 정보를 제거하여 접근 권한을 안전하게 회수합니다.
    """
    session.pop('admin_id', None)
    flash('로그아웃 되었습니다.', 'info')
    return redirect(url_for('index'))

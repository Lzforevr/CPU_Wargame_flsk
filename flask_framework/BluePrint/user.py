# 先引入软件包
import random
import string

from flask import Blueprint, request, jsonify, session
from flask import render_template, redirect, url_for
# 以下用于邮箱验证码
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash

from exts import mail, db
from forms import RegisterForm, LoginForm
from model import User_data, Captcha_data

# 再定义蓝图对象实例，分别设置蓝图名称，网址前缀
bp = Blueprint("user", __name__, url_prefix='/user')


@bp.route('/')
def Main():
    return 'OK'


@bp.route('/register',methods=["GET","POST"])
def Register():
    # get请求直接访问js页面
    if request.method == 'GET':
        return render_template('register.html')
    else:
        form = RegisterForm(request.form.get('register-form',default='0'))

        if form.validate():
            # 从wtforms中取对应值赋值给类中的对象，再用类存储添加到数据库
            mail = form.email.data
            username = form.username.data
            password = form.password.data
            # 加密
            user = User_data(email=mail, username=username, pwd=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            # 注意url_for使用的参数是函数名称，而非地址
            print('注册成功！')
            return redirect(url_for('user.Login'))
        else:
            print(form.errors)
            return redirect(url_for('user.Register'))


@bp.route('/login',methods=['GET','POST'])
def Login():
    if request.method== 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form['login-form'])
        if form.validate():
            username = form.username.data
            password = form.password.data
            user = User_data.query.filter_by(username=username).first()
            if not user:
                print('用户不存在')
                return redirect(url_for('user.Login'))
            elif check_password_hash(user.pwd,password):
                print('登录成功')
                # 设置session加密储存登录状态到cookie里（再次访问域名时，会保持登录状态）
                session['user_id'] = user.id
                return redirect(url_for('main.Games'))

            else:
                print('密码错误')
                return redirect(url_for('user.Login'))

# 在js文件中点击“获取验证码”button后设置action属性为该函数路由，即可执行
@bp.route('/send_captcha',methods=['POST'])
def Send_captcha():
    form = request.form['email']
    # 选择4/6位数字，digits=‘0123456789’
    str = string.digits * 4
    captcha = random.sample(str, 4)
    # 将验证码转换为字符串形式
    captcha = ''.join(captcha)
    message = Message(subject='CPU_WarGame验证码', recipients=[form], body=f'您的验证码是：{captcha}')
    mail.send(message)
    # 将验证码上传服务器，使用memcached/redis缓存
    # 或用数据库表的方式存储（权宜之计，速度慢）
    email_captcha = Captcha_data(email=form, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    # 测试时在导航栏输入？mail=qq邮箱即可，在终端输出验证码
    # 若验证成功
    return jsonify({"code": 200, "message": '输入成功', 'data': None})
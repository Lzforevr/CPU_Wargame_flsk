from flask import Flask
# g用于作为全局变量
from flask import Flask, session, g, render_template
from exts import db, mail  # 从扩展中导入对象
from BluePrint.user import bp as user_bp
from flask_migrate import Migrate
import configs
app = Flask(__name__)

#  绑定配置文件
app.config.from_object(configs)
#  绑定db\mail扩展
db.init_app(app)
mail.init_app(app)
#  绑定blueprint中的对象
app.register_blueprint(user_bp)
# 数据库迁移
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()
@app.route('/')
def hello_world():
    return render_template('')


if __name__ == '__main__':
    app.run()

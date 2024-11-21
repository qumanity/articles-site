from flask import Flask, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Модели пользователей
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Статический пользователь для тестирования
users = {'admin': {'password': 'password'}}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Модель статьи
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Article('{self.title}', '{self.content[:20]}')"

# Создание админки
class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 'admin'

admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
admin.add_view(AdminView(Article, db.session))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect('/admin')
        else:
            return 'Неверные учетные данные', 401
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

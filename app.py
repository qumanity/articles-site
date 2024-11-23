from flask import Flask, render_template, redirect, url_for, request, flash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Строка подключения к базе данных SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключаем отслеживание изменений в базе данных

db = SQLAlchemy(app)

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Функция для загрузки пользователя
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Модели базы данных
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Article('{self.title}', '{self.content[:20]}')"

# Форма для статьи
class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Save')

# Форма для логина
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Админка
class ArticleView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated  # Проверяем, вошел ли пользователь

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/login')  # Перенаправляем на страницу логина, если пользователь не авторизован

# Регистрация админки
admin = Admin(app, name='Admin Panel', template_mode='bootstrap4')
admin.add_view(ArticleView(Article, db.session))  # Подключаем модель статьи в админке

# Главная страница для логина
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect('/admin')  # После успешного логина перенаправляем в админку
        else:
            flash('Invalid credentials')  # Если логин или пароль неверные
    return render_template('login.html', form=form)

# Выход из системы
@app.route('/logout')
@login_required
def logout():
    logout_user()  # Выход из текущей сессии
    return redirect('/')

# Страница со списком статей
@app.route('/articles')
def articles():
    articles = Article.query.all()  # Получаем все статьи
    return render_template('articles.html', articles=articles)

# Страница для редактирования статьи
@app.route('/articles/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = Article.query.get_or_404(article_id)  # Получаем статью по ID
    form = ArticleForm(obj=article)
    if form.validate_on_submit():
        article.title = form.title.data  # Обновляем заголовок
        article.content = form.content.data  # Обновляем содержание
        db.session.commit()  # Сохраняем изменения в базе данных
        flash('Article updated successfully!')  # Сообщение об успешном обновлении
        return redirect(url_for('articles'))  # Перенаправляем на страницу списка статей
    return render_template('edit_article.html', form=form, article=article)

# Создание базы данных и таблиц, если они еще не существуют
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

from flask import Flask, render_template, redirect
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Модели пользователей
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

# Статья
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Article('{self.title}', '{self.content[:20]}')"

# Форма для редактирования статьи с CKEditor
class ArticleForm(FlaskForm):
    title = StringField('Title')
    content = TextAreaField('Content')

# Интеграция CKEditor в форму через админку
class ArticleView(ModelView):
    form = ArticleForm

    # Подключаем CKEditor в форме
    def on_model_change(self, form, model, is_created):
        model.content = form.content.data

    def _get_extra_css(self):
        return super()._get_extra_css() + """
        <link rel="stylesheet" href="https://cdn.ckeditor.com/ckeditor5/34.2.0/classic/theme.css">
        """

    def _get_extra_js(self):
        return super()._get_extra_js() + """
        <script src="https://cdn.ckeditor.com/ckeditor5/34.2.0/classic/ckeditor.js"></script>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                ClassicEditor
                    .create(document.querySelector('#content'))
                    .catch(error => {
                        console.error(error);
                    });
            });
        </script>
        """

admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
admin.add_view(ArticleView(Article, db.session))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Логика для логина (пока простая)
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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

# Статический список статей для примера
articles = [
    {"id": 1, "title": "Первая статья", "content": "Контент первой статьи."},
    {"id": 2, "title": "Вторая статья", "content": "Контент второй статьи."}
]

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('admin'))
        else:
            return 'Неверные учетные данные', 401
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html', articles=articles)

@app.route('/article/<int:article_id>')
def article(article_id):
    article = next((a for a in articles if a["id"] == article_id), None)
    if article is None:
        return "Статья не найдена", 404
    return render_template('article.html', article=article)

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_article = {"id": len(articles) + 1, "title": title, "content": content}
        articles.append(new_article)
        return redirect(url_for('admin'))
    return render_template('admin.html', articles=articles)

@app.route('/admin/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = next((a for a in articles if a["id"] == article_id), None)
    if not article:
        return "Статья не найдена", 404

    if request.method == 'POST':
        article['title'] = request.form['title']
        article['content'] = request.form['content']
        return redirect(url_for('admin'))

    return render_template('edit_article.html', article=article)

@app.route('/admin/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    global articles
    articles = [a for a in articles if a["id"] != article_id]
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)


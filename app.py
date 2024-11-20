
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

articles = [
    {"id": 1, "title": "Список руководства модерации", "content":
    print("Руководитель модерации - https://vk.com/sakaromeow")
    print("Зам.Руководителя модерации - https://vk.com/drozdvk")
    print("Зам.Руководителя модерации - https://vk.com/mahch29")
    print("Зам.Руководителя модерации - https://vk.com/surpwhitewaves")
    print("Главный модератор - https://vk.com/mayson2007")
    print("Зам.Главного модератора - https://vk.com/n.ivanov.official")
    print("Зам.Главного модератора - https://vk.com/kl_llli")
    print("Куратор модерации - https://vk.com/motvot314")},
    {"id": 2, "title": "Вторая статья", "content": "Это контент второй статьи."},
]

@app.route('/')
def index():
    return render_template('index.html', articles=articles)

@app.route('/article/<int:article_id>')
def article(article_id):
    article = next((a for a in articles if a["id"] == article_id), None)
    return render_template('article.html', article=article)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_article = {"id": len(articles) + 1, "title": title, "content": content}
        articles.append(new_article)
        return redirect(url_for('index'))
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)

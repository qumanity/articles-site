from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Список статей с использованием переносов строк (\n)
articles = [
    {
        "id": 1,
        "title": "Список руководства модерации",
        "content": """Руководитель модерации - https://vk.com/sakaromeow
Зам.Руководителя модерации - https://vk.com/drozdvk
Зам.Руководителя модерации - https://vk.com/mahch29
Зам.Руководителя модерации - https://vk.com/surphwhitewaves
Главный модератор - https://vk.com/mayson2007
Зам.Главного модератора - https://vk.com/n.ivanov.official
Зам.Главного модератора - https://vk.com/kl_llli
Куратор модерации - https://vk.com/motvot314"""
    },
    {
        "id": 2,
        "title": "Вторая статья",
        "content": "Это контент второй статьи.\nДополнительная строка контента второй статьи."
    }
]

@app.route('/')
def index():
    return render_template('index.html', articles=articles)

@app.route('/article/<int:article_id>')
def article(article_id):
    # Поиск статьи по ID
    article = next((a for a in articles if a["id"] == article_id), None)
    if article is None:
        return "Article not found", 404
    return render_template('article.html', article=article)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title or not content:
            return "Both title and content are required", 400
        new_article = {"id": len(articles) + 1, "title": title, "content": content}
        articles.append(new_article)
        return redirect(url_for('index'))
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)

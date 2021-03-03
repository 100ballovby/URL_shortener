from flask import Flask, render_template, url_for, redirect, flash, request
from hashids import *
import sqlite3


def connect_to_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)
app.config['SECRET_KEY'] = 'try-to-guess'
hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])
# 3 hash-> t5,D | salt -> tY4nj, = j,tY5nt,D4


@app.route('/', methods=['GET', 'POST'])
def index():
    conn = connect_to_db()  # подключаемся к БД
    if request.method == 'POST': # если форму отправили
        url = request.form['url']

        if not url:  # если нам не передали url
            flash('The URL is required!', 'danger')
            return redirect(url_for('index'))

        url_data = conn.execute('INSERT INTO urls (original_url) VALUES (?)', (url,))
        # вставить url в базу

        conn.commit()  # подтвердить изменения
        conn.close()  # закрыть подключение к БД

        url_id = url_data.lastrowid  # получаем url из БД
        hashid = hashids.encode(url_id)  # хэшируем url
        short_url = request.host_url + hashid

        return render_template('index.html', s_url=short_url)
    return render_template('index.html')


@app.route('/<id>')
def url_redirect(id):
    conn = connect_to_db()
    original = hashids.decode(id)

    if original:
        or_id = original[0]
        url_data = conn.execute('SELECT original_url FROM urls WHERE id = (?)',
                                (or_id,)).fetchone()
        or_url = url_data['original_url']
        clicks = url_data['clicks']

        conn.execute('UPDATE urls SET clicks = ? WHERE id = ?',
                     (clicks + 1, or_id))
        conn.commit()
        conn.close()
        return redirect(or_url)
    else:
        flash('Invalid URL', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
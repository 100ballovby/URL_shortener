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




from flask import Flask, render_template, request, flash, redirect, url_for
from sqlalchemy import create_engine, text, inspect

app = Flask(__name__)
app.secret_key = 'your_secret_key'

conn_str = 'mysql://root:cset155@localhost/examdb'
engine = create_engine(conn_str, echo=False)
conn = engine.connect()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        if errorDetect():
            return redirect(url_for('sign_up'))
        # conn.execute(text('INSERT INTO account VALUES (:acc_id, :role, :name, :email, :password)', request.form))
        # conn.commit
        return render_template('base.html')
    return render_template('index.html')
@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        if errorDetect():
            return redirect(url_for('sign_in'))
        return render_template('base.html')
    return render_template('sign_in.html')



def errorDetect():
    check = False
    if request.form['role'] and request.form['role'] == 'null':
        flash('Invalid role selected. Please try again.', 'error')
        check = True
    if request.form['name'] and len(request.form['name']) < 1:
        flash('No name entered. Please try again.', 'error')
        check = True
    if request.form['email'] and '@' not in request.form['email'] or '.edu' not in request.form['email']:
        flash('Invalid email type, email must end in \'.edu\'. Please try again.', 'error')
        check = True
    if request.form['username'] and len(request.form['username']) < 1:
        flash('No username entered. Please try again.', 'error')
        check = True
    if request.form['password'] and len(request.form['password']) != 8:
        flash('Invalid password, length must be 8 characters. Please try again.', 'error')
        check = True
    return check


if __name__ == '__main__':
    app.run(debug=True)
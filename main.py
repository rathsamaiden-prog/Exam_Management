from flask import Flask, render_template, request
from sqlalchemy import create_engine, text, inspect

app = Flask(__name__)

conn_str = 'mysql://root:cset155@localhost/examdb'
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        return
    else:
        return

if __name__ == '__main__':
    app.run(debug=True)
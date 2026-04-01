from flask import Flask, render_template, request, flash, redirect, url_for, session
from sqlalchemy import create_engine, text

app = Flask(__name__)
app.secret_key = 'your_secret_key'

conn_str = 'mysql://root:cset155@localhost/examdb'
engine = create_engine(conn_str, echo=False)
conn = engine.connect()

# ----------- LOG IN / SIGN IN ---------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        if errorDetect():
            return redirect(url_for('sign_up'))
        conn.execute(text('INSERT INTO account (role, name, email, password) VALUES (:role, :name, :email, :password)'), request.form)
        conn.commit()
        if request.form['role'] == 'student':
            return redirect(url_for('student_page'))
        else:
            return redirect(url_for('teacher_page'))
    return render_template('index.html')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        if errorDetect():
            return redirect(url_for('sign_in'))
        user = conn.execute(text('SELECT * FROM account WHERE email = :email AND password = :password'), request.form).fetchone()
        try: 
            if user.acc_id is not None:
                session['user_id'] = user.acc_id
                session['role'] = user.role
            if session.get('role') == 'student':
                return redirect(url_for('student_page'))
            else:
                return redirect(url_for('teacher_page'))
        except BaseException:
            flash('Invalid or non-existent credentials. Please try again.', 'errror')
            return redirect(url_for('sign_in'))
    return render_template('sign_in.html')


def errorDetect():
    check = False
    try:
        if request.form['role'] == 'null':
            flash('Invalid role selected. Please try again.', 'error')
            check = True
        if len(request.form['name']) < 1:
            flash('No name entered. Please try again.', 'error')
            check = True
        if '@' not in request.form['email'] or '.edu' not in request.form['email']:
            flash('Invalid email type, email must end in \'.edu\'. Please try again.', 'error')
            check = True
    except BaseException:
        print('')
    if len(request.form['password']) != 8:
        flash('Invalid password, length must be 8 characters. Please try again.', 'error')
        check = True
    return check

# --------------- TEACHER PAGE AND FUNCS -------------------
@app.route('/teacher_page')
def teacher_page():
    test_page_tb = conn.execute(text('SELECT ' \
                                        't.test_id,'\
                                        't.title,' \
                                        'COUNT(q.question_id) AS question_count,' \
                                        'a.name AS creator_name ' \
                                    'FROM test t ' \
                                    'JOIN account a ON t.created_by = a.acc_id ' \
                                    'LEFT JOIN question q ON t.test_id = q.test_id ' \
                                    'GROUP BY t.test_id, t.title, a.name;'))
    return render_template('teacher_main.html', test_page_tb=test_page_tb)

@app.route('/edit_test_page/<int:test_id>', methods=['GET','POST'])
def edit_test(test_id):
    test_title = conn.execute(text('SELECT title FROM test WHERE test_id = :test_id;'),{'test_id':test_id}).fetchone()[0]
    test_questions = conn.execute(text('SELECT q.question_text FROM test t JOIN question q ON t.test_id = q.test_id WHERE t.test_id = :test_id;'),{'test_id':test_id}).fetchall()
    return render_template('edit_test.html',test_title=test_title, test_questions=test_questions)

@app.route('/delete_test/<int:test_id>', methods=['POST'])
def delete_test(test_id):
    print(session['user_id'])
    conn.execute(text('DELETE FROM test WHERE test_id=:id AND created_by=:user_id'),{'id':test_id, 'user_id':session.get('user_id')})
    conn.commit()
    return redirect('/teacher_page')



# --------------- STUDENT PAGE AND FUNCS -------------------
@app.route('/student_page')
def student_page():
    # Add logic for student page as needed
    return render_template('student_main.html')








if __name__ == '__main__':
    app.run(debug=True)
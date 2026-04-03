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
        user = conn.execute(text('SELECT * FROM account WHERE email = :email AND password = :password'), request.form).fetchone()
        if user is None:
            conn.execute(text('INSERT INTO account (role, name, email, password) VALUES (:role, :name, :email, :password)'), request.form)
            conn.commit()
            if request.form['role'] == 'student':
                return redirect(url_for('student_page'))
            else:
                return redirect(url_for('teacher_page'))
        else:
            flash('Credentials already in use. Please try again.', 'errror')
            return redirect(url_for('sign_up'))
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
                print('here')
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
@app.route('/teacher_page', methods=['GET','POST'])
def teacher_page():
    user_id = session.get('user_id')
    test_page_tb = conn.execute(text('SELECT ' \
                                        't.test_id,'\
                                        't.title,' \
                                        'COUNT(q.question_id) AS question_count,' \
                                        'a.name AS creator_name, ' \
                                        'a.acc_id '
                                    'FROM test t ' \
                                    'JOIN account a ON t.created_by = a.acc_id ' \
                                    'LEFT JOIN question q ON t.test_id = q.test_id ' \
                                    'GROUP BY t.test_id, t.title, a.name;'))
    num_attempts_tb = conn.execute(text('SELECT count(*) FROM submission GROUP BY test_id;'))
    attempts = [row[0] for row in num_attempts_tb]
    return render_template('teacher_main.html', test_page_tb=test_page_tb, user_id=user_id, attempts=attempts)

@app.route('/edit_test_page/<int:test_id>', methods=['POST'])
def edit_test_page(test_id):
    test_title = conn.execute(text('SELECT title FROM test WHERE test_id = :test_id;'),{'test_id':test_id}).fetchone()[0]
    test_questions = conn.execute(text('SELECT q.question_text FROM test t JOIN question q ON t.test_id = q.test_id WHERE t.test_id = :test_id;'),{'test_id':test_id}).fetchall()
    return render_template('edit_test.html',test_title=test_title, test_questions=test_questions, test_id=test_id)

@app.route('/create_test_page', methods=['POST'])
def create_test_page():
    return render_template('create_test.html')

@app.route('/delete_test/<int:test_id>', methods=['POST'])
def delete_test(test_id):
    conn.execute(text('DELETE FROM test WHERE test_id=:id AND created_by=:user_id'),{'id':test_id, 'user_id':session.get('user_id')})
    conn.commit()
    return redirect('/teacher_page')

@app.route('/edit_test/<int:test_id>/<string:title>', methods=['POST'])
def edit_test(test_id,title):
    questions = request.form.getlist('questions')
    conn.execute(text('DELETE FROM test WHERE test_id=:id AND created_by=:user_id'),{'id':test_id, 'user_id':session.get('user_id')})
    conn.commit()
    conn.execute(text('INSERT INTO test (test_id, title, created_by) VALUES (:test_id,:title,:user_id)'),{'test_id':test_id, 'title':title, 'user_id':session.get('user_id')})
    conn.commit()
    for _ in range(len(questions)):
        if questions[_] != '':
            conn.execute(text('INSERT INTO question (test_id, question_text) VALUES (:test_id,:questions)'),{'test_id':test_id, 'questions':questions[_]})
            conn.commit()
    return render_template('teacher_main.html')

@app.route('/create_test', methods=['POST'])
def create_test():
    title = request.form.get('title')
    conn.execute(text('INSERT INTO test (title, created_by) VALUES (:title, :user_id)'),{'title':title, 'user_id':session.get('user_id')})
    conn.commit()
    questions = request.form.getlist('questions')
    test_id = conn.execute(text('SELECT test_id FROM test WHERE title=:title and created_by=:user_id'),{'title':title, 'user_id':session.get('user_id')}).fetchone()[0]
    for _ in range(len(questions)):
        if questions[_] != '':
            conn.execute(text('INSERT INTO question (test_id, question_text) VALUES (:test_id,:questions)'),{'test_id':test_id,'questions':questions[_]})
            conn.commit()
    return render_template('teacher_main.html')

# --------------- STUDENT PAGE AND FUNCS -------------------
@app.route('/student_page', methods=['GET','POST'])
def student_page():
    user_id = session.get('user_id')
    test_page_tb = conn.execute(text('SELECT ' \
                                        't.test_id,'\
                                        't.title,' \
                                        'COUNT(q.question_id) AS question_count,' \
                                        'a.name AS creator_name, ' \
                                        'a.acc_id ' \
                                    'FROM test t ' \
                                    'JOIN account a ON t.created_by = a.acc_id ' \
                                    'LEFT JOIN question q ON t.test_id = q.test_id ' \
                                    'GROUP BY t.test_id, t.title, a.name;'))
    check_submission = conn.execute(text('SELECT test_id FROM submission WHERE acc_id=:acc_id'),{'acc_id':user_id})
    check_ids = [row[0] for row in check_submission]
    return render_template('student_main.html', test_page_tb=test_page_tb, user_id=user_id, check_ids=check_ids, check=False)

@app.route('/completed_tests', methods=['POST'])
def completed_tests():
    user_id = session.get('user_id')
    completed_tests_tb = conn.execute(text('SELECT ' \
                                        't.test_id,' \
                                        't.title,' \
                                        'a.name as creator_name,' \
                                        'g.mark ' \
                                    'FROM test t ' \
                                    'JOIN account a ' \
                                        'ON t.created_by = a.acc_id ' \
                                    'LEFT JOIN submission s ' \
                                        'ON t.test_id = s.test_id AND s.acc_id = :student_id ' \
                                    'LEFT JOIN grade g ' \
                                        'ON s.submission_id = g.submission_id ' \
                                    'WHERE s.acc_id = :student_id;'), {'student_id':user_id})
    check_submission = conn.execute(text('SELECT test_id FROM submission WHERE acc_id=:acc_id'),{'acc_id':user_id})
    check_ids = [row[0] for row in check_submission]
    return render_template('student_main.html', test_page_tb=completed_tests_tb, user_id=user_id, check_ids=check_ids, check=True)

@app.route('/taking_test/<int:test_id>', methods=['POST'])
def test_page(test_id):
    test_title = conn.execute(text('SELECT title FROM test WHERE test_id = :test_id;'),{'test_id':test_id}).fetchone()[0]
    test_questions = conn.execute(text('SELECT q.question_text FROM test t JOIN question q ON t.test_id = q.test_id WHERE t.test_id = :test_id;'),{'test_id':test_id}).fetchall()
    return render_template('take_test.html',test_title=test_title, test_questions=test_questions, test_id=test_id)

@app.route('/submit_test/<int:test_id>', methods=['POST'])
def submit_test(test_id):
    answers = request.form.getlist('answers')
    conn.execute(text('INSERT INTO submission (acc_id, test_id) VALUES (:user_id, :test_id)'),{'user_id':session.get('user_id'), 'test_id':test_id})
    conn.commit()
    question_ids = conn.execute(text('SELECT q.question_id FROM test t JOIN question q ON t.test_id = q.test_id WHERE t.test_id = :test_id;'),{'test_id':test_id}).fetchall()
    submission_id = conn.execute(text('SELECT submission_id FROM submission WHERE acc_id=:acc_id and test_id=:test_id'),{'acc_id':session.get('user_id'), 'test_id':test_id}).fetchone()[0]
    for _ in range(len(answers)):
        conn.execute(text('INSERT INTO answer (submission_id, question_id, answer_text) VALUES (:submission_id,:question_id,:answer)'),{'submission_id':submission_id,'question_id':question_ids[_][0],'answer':answers[_]})
        conn.commit()

    return redirect('/student_page')

# ----------- SHARED FUNCS ---------------
@app.route('/view_accounts', methods=['POST'])
def view_accounts():
    role = session.get('role')
    accounts_tb = conn.execute(text('SELECT role, name FROM account;'))
    return render_template('view_accounts.html', accounts_tb=accounts_tb, role=role)

@app.route('/view_accounts_students', methods=['POST'])
def view_accounts_students():
    user_id = session.get('user_id')
    accounts_tb = conn.execute(text('SELECT role, name FROM account WHERE role = "student";'))
    return render_template('view_accounts.html', accounts_tb=accounts_tb, user_id=user_id)

@app.route('/view_accounts_teachers', methods=['POST'])
def view_accounts_teachers():
    user_id = session.get('user_id')
    accounts_tb = conn.execute(text('SELECT role, name FROM account WHERE role = "teacher";'))
    return render_template('view_accounts.html', accounts_tb=accounts_tb, user_id=user_id)

@app.route('/log_out', methods=['POST'])
def log_out():
    session['user'] = ''
    session['role'] = ''
    return redirect('/sign_up')



if __name__ == '__main__':
    app.run(debug=True)
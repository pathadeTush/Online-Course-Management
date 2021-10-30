from flask import Flask, render_template, url_for, request, redirect, flash, session, current_app
from forms import RegistrationForm, LoginForm, AccountForm
from flask_mysqldb import MySQL
from utils import get_hashed_msg, save_picture
import os

main_app = Flask(__name__)
main_app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
main_app.config['MYSQL_HOST'] = 'localhost'
main_app.config['MYSQL_USER'] = 'root'
main_app.config['MYSQL_PASSWORD'] = ''
main_app.config['MYSQL_DB'] = 'College'
main_app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(main_app)

'''
    If unable to connect to mysql try following
    Reference: https://www.codegrepper.com/code-examples/shell/%281698%2C+%22Access+denied+for+user+%27root%27%40%27localhost%27%22%29+in+flask

    Now your new password for root user is '' (nothing)

'''

@main_app.route('/')
@main_app.route('/home')
def home():
    return render_template('home.html', title='Home')

@main_app.route('/register', methods=['GET', 'POST'])
def register():
    if 'loggedin' in session:
        flash('You already logged in', 'danger')
        return redirect('account')
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        MIS = form.MIS.data
        password = form.password.data
        password = get_hashed_msg(password)
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('insert into student_login(MIS, password) values(%s, %s)', (MIS, password))
            mysql.connection.commit()
            cursor.close()
        except:
            flash('Invalid MIS', 'danger')
            return render_template('register.html', title='Register', form=form)
        return redirect('login')
    return render_template('register.html', title='Register', form=form)

@main_app.route('/login', methods=['GET', 'POST'])
def login():
    if 'loggedin' in session:
        flash('You already logged in', 'danger')
        return redirect('account')
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        MIS = form.MIS.data
        password = form.password.data
        password = get_hashed_msg(password)
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM student_login WHERE MIS=(%s) AND password=(%s)', (MIS, password))
        data = cursor.fetchone()
        cursor.close()
        if data:
            session['MIS'] = MIS
            session['loggedin'] = True
            flash('Logged in successfully!', 'success')
            return redirect('account')
        else:
            flash('Invalid Login Credientials. Try again!', 'danger')
            return render_template('login.html', title='Login', form=form)
    else:
        return render_template('login.html', title='Login', form=form)

@main_app.route('/account', methods=['GET', 'POST'])
def account():
    if 'loggedin' not in session:
        flash('Log in to access account details', 'danger')
        return redirect('login')
    form = AccountForm()
    MIS = session['MIS']
    if request.method == 'POST' and form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        address = form.address.data
        gender = request.form.get('gender') # name of select field in form
        yearEnrolled = request.form.get('yearEnrolled')
        DOB = request.form.get('DOB')
        deptID = request.form.get('deptID')
        profilepic = form.profilepic.data
        if profilepic:
            profilepic = save_picture(profilepic)
            if session['profilepic'] != 'default.png':
                previous_picture_file = os.path.join(current_app.root_path, 'static/student_pics/', session['profilepic'])
            else:
                previous_picture_file = ''
            session['profilepic'] = profilepic
            # deleting previous profile picture
            if previous_picture_file:
                os.remove(previous_picture_file)
        else:
            profilepic = 'default.png'
        print(profilepic, DOB, yearEnrolled)
        cursor = mysql.connection.cursor()
        if session['new_record']:
            cursor.execute('insert into student_account values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (MIS, firstname, lastname, email, address, gender, yearEnrolled, DOB, deptID, profilepic))
        else:
            cursor.execute('UPDATE student_account SET firstname=%s, lastname=%s, email=%s, address=%s, gender=%s, yearEnrolled=%s, DOB=%s, deptID=%s, profilepic=%s WHERE MIS=%s', (firstname, lastname, email, address, gender, yearEnrolled, DOB, deptID, profilepic, MIS))
        mysql.connection.commit()
        cursor.close()
        flash('Account details updated successfully!', 'success')
        return redirect('account')
    else:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM student_account WHERE MIS=%s', (MIS,))
        data = cursor.fetchone()
        cursor.close()
        if data:
            form.firstname.data = data['firstname']
            form.lastname.data = data['lastname']
            form.email.data = data['email']
            form.address.data = data['address']
            form.gender.data = data['gender']
            form.yearEnrolled.data = data['yearEnrolled']
            form.DOB.data = data['DOB']
            form.profilepic.data = data['profilepic']
            session['new_record'] = False
        else:
            form.profilepic.data = 'default.png'
            session['new_record'] = True
        session['profilepic'] = form.profilepic.data
        return render_template('account.html', title='account', form=form)

@main_app.route('/logout')
def logout():
    if 'loggedin' not in session:
        flash('You are not logged in!', 'danger')
        return redirect('login')
    session.pop('loggedin', None)
    session.pop('MIS', None)
    session.pop('new_record', None)
    session.pop('profilepic', None)
    return redirect('login') 

if __name__ == '__main__':
    main_app.run(debug=True)
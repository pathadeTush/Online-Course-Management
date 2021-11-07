from flask import render_template, url_for, request, redirect, flash, session, current_app, Blueprint
from instructor.forms import RegistrationForm, LoginForm, AccountForm
from utils import get_hashed_msg, save_picture
import os

instructor = Blueprint('instructor', __name__, url_prefix='/inst')

from app import mysql

@instructor.route('/register', methods=['GET', 'POST'])
def register():
    if 'loggedin' in session:
        flash('You already logged in', 'danger')
        return redirect(url_for('instructor.account'))
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        instID = form.instID.data
        password = form.password.data
        password = get_hashed_msg(password)
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('insert into instructor_login(instID, password) values(%s, %s)', (instID, password))
            mysql.connection.commit()
            cursor.close()
        except:
            flash('Invalid instID', 'danger')
            return render_template('instructor/register.html', title='Register', form=form)
        return redirect(url_for('instructor.login'))
    return render_template('instructor/register.html', title='Register', form=form)

@instructor.route('/login', methods=['GET', 'POST'])
def login():
    if 'loggedin' in session:
        flash('You already logged in', 'danger')
        return redirect(url_for('instructor.account'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        instID = form.instID.data
        password = form.password.data
        password = get_hashed_msg(password)
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM instructor_login WHERE instID=(%s) AND password=(%s)', (instID, password))
        data = cursor.fetchone()
        cursor.close()
        if data:
            session['ID'] = instID
            session['loggedin'] = True
            session['user'] = 'instructor'
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM instructor_account WHERE instID=%s', (instID,))
            data = cursor.fetchone()
            cursor.close()
            if not data:
                session['account_details_added'] = True
            else:
                session['account_details_added'] = False
            flash('Logged in successfully!', 'success')
            return redirect(url_for('instructor.account'))
        else:
            flash('Invalid Login Credientials. Try again!', 'danger')
            return render_template('instructor/login.html', title='Login', form=form)
    else:
        return render_template('instructor/login.html', title='Login', form=form)

@instructor.route('/account', methods=['GET', 'POST'])
def account():
    if 'user' in session and session['user'] != 'instructor':
        return render_template('errors/403.html'), 403
    if 'loggedin' not in session:
        flash('Log in to access account details', 'danger')
        return redirect(url_for('instructor.login'))
    form = AccountForm()
    instID = session['ID']
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
        prev_profilepic = session['profilepic']
        
        if profilepic:
            new_profilepic = save_picture(profilepic, 'instructor_pics')
            session['profilepic'] = new_profilepic
        if prev_profilepic != 'default.png' and profilepic:
            # deleting previous profile picture
            previous_picture_file = os.path.join(current_app.root_path, 'static/instructor_pics/', prev_profilepic)
            os.remove(previous_picture_file)
        if not profilepic:
            session['profilepic'] = prev_profilepic
        
        cursor = mysql.connection.cursor()
        if session['new_record']:
            cursor.execute('insert into instructor_account values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (instID, firstname, lastname, email, address, gender, yearEnrolled, DOB, deptID, session['profilepic']))
        else:
            cursor.execute('UPDATE instructor_account SET firstname=%s, lastname=%s, email=%s, address=%s, gender=%s, yearEnrolled=%s, DOB=%s, deptID=%s, profilepic=%s WHERE instID=%s', (firstname, lastname, email, address, gender, yearEnrolled, DOB, deptID, session['profilepic'], instID))
        mysql.connection.commit()
        cursor.close()
        session['account_details_added'] = True
        flash('Account details updated successfully!', 'success')
        return redirect(url_for('instructor.account'))
    else:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM instructor_account WHERE instID=%s', (instID,))
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
            form.deptID.data = data['deptID']
            form.profilepic.data = data['profilepic']
            session['new_record'] = False
            session['account_details_added'] = True
        else:
            form.profilepic.data = 'default.png'
            session['new_record'] = True
            session['account_details_added'] = False
        session['profilepic'] = form.profilepic.data
        return render_template('instructor/account.html', title='account', form=form)

@instructor.route('/mycourses', methods=['GET'])
def mycourses():
    if 'user' in session and session['user'] != 'instructor':
        return render_template('errors/403.html'), 403
    if 'loggedin' not in session:
        flash('You are not logged in!', 'danger')
        return redirect('instructor.login')
    if not session['account_details_added']:
        flash('Please add your account details first!', 'warning')
        return redirect(url_for('instructor.account'))
    instID = session['ID']
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM course WHERE courseId IN (SELECT courseId FROM handled_by WHERE instID=%s);', (instID,))
    courses = cursor.fetchall()
    my_courses = []
    for course in courses:
        my_courses.append(course)
    return render_template('instructor/mycourses.html', title='My Courses', courses=my_courses)

@instructor.route('/logout')
def logout():
    if 'user' in session and session['user'] != 'instructor':
        return render_template('errors/403.html'), 403
    if 'loggedin' not in session:
        flash('You are not logged in!', 'danger')
        return redirect('instructor.login')
    if not session['account_details_added']:
        flash('Please add your account details first!', 'warning')
        return redirect(url_for('instructor.account'))
    session.clear()
    return redirect(url_for('instructor.login')) 


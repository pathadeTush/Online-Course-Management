from flask import render_template, url_for, request, redirect, flash, current_app, session, Blueprint
from student.forms import RegistrationForm, LoginForm, AccountForm, UnenrollmentForm
from utils import get_hashed_msg, save_picture
import os

student = Blueprint('student', __name__)

from app import mysql

@student.route('/register', methods=['GET', 'POST'])
def register():
    if 'loggedin' in session:
        flash('You already logged in', 'danger')
        return redirect(url_for('student.account'))
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
            return render_template('student/register.html', title='Register', form=form)
        return redirect(url_for('student.login'))
    return render_template('student/register.html', title='Register', form=form)

@student.route('/login', methods=['GET', 'POST'])
def login():
    if 'loggedin' in session:
        flash('You already logged in', 'danger')
        return redirect(url_for('student.account'))
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
            session['ID'] = MIS
            session['loggedin'] = True
            session['user'] = 'student'
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM student_account WHERE MIS=%s', (MIS,))
            data = cursor.fetchone()
            cursor.close()
            if not data:
                session['account_details_added'] = True
            else:
                session['account_details_added'] = False
            flash('Logged in successfully!', 'success')
            return redirect(url_for('student.account'))
        else:
            flash('Invalid Login Credientials. Try again!', 'danger')
            return render_template('student/login.html', title='Login', form=form)
    else:
        return render_template('student/login.html', title='Login', form=form)

@student.route('/account', methods=['GET', 'POST'])
def account():
    if 'user' in session and session['user'] != 'student':
        return render_template('errors/403.html'), 403
    if 'loggedin' not in session:
        flash('Log in to access account details', 'danger')
        return redirect(url_for('student.login'))
    form = AccountForm()
    MIS = session['ID']
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
            new_profilepic = save_picture(profilepic, 'student_pics')
            session['profilepic'] = new_profilepic
        if prev_profilepic != 'default.png' and profilepic:
            # deleting previous profile picture
            previous_picture_file = os.path.join(current_app.root_path, 'static/student_pics/', prev_profilepic)
            os.remove(previous_picture_file)
        if not profilepic:
            session['profilepic'] = prev_profilepic

        cursor = mysql.connection.cursor()
        if session['new_record']:
            cursor.execute('insert into student_account values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (MIS, firstname, lastname, email, address, gender, yearEnrolled, DOB, deptID, session['profilepic']))
        else:
            cursor.execute('UPDATE student_account SET firstname=%s, lastname=%s, email=%s, address=%s, gender=%s, yearEnrolled=%s, DOB=%s, deptID=%s, profilepic=%s WHERE MIS=%s', (firstname, lastname, email, address, gender, yearEnrolled, DOB, deptID, session['profilepic'], MIS))
        mysql.connection.commit()
        cursor.close()
        session['account_details_added'] = True
        flash('Account details updated successfully!', 'success')
        return redirect(url_for('student.account'))
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
            form.deptID.data = data['deptID']
            form.profilepic.data = data['profilepic']
            session['new_record'] = False
            session['account_details_added'] = True
        else:
            form.profilepic.data = 'default.png'
            session['new_record'] = True
            session['account_details_added'] = False
        session['profilepic'] = form.profilepic.data
        return render_template('student/account.html', title='account', form=form)


@student.route('/mycourses', methods=['GET', 'POST'])
def mycourses():
    if 'user' in session and session['user'] != 'student':
        return render_template('errors/403.html'), 403
    if 'loggedin' not in session:
        flash('You are not logged in!', 'danger')
        return redirect(url_for('student.login'))
    if not session['account_details_added']:
        flash('Please add your account details first!', 'warning')
        return redirect(url_for('student.account'))
    MIS = session['ID']
    cursor = mysql.connection.cursor()
    cursor.execute('select courseId, courseName from course where courseId in (select courseId from taken_courses where MIS = %s)', (MIS, ))
    data = cursor.fetchall()
    for x in data:
        cursor.execute('select deptID from course where courseId = %s', (x['courseId'], ))
        d_id = cursor.fetchone()
        d_id = d_id['deptID']
        mysql.connection.commit()
    cursor.close()
    course_list = list(data)
    classroom = dict() 
    for i in course_list:
        cursor = mysql.connection.cursor()
        cursor.execute('select classID from taken_in where courseId = %s', (i['courseId'], ))
        classno = cursor.fetchone()['classID']
        classroom[i['courseName']] = classno
    cursor.close()
    form = UnenrollmentForm()
    if request.method == 'POST' and form.validate_on_submit():
        MIS = session['ID']
        course_id = form.course_id.data
        cursor = mysql.connection.cursor()
        cursor.execute('delete from taken_courses where MIS = %s and courseId = %s', (MIS, course_id))
        mysql.connection.commit()
        cursor.execute('select seatsLeft from course where courseId = %s', (course_id, ))
        seats = cursor.fetchone()
        if not seats:
            flash(f'No enrolled course with courseID {course_id}', 'warning')
            return redirect(url_for('student.mycourses'))
        seats_left = str(int(seats['seatsLeft']) + 1)
        sql = 'update course set course.seatsLeft = %s where courseId = %s'
        cursor.execute(sql, (seats_left, course_id))
        mysql.connection.commit()
        cursor.close()
        flash('Unenrolled from the course')
        return redirect('courses')
    return render_template('student/mycourses.html', courses= course_list, form = form, classroom = classroom)


@student.route('/logout')
def logout():
    if 'user' in session and session['user'] != 'student':
        return render_template('errors/403.html'), 403
    if 'loggedin' not in session:
        flash('You are not logged in!', 'danger')
        return redirect(url_for('student.login'))
    if not session['account_details_added']:
        flash('Please add your account details first!', 'warning')
        return redirect(url_for('student.account'))
    session.clear()
    return redirect(url_for('student.login'))

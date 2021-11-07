from flask import Flask, render_template, url_for, redirect, session, request, flash
from flask_mysqldb import MySQL
from forms import EnrollmentForm
from utils import get_hashed_msg
import os

main_app = Flask(__name__)
main_app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
main_app.config['MYSQL_HOST'] = 'localhost'
main_app.config['MYSQL_USER'] = 'root'
main_app.config['MYSQL_PASSWORD'] = ''
main_app.config['MYSQL_DB'] = 'College'
main_app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(main_app)

from student.routes import student
from instructor.routes import instructor
from errors.handlers import errors

main_app.register_blueprint(student)
main_app.register_blueprint(instructor)
main_app.register_blueprint(errors)

@main_app.route('/')
@main_app.route('/home')
def home():
    return render_template('home.html', title='Home')

@main_app.route('/courses', methods= ['GET', 'POST'])
def courses():
    if 'loggedin' not in session:
        flash('You are not logged in!', 'danger')
        return redirect(url_for('student.login'))
    if not session['account_details_added']:
        flash('Please add your account details first!', 'warning')
        return redirect(url_for(f'{session["user"]}.account'))
    cursor = mysql.connection.cursor()
    cursor.execute('select * from course')
    fetched_courses = cursor.fetchall()
    res = []
    classroom = dict()
    for i in fetched_courses:
        res.append(i)
        cursor.execute('select classID from taken_in where courseId = %s', (i['courseId'], ))
        classno = cursor.fetchone()
        if not classno:
            flash('No Classroom Assigned!', 'danger')
            return redirect(url_for(f'{session["user"]}.account'))
        classno = classno['classID']
        classroom[i['courseName']] = classno
        link = str(i['courseName'])
        if link != i['courselink']:
            link = get_hashed_msg(link)
            i['courselink'] = link
            cursor.execute('UPDATE course SET courseName=%s, deptID=%s, term=%s, credits=%s, textbook=%s, refTextbook=%s, courselink=%s, maxCap=%s , seatsLeft=%s WHERE courseId=%s',
                        (i['courseName'], i['deptID'], i['term'], i['credits'], i['textbook'], i['refTextbook'], i['courselink'], i['maxCap'], i['seatsLeft'], i['courseId']))
            mysql.connection.commit()
    cursor.close()
    form = EnrollmentForm()
    if request.method == 'POST' and form.validate_on_submit():
        course_id = form.course_id.data
        MIS = session['ID']
        cursor = mysql.connection.cursor()
        cursor.execute('select * from taken_courses')
        taken = cursor.fetchall()
        taken = list(taken)
        single = True
        prereq = True
        for i in taken:
            if i['courseId'] == course_id and i['MIS'] == MIS:
                single = False
                break
        cursor.execute('select prereqId from prereq where courseId = %s', (course_id, ))
        data = cursor.fetchone()
        res = []
        course_list = []
        while data != None:
            res.append(data['prereqId'])
            curr = data['prereqId']
            cursor.execute('select prereqId from prereq where courseId = %s', (curr, ))
            data = cursor.fetchone()
        if len(res):
            for i in res:
                cursor.execute('select * from taken_courses where MIS = %s and courseId = %s', (MIS, i))
                enrolled = cursor.fetchone()
                if not enrolled:
                    prereq = False
                    cursor.execute('select courseName from course where courseId = %s', (i, ))
                    cname = cursor.fetchone()
                    course_list.append(cname['courseName'])
            
        if single and prereq: 
            sql = 'insert into taken_courses values(%s, %s)'
            cursor.execute(sql, (MIS, course_id))
            mysql.connection.commit()
            cursor.execute('select seatsLeft from course where courseId = %s', (course_id, ))
            seats = cursor.fetchone()
            if not seats:
                flash(f'No course with courseID {course_id}', 'warning')
                return redirect('courses')
            seats_left = str(int(seats['seatsLeft']) - 1)
            if int(seats_left) < 0:
                flash('No Seats Left!!')
                return redirect('courses')
            sql = 'update course set course.seatsLeft = %s where courseId = %s'
            cursor.execute(sql, (seats_left, course_id))
            mysql.connection.commit()
            flash('Enrolled in Course Successfully', 'success')
            return redirect(url_for('student.mycourses'))
        elif not single and prereq:
            flash('Already Enrolled', 'danger')
        elif not prereq and single:
            flash('Not enrolled in the prerequisite courses', 'danger')
            flash(f'Enroll in the following courses first {course_list}')
            return redirect('courses')
        else:
            flash('Either you are already enrolled or can\'t meet the prereq')
            return redirect('courses')
        cursor.close()
    return render_template('courses.html', title='Courses', has_courses=res, form = form, classroom = classroom)


@main_app.route('/course_page/<course_name>', methods=['GET', 'POST'])
def course_page(course_name):
    if 'loggedin' not in session:
        flash('You are not logged in!', 'danger')
        return redirect(url_for('student.login'))
    if not session['account_details_added']:
        flash('Please add your account details first!', 'warning')
        return redirect(url_for(f'{session["user"]}.account'))
    course_dict = {'Artificial Intelligence': '1001S', 'EE': '2001F', 'Combustion Engines': '3001F','Material Strengths': '4001S', 'Control Systems': '5001S', 'Automation and Robotics': '6001F', 'Metals, Alloys and Composites': '7001S', 'IOT Systems': '8001F', 'Microprocessors and system arch': '9001F'}
    course_dict['Theory of Computation'] = '1001P'
    course_dict['BEE'] = '2001P'
    course_dict['Foundation of ME'] = '3001P'   
    course_dict['Engg. Mechanics'] = '4001P'
    course_dict['Newtonian Mechanics'] = '4001PP'
    course_dict['Sensors and Transducers'] = '5001P'
    course_id = course_dict[course_name]
    cname = course_name
    cursor = mysql.connection.cursor()
    cursor.execute('select * from course where courseId = %s', (course_id, ))
    details = cursor.fetchone()
    cursor.close()
    form = EnrollmentForm()
    if request.method == 'POST' and form.validate_on_submit():
        pass
    return render_template('course_page.html', title=course_name.upper(), details = details, enumerate=enumerate, form=form)



if __name__ == '__main__':
    import sys
    main_app.run(debug=True)

'''
    If unable to connect to mysql try following
    Reference: https://www.codegrepper.com/code-examples/shell/%281698%2C+%22Access+denied+for+user+%27root%27%40%27localhost%27%22%29+in+flask

    Now your new password for root user is '' (nothing)

'''

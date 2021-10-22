from flask import Flask, render_template, url_for

main_app = Flask(__name__)

@main_app.route('/')
@main_app.route('/home')
def home():
    return render_template('home.html', title='Home')

@main_app.route('/about')
def about():
    return render_template('about.html', title='About')

@main_app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html', title='Register')

@main_app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title='Login')

@main_app.route('/account', methods=['GET', 'POST'])
def account():
    return render_template('account.html', title='Account')

if __name__ == '__main__':
    main_app.run(debug=True)
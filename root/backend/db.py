from flaskext.mysql import MySQL
from app import main_app

mysql = MySQL()
mysql.init_app(main_app)
cursor = mysql.get_db()
# print(type(cursor))
if __name__ == '__main__':
    main_app.run(debug=True)


''' 
   Reference: https://flask-mysql.readthedocs.io/en/latest/
'''
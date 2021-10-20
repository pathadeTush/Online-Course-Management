from flaskext.mysql import MySQL
import Code.app.app as app
mysql = MySQL()
mysql.init_app(app)
cursor = mysql.get_db()
print(type(cursor))
app.run()

from flask import Blueprint, render_template

# Creating blueprint for errors
errors = Blueprint('errors', __name__)

# event handler for error raised (app_errorhandler)
# 404 Not Found
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

# 403 Forbidden
@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

# 500 Internal Server Error
@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500
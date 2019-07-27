from flask import render_template,Blueprint
from favoriteThings.models import AuditLog
from flask_login import current_user
from datetime import datetime
from favoriteThings.utils import addLog
logs = Blueprint('logs',__name__)


@logs.route('/log',methods=['GET'])
def log():
    logs = AuditLog.query.filter_by(user_id=current_user.id).all()
    log = 'Open logs tab on'
    addLog(log)
    return render_template('log.html',logs=logs)


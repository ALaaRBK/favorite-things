from favoriteThings.models import AuditLog
from flask_login import current_user
from favoriteThings import db
from datetime import datetime


def addLog(log):
    log = log + ' ' + datetime.utcnow().strftime('%Y-%m-%d %H:%M')
    newLog = AuditLog(log=log,user_id=current_user.id)
    db.session.add(newLog)
    db.session.commit()
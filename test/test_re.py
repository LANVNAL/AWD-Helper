from db import *
def delete_target(ip):
    num = Target.query.filter_by(ip=ip).count()
    if num > 1:
        return 'error'
    else:
        data = Target.query.filter_by(ip=ip).first()
        db.session.delete(data)
        db.session.commit()


a = delete_target('192.168.1.7')

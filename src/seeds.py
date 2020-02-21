from models import db, Users

def run():
    db.session.add(Users(
        username = 'JakAtak',
        email = 'prtecc321@gmail.com'
    ))
    db.session.commit()
    return 'User successfully created!'
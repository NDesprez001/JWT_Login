from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))

    def __repr__(self):
        return '<Users %r>' % self.username

    def serialize(self):
        return {
            "username": self.username,
            "email": self.email
        }
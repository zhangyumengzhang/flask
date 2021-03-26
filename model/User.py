from init import db


class User(db.Model):
    __tablename__ = 'user'
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(32), nullable=False)
    phone = db.Column(db.String(320))
    email = db.Column(db.String(320))
    country = db.Column(db.String(320))
    gender = db.Column(db.String(320))
    age = db.Column(db.String(320))

    def __repr__(self):
        return '<User %r>' % self.userid
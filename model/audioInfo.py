from init import db


class audioinfo(db.Model):
    __tablename__ = 'audioinfo'
    userid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), primary_key=True)
    audiotime = db.Column(db.String(255), nullable=False)
    isstar = db.Column(db.String(255))
    type = db.Column(db.String(255))

    def __repr__(self):
        return '<audioinfo %r>' % self.userid
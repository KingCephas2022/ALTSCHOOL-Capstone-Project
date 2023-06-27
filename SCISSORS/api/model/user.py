from ..utils import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(6), unique=True, nullable=False)
    link = db.relationship('LinkSpace', backref='links', lazy=True)

    def __repr__(self):
        return f"User('{self.name}')"
    
    def save(self):
        db.session.add(self)
        db.session.commit()



        
from ..utils import db

class LinkSpace(db.Model):
    __tablename__ = 'link'
    id = db.Column(db.Integer(), primary_key=True)
    link = db.Column(db.String(200), nullable=False)
    user = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f"LinkSpace('{self.link}')"
    
    def save(self):
        db.session.add(self)
        db.session.commit()


        
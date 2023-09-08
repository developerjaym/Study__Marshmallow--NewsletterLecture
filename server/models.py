from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Newsletter(db.Model):
    __tablename__ = 'newsletters'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.String)
    published_at = db.Column(db.DateTime, server_default=db.func.now())
    edited_at = db.Column(db.DateTime, onupdate=db.func.now())
    writer_id = db.Column(db.Integer, db.ForeignKey('writers.id'))
    tags = db.relationship('Tag', backref='newsletter')

    def __repr__(self):
        return f'<Newsletter {self.title}, published at {self.published_at}.>'

class Writer(db.Model):
    __tablename__ = "writers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    newsletters = db.relationship('Newsletter', backref='writer')

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    newsletter_id = db.Column(db.Integer, db.ForeignKey('newsletters.id'))
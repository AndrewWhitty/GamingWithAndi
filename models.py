from app import db

class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'), nullable=False)
    platform = db.relationship('Platform', backref='entries')
    date_started = db.Column(db.Date)
    date_finished = db.Column(db.Date)
    status = db.Column(db.String(20))
    release_date = db.Column(db.Date)
    format = db.Column(db.String(20))
    size = db.Column(db.Float)
    hours_to_complete = db.Column(db.Integer)
    metacritic_rating = db.Column(db.Integer)
    my_rating = db.Column(db.Integer)

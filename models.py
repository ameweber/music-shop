from db import *


class Ensemble(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    ensemble_type = db.Column(db.String(80), nullable=False)
    label_id = db.Column(db.Integer, db.ForeignKey('label.id'), nullable=False)
    label = db.relationship('Label',
                            backref=db.backref('ensembles', lazy='dynamic'))
    records = db.relationship('Record', backref='ensembles', lazy=True)
    songs = db.relationship('Song', backref='ensembles', lazy=True)


class Label(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)


class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)


class Musician(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    ensemble_id = db.Column(db.Integer, db.ForeignKey('ensemble.id'), nullable=False)
    ensemble = db.relationship('Ensemble',
                               backref=db.backref('musicians', lazy='dynamic'))


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ensemble_id = db.Column(db.Integer, db.ForeignKey('ensemble.id'), nullable=False)
    label_id = db.Column(db.Integer, db.ForeignKey('label.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    price_wholesale = db.Column(db.Integer, nullable=False)
    price_retail = db.Column(db.Integer, nullable=False)
    release_date = db.Column(db.Date, nullable=False)


class RecordCopy(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    record_id = db.Column(db.Integer, db.ForeignKey('record.id'), nullable=False)
    sticker_id = db.Column(db.Integer, db.ForeignKey('sticker.id'), nullable=False)
    sold = db.Column(db.Boolean, nullable=False)
    date_sold = db.Column(db.DateTime)
    record = db.relationship('Record',
                             backref=db.backref('record_copy', lazy='dynamic'))


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    ensemble_id = db.Column(db.Integer, db.ForeignKey('ensemble.id'), nullable=False)


class RecordSong(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    record_id = db.Column(db.Integer, db.ForeignKey('record.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    song = db.relationship('Song',
                           backref=db.backref('record_song', lazy='dynamic'))
    record = db.relationship('Record',
                             backref=db.backref('record_song', lazy='dynamic'))


class Sticker(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(255), nullable=False)

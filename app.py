from flask import render_template, request, redirect
from models import *
from db import *
from datetime import datetime, date
from sqlalchemy import func


@app.route('/')
def home():
    leaders = db.engine.execute(
        "SELECT e.name as ensemble, r.name as record, count(record_id) as amount FROM record_copy as rc INNER JOIN record r ON rc.record_id=r.id INNER JOIN ensemble e ON r.ensemble_id=e.id WHERE sold = 1 AND date_sold > '2020-01-01' GROUP by record_id ORDER BY count(record_id) DESC")
    return render_template('home.html', leaders=leaders)


@app.route('/ensembles')
def ensembles():
    ensembles = Ensemble.query.all()
    return render_template('ensembles.html', ensembles=ensembles)


@app.route('/add-ensemble', methods=["GET", "POST"])
def add_ensemble():
    if request.form:
        try:
            ensemble = Ensemble(
                name=request.form.get("ensemble_name"),
                ensemble_type=request.form.get("ensemble_type"),
                label_id=request.form.get("label_id")
            )
            db.session.add(ensemble)
            db.session.commit()
            return redirect('/ensembles')
        except Exception as e:
            print("Failed to add an ensemble")
            print(e)
    labels = Label.query.all()
    return render_template('add_ensemble.html', labels=labels)


@app.route('/edit-ensemble', methods=["GET", "POST"])
def edit_ensemble():
    ensemble_id = request.args.get('ensemble_id')
    ensemble = Ensemble.query.filter_by(id=ensemble_id).first()
    if request.form:
        ensemble = Ensemble.query.filter_by(id=request.form.get('ensemble_id')).first()
        ensemble.name = request.form.get('ensemble_name')
        ensemble.ensemble_type = request.form.get('ensemble_type')
        ensemble.label_id = request.form.get('label_id')
        db.session.commit()
        return redirect('/ensembles')
    labels = Label.query.all()
    return render_template('edit_ensemble.html', ensemble=ensemble, labels=labels)


@app.route('/add-label', methods=["GET", "POST"])
def add_label():
    if request.form:
        try:
            label = Label(
                name=request.form.get("label_name"),
            )
            db.session.add(label)
            db.session.commit()
            return redirect('/add-ensemble')
        except Exception as e:
            print("Failed to add a label")
            print(e)
    return render_template('add_label.html')


@app.route('/add-musicians', methods=["GET", "POST"])
def add_musicians():
    ensemble_id = request.args.get('ensemble_id')
    musicians = Musician.query.filter_by(ensemble_id=ensemble_id).all()
    delete_id = request.args.get("delete_id")
    ensemble = Ensemble.query.filter_by(id=ensemble_id).first()
    if delete_id:
        musician = Musician.query.filter_by(id=delete_id).first()
        db.session.delete(musician)
        db.session.commit()
        return redirect('/add-musicians?ensemble_id=' + ensemble_id)
    if request.form:
        ensemble_id = request.form.get("ensemble_id")
        musician = Musician(
            firstname=request.form.get("firstname"),
            lastname=request.form.get("lastname"),
            role=request.form.get("role"),
            ensemble_id=ensemble_id,
        )
        db.session.add(musician)
        db.session.commit()
        return redirect('/add-musicians?ensemble_id=' + ensemble_id)
    return render_template('add_musicians.html', musicians=musicians, ensemble_id=ensemble_id,
                           ensemble_name=ensemble.name, musicians_len=len(musicians))


@app.route('/records', methods=["GET", "POST"])
def records():
    ensemble_id = request.args.get('ensemble_id')
    ensemble = Ensemble.query.filter_by(id=ensemble_id).first()
    labels = Label.query.all()
    sellers = Seller.query.all()
    records = Record.query.filter_by(ensemble_id=ensemble_id).all()
    delete_id = request.args.get("delete_id")
    if delete_id:
        record = Record.query.filter_by(id=delete_id).first()
        db.session.delete(record)
        db.session.commit()
        return redirect('/records?ensemble_id=' + ensemble_id)
    return render_template('records.html', records=records, sellers=sellers, ensemble=ensemble, labels=labels)


@app.route('/add-record', methods=["GET", "POST"])
def add_record():
    ensemble_id = request.args.get('ensemble_id')
    if request.form:
        ensemble_id = request.form.get("ensemble_id")
        release_date = request.form.get("release_date")
        release_date = datetime.strptime(release_date, '%Y-%m-%d')
        record = Record(
            ensemble_id=ensemble_id,
            label_id=request.form.get("label_id"),
            seller_id=request.form.get("seller_id"),
            name=request.form.get("name"),
            price_retail=request.form.get("price_retail"),
            price_wholesale=request.form.get("price_wholesale"),
            release_date=release_date
        )
        db.session.add(record)
        db.session.commit()
        return redirect('/records?ensemble_id=' + ensemble_id)


@app.route('/edit-record', methods=["GET", "POST"])
def edit_record():
    ensemble_id = request.args.get('ensemble_id')
    record_id = request.args.get('record_id')
    record = Record.query.filter_by(id=record_id).first()
    if request.form:
        record_id = request.form.get('record_id')
        ensemble_id = request.form.get('ensemble_id')
        record = Record.query.filter_by(id=record_id).first()
        release_date = request.form.get("release_date")
        release_date = datetime.strptime(release_date, '%Y-%m-%d').date()
        record = Record.query.filter_by(id=request.form.get('record_id')).first()
        record.name = request.form.get('record_name')
        record.price_retail = request.form.get('price_retail')
        record.price_wholesale = request.form.get('price_wholesale')
        record.release_date = release_date
        db.session.commit()
        return redirect('/records?ensemble_id=' + ensemble_id)
    return render_template('edit_record.html', record=record, ensemble_id=ensemble_id)


@app.route('/add-seller', methods=["GET", "POST"])
def add_seller():
    ensemble_id = request.args.get('ensemble_id')
    if request.form:
        ensemble_id = request.form.get('ensemble_id')
        seller = Seller(
            name=request.form.get("seller_name"),
            address=request.form.get("address")
        )

        db.session.add(seller)
        db.session.commit()
        return redirect('/records?ensemble_id=' + ensemble_id)
    return render_template('add_seller.html', ensemble_id=ensemble_id)


@app.route('/songs')
def songs():
    # record_id = request.args.get('record_id')
    ensemble_id = request.args.get('ensemble_id')
    ensemble = Ensemble.query.filter_by(id=ensemble_id).first()
    songs = Song.query.filter_by(ensemble_id=ensemble_id).all()
    delete_id = request.args.get('delete_id')
    if delete_id:
        song = Song.query.filter_by(id=delete_id).first()
        db.session.delete(song)
        db.session.commit()
        return redirect('/songs?ensemble_id=' + ensemble_id)
    # label = Label.query.filter_by(id=1).first()
    # print(label.ensembles)
    return render_template('songs.html', songs=songs, ensemble_id=ensemble_id, ensemble = ensemble)


@app.route('/add-song', methods=["POST"])
def add_song():
    if request.form:
        ensemble_id = request.form.get("ensemble_id")
        record_id = request.form.get("record_id")
        song = Song(
            ensemble_id=ensemble_id,
            name=request.form.get("name"),
        )
        db.session.add(song)
        db.session.commit()
        return redirect('/songs?ensemble_id=' + ensemble_id + '&record_id=' + record_id)


@app.route('/record-copies')
def record_copies():
    record_id = request.args.get('record_id')
    ensemble_id = request.args.get('ensemble_id')
    copies = RecordCopy.query.filter_by(record_id=record_id).all()
    stickers = Sticker.query.all()
    delete_id = request.args.get('delete_id')
    sold_id = request.args.get('sold_id')
    if delete_id:
        record_copy = RecordCopy.query.filter_by(id=delete_id).first()
        db.session.delete(record_copy)
        db.session.commit()
        return redirect('/record-copies?ensemble_id=' + ensemble_id + '&record_id=' + record_id)
    if sold_id:
        record_copy = RecordCopy.query.filter_by(id=sold_id).first()
        record_copy.sold = 1
        record_copy.date_sold = datetime.now()
        db.session.commit()
        return redirect('/record-copies?ensemble_id=' + ensemble_id + '&record_id=' + record_id)
    return render_template('record_copies.html', copies=copies, stickers=stickers, record_id=record_id,
                           ensemble_id=ensemble_id)


@app.route('/add-record-copy', methods=["POST"])
def add_record_copy():
    if request.form:
        ensemble_id = request.form.get("ensemble_id")
        record_id = request.form.get("record_id")
        record_copy = RecordCopy(
            record_id=record_id,
            sticker_id=request.form.get("sticker_id"),
            sold=0,
        )
        db.session.add(record_copy)
        db.session.commit()
        return redirect('/record-copies?ensemble_id=' + ensemble_id + '&record_id=' + record_id)


@app.route('/add-sticker', methods=["GET", "POST"])
def add_sticker():
    ensemble_id = request.args.get('ensemble_id')
    record_id = request.args.get('record_id')
    if request.form:
        ensemble_id = request.form.get('ensemble_id')
        record_id = request.form.get('record_id')
        sticker = Sticker(
            comment=request.form.get("comment"),
        )

        db.session.add(sticker)
        db.session.commit()
        return redirect('/record-copies?ensemble_id=' + ensemble_id + '&record_id=' + record_id)
    return render_template('add_sticker.html', ensemble_id=ensemble_id, record_id=record_id)


@app.route('/records-songs')
def records_songs():
    record_id = request.args.get('record_id')
    ensemble_id = request.args.get('ensemble_id')
    record_songs = RecordSong.query.filter_by(record_id=record_id).all()
    songs = Song.query.filter_by(ensemble_id=ensemble_id).all()
    delete_id = request.args.get('delete_id')
    if delete_id:
        record_songs = RecordSong.query.filter_by(id=delete_id).first()
        db.session.delete(record_songs)
        db.session.commit()
        return redirect('/records-songs?ensemble_id=' + ensemble_id + '&record_id=' + record_id)
    # label = Label.query.filter_by(id=1).first()
    # print(label.ensembles)
    return render_template('records_songs.html', songs=songs, record_songs=record_songs, record_id=record_id,
                           ensemble_id=ensemble_id)


@app.route('/add-record-song', methods=["POST"])
def add_record_song():
    if request.form:
        ensemble_id = request.form.get("ensemble_id")
        record_id = request.form.get("record_id")
        record_song = RecordSong(
            record_id=record_id,
            song_id=request.form.get("song_id"),
        )
        db.session.add(record_song)
        db.session.commit()
        return redirect('/records-songs?ensemble_id=' + ensemble_id + '&record_id=' + record_id)


# @app.route('/leaders')
# def leaders():
#     leaders = db.engine.execute(
#         "SELECT e.name as ensemble, r.name as record, count(record_id) as amount FROM record_copy as rc INNER JOIN record r ON rc.record_id=r.id INNER JOIN ensemble e ON r.ensemble_id=e.id WHERE sold = 1 AND date_sold > '2020-01-01' GROUP by record_id ORDER BY count(record_id) DESC")
#     return render_template('leaders.html', leaders=leaders)


if __name__ == '__main__':
    app.run(debug=True)

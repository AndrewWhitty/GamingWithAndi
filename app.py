from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import EntryForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_url_here'
db = SQLAlchemy(app)

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

@app.route('/')
def index():
    entries = Entry.query.all()
    return render_template('index.html', entries=entries)

@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    form = EntryForm()
    if form.validate_on_submit():
        new_entry = Entry(
            title=form.title.data,
            platform_id=form.platform.data,
            date_started=form.date_started.data,
            date_finished=form.date_finished.data,
            status=form.status.data,
            release_date=form.release_date.data,
            format=form.format.data,
            size=form.size.data,
            hours_to_complete=form.hours_to_complete.data,
            metacritic_rating=form.metacritic_rating.data,
            my_rating=form.my_rating.data
        )
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_entry.html', form=form)

@app.route('/edit_entry/<int:entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id):
    entry = Entry.query.get(entry_id)
    form = EntryForm(obj=entry)
    if form.validate_on_submit():
        entry.title = form.title.data
        entry.platform_id = form.platform.data
        entry.date_started = form.date_started.data
        entry.date_finished = form.date_finished.data
        entry.status = form.status.data
        entry.release_date = form.release_date.data
        entry.format = form.format.data
        entry.size = form.size.data
        entry.hours_to_complete = form.hours_to_complete.data
        entry.metacritic_rating = form.metacritic_rating.data
        entry.my_rating = form.my_rating.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_entry.html', form=form, entry_id=entry_id)

@app.route('/delete_entry/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    entry = Entry.query.get(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

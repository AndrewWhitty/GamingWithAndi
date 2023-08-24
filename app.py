from flask import Flask, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gwa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    platform = db.Column(db.Text)
    date_started = db.Column(db.Text)
    date_finished = db.Column(db.Text)
    status = db.Column(db.Text)
    release_date = db.Column(db.Text)
    format = db.Column(db.Text)
    size = db.Column(db.Float)
    hours_to_complete_hltb = db.Column(db.Float)
    hours_to_complete_personal = db.Column(db.Float)
    metacritic_rating = db.Column(db.Integer)
    gameplay_story_rating = db.Column(db.Integer)
    controls_rating = db.Column(db.Integer)
    visuals_rating = db.Column(db.Integer)
    audio_rating = db.Column(db.Integer)
    value_rating = db.Column(db.Integer)
    rating = db.Column(db.Integer)

    @property
    def calculate_rating(self):
        total = (
                self.gameplay_story_rating
                + self.controls_rating
                + self.visuals_rating
                + self.audio_rating
                + self.value_rating
        )
        return total


@app.route('/')
def index():
    games = Game.query.all()
    return render_template('index.html', games=games)


@app.route('/edit/<int:game_id>', methods=['GET', 'POST'])
def edit_game(game_id):
    game = Game.query.get(game_id)
    if request.method == 'POST':
        game.title = request.form['title']
        game.genre = request.form['genre']
        game.platform = request.form['platform']
        db.session.commit()
        flash('Game updated successfully!')
        return redirect(url_for('index'))
    return render_template('edit.html', game=game)


@app.route('/add_game', methods=['GET', 'POST'])
def add_game():
    if request.method == 'POST':
        # Retrieve the form data
        title = request.form['title']
        platform = request.form['platform']
        date_started = request.form['date_started']
        date_finished = request.form['date_finished']
        status = request.form['status']
        release_date = request.form['release_date']
        format = request.form['format']
        size = float(request.form['size']) if request.form['size'] else 0.0
        hours_to_complete_hltb = float(request.form['hours_to_complete_hltb']) if request.form['hours_to_complete_hltb'] else 0.0
        hours_to_complete_personal = float(request.form['hours_to_complete_personal']) if request.form['hours_to_complete_personal'] else 0.0
        metacritic_rating = int(request.form['metacritic_rating']) if request.form['metacritic_rating'] else 0
        gameplay_story_rating = int(request.form['gameplay_story_rating']) if request.form['gameplay_story_rating'] else 0
        controls_rating = int(request.form['controls_rating']) if request.form['controls_rating'] else 0
        visuals_rating = int(request.form['visuals_rating']) if request.form['visuals_rating'] else 0
        audio_rating = int(request.form['audio_rating']) if request.form['audio_rating'] else 0
        value_rating = int(request.form['value_rating']) if request.form['value_rating'] else 0

        # Calculate the total rating
        rating = (
                gameplay_story_rating
                + controls_rating
                + visuals_rating
                + audio_rating
                + value_rating
        )

        # Create a new game object
        new_game = Game(
            title=title,
            platform=platform,
            date_started=date_started,
            date_finished=date_finished,
            status=status,
            release_date=release_date,
            format=format,
            size=size,
            hours_to_complete_hltb=hours_to_complete_hltb,
            hours_to_complete_personal=hours_to_complete_personal,
            metacritic_rating=metacritic_rating,
            gameplay_story_rating=gameplay_story_rating,
            controls_rating=controls_rating,
            visuals_rating=visuals_rating,
            audio_rating=audio_rating,
            value_rating=value_rating,
            rating=rating
        )

        # Add the new game to the database
        db.session.add(new_game)
        db.session.commit()

        flash('Game added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_game.html')


if __name__ == '__main__':
    app.run(debug=True)

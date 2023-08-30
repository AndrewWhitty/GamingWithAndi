from flask import Flask, render_template, request
import csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gaming_log')
def gaming_log():
    with open('data/gamedata.csv', 'r') as file:
        reader = csv.DictReader(file)
        games = list(reader)
    return render_template('gaming_log.html', games=games)

@app.route('/stats', methods=['GET', 'POST'])
def stats():
    platforms = set()
    with open('data/gamedata.csv', 'r') as file:
        reader = csv.DictReader(file)
        games = list(reader)
        for game in games:
            platforms.add(game['platform'])
    
    selected_platform = request.form.get('platform')
    if selected_platform == 'all':
        filtered_games = games
    else:
        filtered_games = [game for game in games if game['platform'] == selected_platform]
    
    return render_template('stats.html', games=filtered_games, platforms=platforms)

if __name__ == '__main__':
    app.run()

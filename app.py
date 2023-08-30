from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def gaming_log():
    data = pd.read_csv('data/gamedata.csv')
    return render_template('gaming_log.html', data=data)

@app.route('/stats')
def stats():
    data = pd.read_csv('gamedata.csv')
    total_hours = data['Hours Played'].sum()
    game_count = len(data)
    average_hours_per_game = total_hours / game_count

    # Calculate your gaming stats here
    # Example: Current year in gaming
    current_year_stats = data[data['Date Finished'].str.contains('2023')]
    current_year_hours = current_year_stats['Hours Played'].sum()
    current_year_games = len(current_year_stats)
    current_year_stats = current_year_stats.groupby('Title').agg({'Hours Played': 'sum'}).reset_index()
    current_year_stats = current_year_stats.sort_values('Hours Played', ascending=False)

    return render_template('stats.html', average_hours_per_game=average_hours_per_game, current_year_stats=current_year_stats)

if __name__ == '__main__':
    app.run()

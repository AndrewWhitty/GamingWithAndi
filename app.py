from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load CSV data into a Pandas DataFrame
data = pd.read_csv('data/gamedata.csv')

default_columns = ['Title', 'Platform', 'Status', 'Completion %', 'HLTB Story', 'HLTB Extras', 'HLTB Complete', 'Critic Rating']

@app.route('/')
def gaming_log():
    selected_columns = request.args.getlist('columns')
    if not selected_columns:
        selected_columns = default_columns

    return render_template('gaming_log.html', columns=selected_columns, data=data.to_dict('records'))

@app.route('/stats')
def stats():
    platform_stats = data['Platform'].value_counts().to_dict()

    # Calculate other statistics as needed
    average_hours_per_game = data['Hours Played'].mean()
    # Add more statistics calculations here

    return render_template('stats.html', platform_stats=platform_stats, average_hours_per_game=average_hours_per_game)

if __name__ == '__main__':
    app.run(debug=True)

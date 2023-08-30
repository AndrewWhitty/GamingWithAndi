from flask import Flask, render_template, request
import pandas as pd
from datetime import datetime

app = Flask(__name__)

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

    total_games_owned_per_platform = data[data['Platform'].isin(data['Platform'].value_counts().index)].groupby('Platform').size().to_dict()
    
    total_games = len(data)
    total_hours_played = round(data['Hours Played'].sum(), 0)
    average_hours_per_game = round(total_hours_played / total_games, 0)
    total_completed_games = len(data[data['Status'] == 'Completed'])
    total_in_progress_games = len(data[data['Status'] == 'Now Playing'])
    total_unplayed_games = len(data[(data['Status'] != 'Completed') & (data['Status'] != 'Now Playing')])

    completed_games = data[data['Status'] == 'Completed']
    valid_completion_percentages = completed_games[completed_games['Completion %'].notnull() & (completed_games['Completion %'] > 0)]
    average_completion_percentage = round(valid_completion_percentages['Completion %'].mean(), 2)
    
    most_played_platform = completed_games['Platform'].mode().iloc[0]

    valid_hours_played = completed_games[(completed_games['Hours Played'].notnull()) & (completed_games['Hours Played'] > 0)]
    
    longest_time_played = round(valid_hours_played['Hours Played'].max(), 0)
    shortest_time_played = round(valid_hours_played['Hours Played'].min(), 0)
    average_time_played = round(valid_hours_played['Hours Played'].mean(), 0)

    valid_critic_ratings = completed_games[completed_games['Critic Rating'].notnull() & (completed_games['Critic Rating'] > 0)]
    average_critic_rating = round(valid_critic_ratings['Critic Rating'].mean(), 2)

    current_year = datetime.now().year
    valid_date_completed = completed_games['Date Finished'].dropna()
    games_completed_this_year = len(valid_date_completed[valid_date_completed.astype(str).str.contains(str(current_year))])

    percentage_completed_vs_uncompleted = round((total_completed_games / total_games) * 100, 2)

    valid_hours_per_platform = completed_games[completed_games['Hours Played'] > 0]
    average_hours_per_platform = valid_hours_per_platform.groupby('Platform')['Hours Played'].mean().to_dict()

    data['Year'] = pd.to_datetime(data['Date Finished']).dt.year

    total_hours_per_year = data.groupby('Year')['Hours Played'].sum().to_dict()

    return render_template('stats.html',
                           platform_stats=platform_stats,
                           total_games=total_games,
                           total_hours_played=total_hours_played,
                           average_hours_per_game=average_hours_per_game,
                           total_completed_games=total_completed_games,
                           total_in_progress_games=total_in_progress_games,
                           total_unplayed_games=total_unplayed_games,
                           average_completion_percentage=average_completion_percentage,
                           most_played_platform=most_played_platform,
                           longest_time_played=longest_time_played,
                           shortest_time_played=shortest_time_played,
                           average_time_played=average_time_played,
                           average_critic_rating=average_critic_rating,
                           games_completed_this_year=games_completed_this_year,
                           percentage_completed_vs_uncompleted=percentage_completed_vs_uncompleted,
                           average_hours_per_platform=average_hours_per_platform,
                           total_hours_per_year=total_hours_per_year),
                            total_games_owned_per_platform=total_games_owned_per_platform)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request
import pandas as pd
from datetime import datetime  # Import the datetime module

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

    total_games = len(data)
    total_hours_played = round(data['Hours Played'].sum(), 2)
    average_hours_per_game = round(total_hours_played / total_games, 2)
    total_completed_games = len(data[data['Status'] == 'Completed'])
    total_in_progress_games = len(data[data['Status'] == 'In Progress'])
    total_unplayed_games = len(data[data['Status'] == 'Unplayed'])

    valid_completion_percentages = data[data['Completion %'].notnull() & (data['Completion %'] > 0)]
    average_completion_percentage = round(valid_completion_percentages['Completion %'].mean(), 2)
    most_played_platform = data['Platform'].mode().iloc[0]

    longest_time_played = round(data['Hours Played'].max(), 2)
    shortest_time_played = round(data['Hours Played'].min(), 2)
    average_time_played = round(data[data['Hours Played'] > 0]['Hours Played'].mean(), 2)

    valid_critic_ratings = data[data['Critic Rating'].notnull() & (data['Critic Rating'] > 0)]
    average_critic_rating = round(valid_critic_ratings['Critic Rating'].mean(), 2)
    highest_critic_rating = round(valid_critic_ratings['Critic Rating'].max(), 2)
    lowest_critic_rating = round(valid_critic_ratings['Critic Rating'].min(), 2)

    current_year = datetime.now().year
    valid_date_completed = data['Date Finished'].dropna()
    games_completed_this_year = len(valid_date_completed[valid_date_completed.str.contains(str(current_year))])

    percentage_completed_vs_uncompleted = round((total_completed_games / total_games) * 100, 2)
    most_common_status = data['Status'].mode().iloc[0]

    valid_hours_per_platform = data[data['Hours Played'] > 0]
    average_hours_per_platform = valid_hours_per_platform.groupby('Platform')['Hours Played'].mean().to_dict()

    total_hours_per_year = data.groupby('Year')['Hours Played'].sum().to_dict()

    total_games_owned_per_platform = valid_hours_per_platform['Platform'].value_counts().to_dict()

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
                           highest_critic_rating=highest_critic_rating,
                           lowest_critic_rating=lowest_critic_rating,
                           games_completed_this_year=games_completed_this_year,
                           percentage_completed_vs_uncompleted=percentage_completed_vs_uncompleted,
                           most_common_status=most_common_status,
                           average_hours_per_platform=average_hours_per_platform,
                           total_hours_per_year=total_hours_per_year,
                           total_games_owned_per_platform=total_games_owned_per_platform)

if __name__ == '__main__':
    app.run(debug=True)

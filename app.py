from flask import Flask, render_template, request, jsonify
import pandas as pd
from datetime import datetime

app = Flask(__name__)

data = pd.read_csv('data/gamedata.csv')

default_columns = ['Status', 'Platform', 'Title', 'Completion %', 'HLTB Story', 'Critic Rating']

@app.route('/')
def gaming_log():
    columns = [col for col in default_columns if col != 'Status']
    return render_template('gaming_log.html', columns=columns, data=data.to_dict('records'))

@app.route('/stats')
def stats():
    # Create a dictionary to store distribution by platform and status
    total_games_by_platform = {}

    for platform in data['Platform'].unique():
        total_by_status = {
            'Completed': len(data[(data['Status'] == 'Completed') & (data['Platform'] == platform)]),
            'Playing': len(data[(data['Status'] == 'Playing') & (data['Platform'] == platform)]),
            'Backlog': len(data[(data['Status'] == 'Backlog') & (data['Platform'] == platform)]),
        }
        total_games_by_platform[platform] = total_by_status

    # Calculate total for each status and total for all statuses
    total_status = {
        'Completed': sum(total['Completed'] for total in total_games_by_platform.values()),
        'Playing': sum(total['Playing'] for total in total_games_by_platform.values()),
        'Backlog': sum(total['Backlog'] for total in total_games_by_platform.values()),
    }
    total_all = sum(total_status.values())


    total_games = len(data)
    total_hours_played = int(data['Hours Played'].sum())
    average_hours_per_game = int(total_hours_played / total_games)
    total_completed_games = len(data[data['Status'] == 'Completed'])
    total_in_progress_games = len(data[data['Status'] == 'Playing'])
    total_unplayed_games = len(data[data['Status'] == 'Backlog'])

    completed_games = data[data['Status'] == 'Completed']
    valid_hours_played = completed_games[(completed_games['Hours Played'].notnull()) & (completed_games['Hours Played'] > 0)]
    average_hours_per_completed_game = int(valid_hours_played['Hours Played'].mean())
    
    most_played_platform = completed_games['Platform'].mode().iloc[0]

    valid_hours_played = completed_games[(completed_games['Hours Played'].notnull()) & (completed_games['Hours Played'] > 0)]
    
    longest_time_played = int(valid_hours_played['Hours Played'].max())
    shortest_time_played = int(valid_hours_played['Hours Played'].min())
    average_time_played = int(valid_hours_played['Hours Played'].mean())
    
    valid_critic_ratings = data[data['Critic Rating'].notnull() & (data['Critic Rating'] > 0)]

    # Calculate the average critic rating for each platform
    average_critic_rating_per_platform = {platform: valid_critic_ratings[valid_critic_ratings['Platform'] == platform]['Critic Rating'].mean() for platform in data['Platform'].unique()}
    
    # Remove platforms with null or 0 critic ratings
    average_critic_rating_per_platform = {platform: rating for platform, rating in average_critic_rating_per_platform.items() if pd.notna(rating) and rating > 0}
    
    current_year = datetime.now().year
    valid_date_completed = completed_games['Date Finished'].dropna()
    games_completed_this_year = len(valid_date_completed[valid_date_completed.astype(str).str.contains(str(current_year))])

    percentage_completed_vs_uncompleted = round((total_completed_games / total_games) * 100, 2)

    valid_hours_per_platform = completed_games[completed_games['Hours Played'] > 0]
    average_hours_per_platform = valid_hours_per_platform.groupby('Platform')['Hours Played'].mean().round(0).astype(int).to_dict()

    data['Year'] = pd.to_datetime(data['Date Finished']).dt.year

    total_hours_per_year = {}
    
    for year, group in data.groupby(data['Year']):
        total_hours_per_year[year] = int(group['Hours Played'].sum())

    # Sort the dictionary values in descending order
    sorted_average_hours_per_platform = dict(sorted(average_hours_per_platform.items(), key=lambda item: item[1], reverse=True))
    sorted_total_hours_per_year = dict(sorted(total_hours_per_year.items(), key=lambda item: item[1], reverse=True))
    sorted_average_critic_rating_per_platform = dict(sorted(average_critic_rating_per_platform.items(), key=lambda item: item[1], reverse=True))
    
    return render_template('stats.html',
                           average_hours_per_platform=sorted_average_hours_per_platform,
                           total_games_by_platform=total_games_by_platform,
                           total_status=total_status,
                           total_all=total_all,
                           total_hours_per_year=sorted_total_hours_per_year,
                           total_games=total_games,
                           total_hours_played=total_hours_played,
                           average_hours_per_game=average_hours_per_game,
                           total_completed_games=total_completed_games,
                           total_in_progress_games=total_in_progress_games,
                           total_unplayed_games=total_unplayed_games,
                           average_hours_per_completed_game=average_hours_per_completed_game,
                           most_played_platform=most_played_platform,
                           longest_time_played=longest_time_played,
                           shortest_time_played=shortest_time_played,
                           average_time_played=average_time_played,
                           average_critic_rating_per_platform=sorted_average_critic_rating_per_platform,  # Pass the sorted dictionary here
                           games_completed_this_year=games_completed_this_year,
                           percentage_completed_vs_uncompleted=percentage_completed_vs_uncompleted
                          )
    
if __name__ == '__main__':
    app.run(debug=True)

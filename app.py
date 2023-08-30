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

    total_games = len(data)
    total_hours_played = data['Hours Played'].sum()
    average_hours_per_game = total_hours_played / total_games
    total_completed_games = len(data[data['Status'] == 'Completed'])
    total_in_progress_games = len(data[data['Status'] == 'In Progress'])
    total_unplayed_games = len(data[data['Status'] == 'Unplayed'])
    average_completion_percentage = data['Completion %'].mean()
    most_played_platform = data['Platform'].mode().iloc[0]
    average_completion_by_platform = data.groupby('Platform')['Completion %'].mean().to_dict()
    longest_time_played = data['Hours Played'].max()
    shortest_time_played = data['Hours Played'].min()
    average_time_played = data['Hours Played'].mean()
    average_critic_rating = data['Critic Rating'].mean()
    highest_critic_rating = data['Critic Rating'].max()
    lowest_critic_rating = data['Critic Rating'].min()

    current_year = datetime.now().year
    games_completed_this_year = len(data[data['Status'] == 'Completed'][data['End Date'].str.contains(str(current_year))])
    # Calculate more time frame stats here

    most_played_genre = data['Genre'].mode().iloc[0]
    average_completion_by_genre = data.groupby('Genre')['Completion %'].mean().to_dict()
    percentage_completed_vs_uncompleted = (total_completed_games / total_games) * 100
    most_common_status = data['Status'].mode().iloc[0]
    average_hours_per_platform = data.groupby('Platform')['Hours Played'].mean().to_dict()

    # Calculate average hours played for games with a certain completion percentage range
    average_hours_by_completion_range = {}
    for range_start in range(0, 101, 20):
        range_end = range_start + 19
        mask = (data['Completion %'] >= range_start) & (data['Completion %'] <= range_end)
        average_hours = data[mask]['Hours Played'].mean()
        average_hours_by_completion_range[f'{range_start}-{range_end}%'] = average_hours

    # Calculate stats for total games above/below certain thresholds, platform percentage, time gap, decade count, and more
    # ...

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
                           average_completion_by_platform=average_completion_by_platform,
                           longest_time_played=longest_time_played,
                           shortest_time_played=shortest_time_played,
                           average_time_played=average_time_played,
                           average_critic_rating=average_critic_rating,
                           highest_critic_rating=highest_critic_rating,
                           lowest_critic_rating=lowest_critic_rating,
                           games_completed_this_year=games_completed_this_year,
                           most_played_genre=most_played_genre,
                           average_completion_by_genre=average_completion_by_genre,
                           percentage_completed_vs_uncompleted=percentage_completed_vs_uncompleted,
                           most_common_status=most_common_status,
                           average_hours_per_platform=average_hours_per_platform,
                           average_hours_by_completion_range=average_hours_by_completion_range)

if __name__ == '__main__':
    app.run(debug=True)    

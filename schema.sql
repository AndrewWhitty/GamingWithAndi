import sqlite3

# Create/connect to the database
conn = sqlite3.connect('game_database.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''
    CREATE TABLE games (
        id INTEGER PRIMARY KEY,
        title TEXT,
        platform TEXT,
        date_started TEXT,
        date_finished TEXT,
        status TEXT,
        release_date TEXT,
        format TEXT,
        size REAL,
        hltb_hours REAL,
        personal_hours REAL,
        metacritic_rating INTEGER,
        gameplay_rating INTEGER,
        story_rating INTEGER,
        controls_rating INTEGER,
        visuals_rating INTEGER,
        audio_rating INTEGER,
        value_rating INTEGER
    )
''')

# Commit changes and close the connection
conn.commit()
conn.close()
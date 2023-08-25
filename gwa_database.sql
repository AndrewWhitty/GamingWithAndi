CREATE TABLE IF NOT EXISTS Game (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    platform TEXT,
    date_started TEXT,
    date_finished TEXT,
    status TEXT,
    release_date TEXT,
    format TEXT,
    size DECIMAL,
    hours_to_complete_hltb REAL,
    hours_to_complete_personal REAL,
    metacritic_rating INTEGER,
    gameplay_story_rating INTEGER,
    controls_rating INTEGER,
    visuals_rating INTEGER,
    audio_rating INTEGER,
    value_rating INTEGER,
    rating INTEGER
);
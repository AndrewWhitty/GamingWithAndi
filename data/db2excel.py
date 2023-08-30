import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Function to convert Swift date to Excel serial date
def swift_to_excel_date(swift_date):
    if pd.isnull(swift_date):
        return swift_date
    reference_date = datetime(2001, 1, 1)
    excel_date = reference_date + timedelta(seconds=swift_date)
    return excel_date.date()
    
# Connect to the SQLite database
db_connection = sqlite3.connect('GameData.sqlite')

# Get a list of all tables in the database
cursor = db_connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
table_names = cursor.fetchall()

# Close the cursor
cursor.close()

# Initialize an empty list to store data frames
data_frames = []

# Iterate through table names and export 'ZGAME' to 'gametrackexport.csv'
for table_name in table_names:
    if table_name[0] == 'ZGAME':
        query = f'SELECT * FROM {table_name[0]}'
        data_frame = pd.read_sql_query(query, db_connection)

        # Export the unmodified DataFrame to 'gametrackexport.csv'
        initial_csv_filename = 'gametrackexport.csv'
        data_frame.to_csv(initial_csv_filename, index=False)
        print(f"Initial data exported to '{initial_csv_filename}'")

        # Column mappings
        column_mapping = {
            "ZCOMPLETION": "Completion %",
            "ZCRITICRATING": "Critic Rating",
            "ZFORMAT": "Format",
            "ZUSERRATING": "My Rating",
            "ZFINISHDATE": "Date Finished",
            "ZHOURSPLAYED": "Hours Played",
            "ZRELEASEDATE": "Release Date",
            "ZSTARTDATE": "Date Started",
            "ZTIMETOBEATCOMPLETE": "HLTB Complete",
            "ZTIMETOBEATEXTRAS": "HLTB Extras",
            "ZTIMETOBEATSTORY": "HLTB Story",  
            "ZBANNERURL": "Banner URL",
            "ZDEVELOPER": "Developer",
            "ZOWNEDPLATFORM": "Platform",
            "ZPOSTERURL": "Poster URL",
            "ZPUBLISHER": "Publisher",
            "ZREVIEW": "Review",
            "ZSTATUS": "Status",
            "ZSUMMARY": "Summary",
            "ZTITLE": "Title"
        }

        # Rename columns based on mappings and keep only specified columns
        columns_to_keep = list(column_mapping.values())
        data_frame = data_frame.rename(columns=column_mapping)
        data_frame = data_frame[columns_to_keep]

        # Convert specified columns to Excel dates
        date_columns = ["Date Finished", "Release Date", "Date Started"]
        for col in date_columns:
            data_frame[col] = data_frame[col].apply(swift_to_excel_date)

        # Replace values in the "Status" column and fill blank values with "Backlog"
        replacement_mapping = {
            "A ": "", "B ": "", "C ": "", "Play Later": "Backlog",
            "Wanted": "Wishlist", "Collection": "Backlog",
            "Finished": "Completed", "Play Next": "Backlog",
            "Now Playing": "Playing", "Abandoned": "Backlog"
        }
        data_frame['Status'] = data_frame['Status'].replace(replacement_mapping, regex=True).fillna("Backlog")

        # Append the data frame to the list
        data_frames.append(data_frame)

# Concatenate the data frames in the list
final_data_frame = pd.concat(data_frames, ignore_index=True)

# Export the modified DataFrame to 'gamedata.csv'
converted_csv_filename = 'gamedata.csv'
final_data_frame.to_csv(converted_csv_filename, index=False)
print(f"Modified data exported to '{converted_csv_filename}'")

# Close the database connection
db_connection.close()

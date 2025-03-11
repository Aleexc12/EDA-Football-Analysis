#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pymysql
import pandas as pd

def main():
    print("\n🚀 Data loading process started. Please wait until all data is fully loaded before running the `EDA.ipynb` notebook.")

    # 1) Database Connection
    #    Using environment variables to avoid hardcoded credentials
    db_config = {
        'host': os.getenv('MARIADB_HOST', 'localhost'),
        'user': os.getenv('MARIADB_USER', 'root'),
        'password': os.getenv('MARIADB_PASSWORD', ''),
        'database': os.getenv('MARIADB_DATABASE', 'futbol_db'),
        'port': 3306
    }
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    print("✅ Successfully connected to MariaDB from data_loader.")

    # 2) Read CSV files from /app/csvs
    # (Adjust filenames if necessary)
    results_df   = pd.read_csv("/app/csvs/results_clean.csv", parse_dates=['date'])
    shootouts_df = pd.read_csv("/app/csvs/shootouts_clean.csv", parse_dates=["date"])
    goals_df     = pd.read_csv("/app/csvs/goalscorers_clean.csv", parse_dates=["date"])

    # 3) Data type adjustments
    results_df['home_score'] = results_df['home_score'].astype(int)
    results_df['away_score'] = results_df['away_score'].astype(int)
    results_df['neutral'] = results_df['neutral'].astype(bool)

    # Dictionaries to cache IDs
    teams_dict = {}
    tournaments_dict = {}
    locations_dict = {}

    # Prepared queries
    insert_team_sql = "INSERT INTO teams (team_name) VALUES (%s)"
    insert_tournament_sql = "INSERT INTO tournaments (name) VALUES (%s)"
    insert_location_sql = "INSERT INTO locations (city, country) VALUES (%s, %s)"
    insert_match_sql = """
        INSERT INTO matches (
            date, home_team_id, away_team_id,
            home_score, away_score,
            tournament_id, location_id, neutral
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    # --------------------------------------------------------------------------
    # Insert Matches (and referenced tables: teams, tournaments, locations)
    # --------------------------------------------------------------------------
    for _, row in results_df.iterrows():
        home_team = row['home_team']
        away_team = row['away_team']
        tournament = row['tournament']
        city = row['city']
        country = row['country']

        # Team IDs
        if home_team not in teams_dict:
            cursor.execute(insert_team_sql, (home_team,))
            teams_dict[home_team] = cursor.lastrowid

        if away_team not in teams_dict:
            cursor.execute(insert_team_sql, (away_team,))
            teams_dict[away_team] = cursor.lastrowid

        home_team_id = teams_dict[home_team]
        away_team_id = teams_dict[away_team]

        # Tournament ID
        if tournament not in tournaments_dict:
            cursor.execute(insert_tournament_sql, (tournament,))
            tournaments_dict[tournament] = cursor.lastrowid
        tournament_id = tournaments_dict[tournament]

        # Location ID
        loc_key = (city, country)
        if loc_key not in locations_dict:
            cursor.execute(insert_location_sql, (city, country))
            locations_dict[loc_key] = cursor.lastrowid
        location_id = locations_dict[loc_key]

        # Insert match
        match_data = (
            row['date'].strftime('%Y-%m-%d'),
            home_team_id,
            away_team_id,
            row['home_score'],
            row['away_score'],
            tournament_id,
            location_id,
            row['neutral']
        )
        cursor.execute(insert_match_sql, match_data)

    connection.commit()
    print("✅ `results_clean` data successfully inserted into `matches` and referenced tables.")

    # --------------------------------------------------------------------------
    # Insert Shootouts
    # --------------------------------------------------------------------------
    insert_shootout_sql = """
        INSERT INTO shootouts (match_id, winner_team_id, first_shooter_team_id)
        VALUES (%s, %s, %s)
    """

    for index, row in shootouts_df.iterrows():
        date_str = row['date'].strftime('%Y-%m-%d')
        home_team_id = teams_dict.get(row['home_team'])
        away_team_id = teams_dict.get(row['away_team'])
        winner_team_id = teams_dict.get(row['winner'])

        if pd.isna(row['first_shooter']):
            first_shooter_team_id = None
        else:
            first_shooter_team_id = teams_dict.get(row['first_shooter'])

        # Validations
        if home_team_id is None or away_team_id is None or winner_team_id is None:
            print(f"⚠️ SKIPPING => Missing data in row {index}: {row.to_dict()}")
            continue

        # Retrieve match_id
        query_match_id = """
            SELECT match_id
            FROM matches
            WHERE date = %s
              AND home_team_id = %s
              AND away_team_id = %s
        """
        cursor.execute(query_match_id, (date_str, home_team_id, away_team_id))
        match_row = cursor.fetchone()
        if not match_row:
            print(f"⚠️ SKIPPING => No match found for {date_str}, {row['home_team']} vs {row['away_team']}")
            continue

        match_id = match_row[0]
        cursor.execute(insert_shootout_sql, (match_id, winner_team_id, first_shooter_team_id))

    connection.commit()
    print("✅ Shootouts successfully inserted.")

    # --------------------------------------------------------------------------
    # Insert Goals + Players
    # --------------------------------------------------------------------------
    goals_df['minute'] = goals_df['minute'].astype(float).astype(int)
    goals_df['own_goal'] = goals_df['own_goal'].astype(bool)
    goals_df['penalty'] = goals_df['penalty'].astype(bool)

    players_dict = {}  # (player_name, team_id) -> player_id

    insert_player_sql = "INSERT INTO players (player_name, team_id) VALUES (%s, %s)"
    insert_goal_sql = """
        INSERT INTO goals (
            match_id, team_id, player_id,
            minute, own_goal, penalty
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """

    for index, row in goals_df.iterrows():
        date_str = row['date'].strftime('%Y-%m-%d')
        home_team_id = teams_dict.get(row['home_team'])
        away_team_id = teams_dict.get(row['away_team'])

        if home_team_id is None or away_team_id is None:
            print(f"⚠️ SKIPPING => Home/Away team not found for row {index}")
            continue

        query_match_id = """
            SELECT match_id 
            FROM matches
            WHERE date = %s
              AND home_team_id = %s
              AND away_team_id = %s
        """
        cursor.execute(query_match_id, (date_str, home_team_id, away_team_id))
        match_row = cursor.fetchone()
        if not match_row:
            print(f"⚠️ SKIPPING => No match found in DB for {date_str}, {row['home_team']} vs {row['away_team']}")
            continue

        match_id = match_row[0]

        scoring_team_id = teams_dict.get(row['team'])
        if scoring_team_id is None:
            print(f"⚠️ SKIPPING => Scoring team '{row['team']}' not found.")
            continue

        # Insert/Get player_id
        player_name = row['scorer']
        pl_key = (player_name, scoring_team_id)
        if pl_key not in players_dict:
            cursor.execute(insert_player_sql, (player_name, scoring_team_id))
            players_dict[pl_key] = cursor.lastrowid

        player_id = players_dict[pl_key]

        # Insert goal
        goal_data = (
            match_id,
            scoring_team_id,
            player_id,
            row['minute'],
            row['own_goal'],
            row['penalty']
        )
        cursor.execute(insert_goal_sql, goal_data)

    connection.commit()
    print("✅ Goals and Players successfully inserted.")

    # Close the connection
    cursor.close()
    connection.close()
    print("\n🎉 Data loading completed successfully! You can now run `EDA.ipynb` safely.")

if __name__ == "__main__":
    main()

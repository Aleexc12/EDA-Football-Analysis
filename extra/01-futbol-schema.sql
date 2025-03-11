DROP SCHEMA IF EXISTS futbol_db;
CREATE SCHEMA futbol_db;

SET NAMES utf8mb4;
USE futbol_db;

-- 1. Teams table (Used in matches, players, and shootouts)
CREATE TABLE teams (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    team_name VARCHAR(100) UNIQUE NOT NULL
);

-- 2. Tournaments table (Used in matches)
CREATE TABLE tournaments (
    tournament_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

-- 3. Locations table (Used in matches)
CREATE TABLE locations (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL
);

-- 4. Matches table (Used in shootouts and goals)
CREATE TABLE matches (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    home_team_id INT NOT NULL,
    away_team_id INT NOT NULL,
    home_score INT NOT NULL,
    away_score INT NOT NULL,
    tournament_id INT NULL,
    location_id INT NULL,
    neutral BOOLEAN NOT NULL,
    FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (away_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (tournament_id) REFERENCES tournaments(tournament_id) ON DELETE SET NULL,
    FOREIGN KEY (location_id) REFERENCES locations(location_id) ON DELETE SET NULL
);

-- 5. Players table (Used in goals)
CREATE TABLE players (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    player_name VARCHAR(255) NOT NULL,
    team_id INT NULL,
    FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE SET NULL
);

-- 6. Shootouts table (Used in shootouts)
CREATE TABLE shootouts (
    shootout_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    winner_team_id INT NOT NULL,
    first_shooter_team_id INT NULL,
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (winner_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (first_shooter_team_id) REFERENCES teams(team_id)
);

-- 7. Goals table (Last because it depends on matches, teams, and players)
CREATE TABLE goals (
    goal_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    team_id INT NOT NULL,
    player_id INT NOT NULL,
    minute INT NOT NULL,
    own_goal BOOLEAN NOT NULL,
    penalty BOOLEAN NOT NULL,
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

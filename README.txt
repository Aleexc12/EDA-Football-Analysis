Here is your **cleaned and final version** of the `README.txt`, without bold formatting but keeping the structure clear and easy to read.

---

# EDA PROJECT - FOOTBALL DATA ANALYSIS AND SAKILA DATABASE

This project provides the infrastructure for analyzing football data, including preprocessing, automated loading into a MariaDB database, and exploratory data analysis using Jupyter Notebook. The Sakila database is also included for additional experimentation.

---

## WORKFLOW

1. Download CSV files  
2. Visual analysis and data cleaning  
3. Define entity-relationship schema with cleaned data  
4. Create the database  
5. Define database schema based on the entity-relationship model  
6. Automatically load cleaned data using a Python script  
7. Perform graphical analysis of different tables  
8. Run SQL queries to verify table functionality  

---

## PROJECT DIRECTORY STRUCTURE

📦 EDA_PROJECT/  
 ├── 📂 docker/ - Docker configuration files  
 │   ├── 📝 docker-compose.yml - Defines and configures MariaDB and Jupyter services  
 │  
 ├── 📂 extra/ - Data, SQL scripts, and CSV files  
 │   ├── 📂 csvs/ - Folder containing raw and cleaned CSV files  
 │   ├── 📂 mariadb_data/ - Persistent MariaDB data  
 │   ├── 📝 00-setup.sql - Creates the databases (futbol_db)  
 │   ├── 📝 01-futbol-schema.sql - Defines the schema for futbol_db  
 │  
 ├── 📂 notebooks/ - Jupyter notebooks and data scripts  
 │   ├── 📓 EDA.ipynb - Data exploration and visualization  
 │   ├── 📝 insert_data_script.py - Automated data loading script (replaces manual loading in Jupyter)  
 │   ├── 📓 preprocessing.ipynb - Cleans and transforms CSV data (not required for execution)  
 │  
 ├── 📝 README.txt - Project documentation  

---

## DATA PROCESSING

THE CLEANED CSV FILES ARE ALREADY PROVIDED, SO RUNNING THE PREPROCESSING NOTEBOOK IS NOT NECESSARY UNLESS MODIFICATIONS ARE NEEDED.

### PREPROCESSING (preprocessing.ipynb)  
- Reads raw CSV files and generates cleaned versions (`*_clean.csv`).  
- Normalizes country names, converts dates, and removes null values.  
- Maps former country names to their current names, except for ambiguous cases like the USSR and CIS, which are excluded.  

Note: After verifying the dataset, former names were found only in `results.csv`, so the mapping is applied only there.

### AUTOMATED DATA LOADING (insert_data_script.py)  
- This script automatically loads cleaned CSV data into `futbol_db`.  
- It replaces the previous manual loading process in Jupyter Notebook.  
- It ensures that tables are populated in the correct order, handling foreign key dependencies.  

### EXPLORATORY DATA ANALYSIS (EDA.ipynb)  
- Runs SQL queries and generates visualizations (boxplots, heatmaps, bar charts, etc.).  
- Analyzes historical football match trends from 1872 to 2024.  
- Includes key insights such as:  
  - Goals distribution per match  
  - Teams with the most goals scored  
  - Relationship between home and away goals  
  - Matches played per year  

---

## HOW TO RUN THE PROJECT

### 1️⃣ START THE DOCKER ENVIRONMENT  
Navigate to the `/docker` folder and run:  
```bash
docker-compose up
```
This starts the MariaDB database and Jupyter Notebook server.  

### 2️⃣ AUTOMATICALLY LOAD DATA  
Once the database is running, the data will be automatically inserted using `insert_data_script.py`.  

### 3️⃣ ACCESS JUPYTER NOTEBOOK  
After launching Docker, look for a message like this:  
```
http://127.0.0.1:8888/lab?token=your_token_here
```
Copy and paste the link into your browser.  

### 4️⃣ RUN EXPLORATORY DATA ANALYSIS (EDA)  
Inside Jupyter, open `EDA.ipynb` and run the cells to:  
- Query the database  
- Generate visualizations  
- Analyze trends in football data  

---

## DATASET INFORMATION

This dataset contains detailed information on international football matches from 1872 to 2024, covering over 47,000 matches. It includes teams, match dates, locations, tournaments, and results, enabling analysis of how international football has evolved over time.

The dataset consists of the following CSV files:  
- `results.csv` - Match records (date, teams, score, location)  
- `shootouts.csv` - Penalty shootout data  
- `former_names.csv` - Historical country name changes  
- `scorers.csv` - List of players who scored goals  

Source: The data is collected from historical records and is organized on Kaggle for easy analysis.  

Kaggle Dataset: [International Football Results](https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017/data)  

---

## KEY INSIGHTS FROM THE ANALYSIS

- Trends in football over the years  
- Impact of penalty shootouts on match outcomes  
- Goal distribution and scoring patterns  
- Performance of national teams over time  
- Tournament influence on match dynamics  

---

## NOTES & CONSIDERATIONS

- The `first_shooter` column is kept despite many null values, as it may help analyze whether shooting first provides an advantage in penalty shootouts.  
- Do not open `EDA.ipynb` until all data has been loaded, or queries may return errors.  
- Former country names are mapped to their current names, except for ambiguous cases like USSR and CIS, which are excluded.  

---

## FUTURE IMPROVEMENTS

- Automate data ingestion directly from Kaggle  
- Expand statistical models for better insights  
- Integrate machine learning to predict match outcomes  
- Compare tournament formats and their impact on results  

---

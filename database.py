import sqlite3
import datetime

DB_NAME = 'pcos.db'

def initialize_database():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE
        )
    ''')

    # Create daily_logs table
    c.execute('''
        CREATE TABLE IF NOT EXISTS daily_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            Age REAL,
            Weight REAL,
            Height REAL,
            BMI REAL,
            Cycle_R_I INTEGER,
            Cycle_length_days INTEGER,
            Marriage_Status_Yrs INTEGER,
            Pregnant_Y_N INTEGER,
            Hip REAL,
            Waist REAL,
            Waist_Hip_Ratio REAL,
            Weight_gain_Y_N INTEGER,
            Hair_growth_Y_N INTEGER,
            Skin_darkening_Y_N INTEGER,
            Hair_loss_Y_N INTEGER,
            Pimples_Y_N INTEGER,
            Fast_food_Y_N INTEGER,
            Reg_Exercise_Y_N INTEGER,
            Irregular_Periods INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

def register_user(username, email):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, email) VALUES (?, ?)', (username, email))
        conn.commit()
    except sqlite3.IntegrityError as e:
        # Handle duplicate username/email
        print(f"Error registering user: {e}")
        return False
    finally:
        conn.close()
    return True

def get_user_id(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def add_daily_log(user_id, data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO daily_logs (
            user_id, date, Age, Weight, Height, BMI, Cycle_R_I, Cycle_length_days,
            Marriage_Status_Yrs, Pregnant_Y_N, Hip, Waist, Waist_Hip_Ratio, Weight_gain_Y_N,
            Hair_growth_Y_N, Skin_darkening_Y_N, Hair_loss_Y_N, Pimples_Y_N, Fast_food_Y_N,
            Reg_Exercise_Y_N, Irregular_Periods
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, str(datetime.date.today()), *data))
    conn.commit()
    conn.close()

def get_user_logs(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Fetch date and all data columns
    c.execute('''
        SELECT date, Age, Weight, Height, BMI, Cycle_R_I, Cycle_length_days,
               Marriage_Status_Yrs, Pregnant_Y_N, Hip, Waist, Waist_Hip_Ratio,
               Weight_gain_Y_N, Hair_growth_Y_N, Skin_darkening_Y_N, Hair_loss_Y_N,
               Pimples_Y_N, Fast_food_Y_N, Reg_Exercise_Y_N, Irregular_Periods
        FROM daily_logs WHERE user_id = ? ORDER BY date
    ''', (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_average_inputs(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT 
            AVG(Age), AVG(Weight), AVG(Height), AVG(BMI), AVG(Cycle_R_I),
            AVG(Cycle_length_days), AVG(Marriage_Status_Yrs), AVG(Pregnant_Y_N),
            AVG(Hip), AVG(Waist), AVG(Waist_Hip_Ratio), AVG(Weight_gain_Y_N),
            AVG(Hair_growth_Y_N), AVG(Skin_darkening_Y_N), AVG(Hair_loss_Y_N),
            AVG(Pimples_Y_N), AVG(Fast_food_Y_N), AVG(Reg_Exercise_Y_N),
            AVG(Irregular_Periods)
        FROM daily_logs WHERE user_id = ?
    ''', (user_id,))
    result = c.fetchone()
    conn.close()
    return list(result) if result else [None]*19

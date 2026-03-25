import psycopg2
from config import Config

def get_db_connection():
    conn = psycopg2.connect(Config.DATABASE_URL)
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            task TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT FALSE
        )
    ''')
    conn.commit()
    
    cur.close()
    conn.close()
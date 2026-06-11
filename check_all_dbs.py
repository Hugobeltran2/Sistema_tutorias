import sqlite3
import os

dbs = ['tutorias.sqlite', 'tutorias_posgrado/tutoria.sqlite']

for db_path in dbs:
    if os.path.exists(db_path):
        print(f"--- Checking {db_path} ---")
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [t[0] for t in cursor.fetchall()]
            print(f"Tables: {tables}")
            
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"Table: {table}, Rows: {count}")
                
                cursor.execute(f"SELECT * FROM {table} LIMIT 2")
                data = cursor.fetchall()
                print(f"Sample: {data}")
            conn.close()
        except Exception as e:
            print(f"Error checking {db_path}: {e}")
    else:
        print(f"File {db_path} not found")

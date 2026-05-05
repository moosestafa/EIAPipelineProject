import sqlite3 as sqlite
import uuid 
from datetime import datetime



def init_db():
    conn = sqlite.connect('db/pipeline_metadata.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS metadata(run_id TEXT, 
                          run_timestamp text, rows_fetched int,
                          rows_written int, s3_path TEXT, status int, error_message TEXT, duration_seconds real);""")
    conn.commit()
    conn.close()

def log_run(rows_fetched, rows_written,s3_path,status,duration_seconds,error_message="None",):
    conn = sqlite.connect('db/pipeline_metadata.db')
    cursor = conn.cursor()
    run_id = str(uuid.uuid4())
    cursor.execute("insert into metadata VALUES(?,?,?,?,?,?,?,?)",(run_id,
                   datetime.now(),rows_fetched,rows_written,s3_path,status,error_message,duration_seconds))
    conn.commit()
    conn.close()
    


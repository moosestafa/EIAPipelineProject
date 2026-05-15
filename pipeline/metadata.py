import sqlite3 as sqlite
import uuid 
from datetime import datetime
import os
import boto3
from botocore.exceptions import ClientError



def init_db():
    os.makedirs('db', exist_ok=True)
    conn = sqlite.connect('db/pipeline_metadata.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS metadata(run_id TEXT, 
                          run_timestamp text, rows_fetched int,
                          rows_written int,state TEXT, month int, year int, s3_path TEXT, status int, error_message TEXT, duration_seconds real);""")
    conn.commit()
    conn.close()

def log_run(rows_fetched, rows_written,state,month,year,s3_path,status,duration_seconds,error_message="None",):
    conn = sqlite.connect('db/pipeline_metadata.db')
    cursor = conn.cursor()
    run_id = str(uuid.uuid4())
    cursor.execute("insert into metadata VALUES(?,?,?,?,?,?,?,?,?,?,?)",(run_id,
                   datetime.now(),rows_fetched,rows_written,state,month,year,s3_path,status,error_message,duration_seconds))
    conn.commit()
    conn.close()

def backfill():
    return 2020,1

    
def increment(state):
    conn = sqlite.connect('db/pipeline_metadata.db')
    cursor = conn.cursor()
    month_year = cursor.execute("SELECT year, month FROM metadata WHERE status = 1 AND state=? ORDER BY year DESC, month DESC LIMIT 1",(state,)).fetchone()
    conn.close()
    if month_year is None:
        return backfill()

    year = month_year[0]
    month = month_year[1]
    
    if month == 12:
        month = 1
        year = year+1
        return year,month
    else:
        return year,month+1
    


def download_metadata():
    try:
        s3 = boto3.client('s3')
        s3.download_file(Bucket='eia-pipeline-md', 
                     Key='metadata/pipeline_metadata.db',
                     Filename='db/pipeline_metadata.db')
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            pass  # File doesn't exist yet, init_db() will create it
        else:
            raise  # Re-raise unexpected errors


def upload_metadata():
    s3 = boto3.client('s3')
    s3.upload_file(
    Filename='db/pipeline_metadata.db',   # Path to your local file
    Bucket='eia-pipeline-md',   # Name of the target S3 bucket
    Key='metadata/pipeline_metadata.db'        # Name of the object in S3
    )


from pipeline.eia_client import fetch_data
from pipeline.transform import create_dataframe, clean_data, transform_data
from pipeline.loader import save_parquet
from pipeline.metadata import init_db,log_run
import time 
#initializes metadata database 
init_db()
#makes api request for each month of the year and calls functions to create dataframe, clean and transform data, create parquet file and upload to S3 
for i in range(1,13):
    
    start = time.time()
    month = str(i).zfill(2)
    rawdata = fetch_data("TX",f"2024-{month}",f"2024-{month}")
    rows_fetched = len(rawdata["response"]["data"]) 
    df = create_dataframe(rawdata)
    

    df=clean_data(df)

    df = transform_data(df)

    end = time.time()
    rows_written = len(df)    

    s3_path=save_parquet(df,"TX","2024",str(i).zfill(2))

    
    log_run(rows_fetched,rows_written,s3_path,1,end-start,"None")

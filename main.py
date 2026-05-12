from pipeline.eia_client import fetch_data
from pipeline.transform import create_dataframe, clean_data, transform_data
from pipeline.loader import save_parquet
from pipeline.metadata import init_db,log_run,increment,backfill
import time 
#initializes metadata database 
init_db()
#makes api request for each month of the year and calls functions to create dataframe, clean and transform data, create parquet file and upload to S3 
year_month = increment()
year = year_month[0]
month = str(year_month[1]).zfill(2)
rawdata = fetch_data("TX",f"{year}-{month}",f"{year}-{month}")
while len(rawdata["response"]["data"]) != 0:
    
    start = time.time()
    rows_fetched = len(rawdata["response"]["data"]) 
    df = create_dataframe(rawdata)
    

    df=clean_data(df)

    df = transform_data(df)

    end = time.time()
    rows_written = len(df)    

    s3_path=save_parquet(df,"TX",f"{year}",str(month).zfill(2))

    
    log_run(rows_fetched,rows_written,month,year,s3_path,1,end-start,"None")
    year_month = increment()
    year = year_month[0]
    month = str(year_month[1]).zfill(2)
    rawdata = fetch_data("TX",f"{year}-{month}",f"{year}-{month}")

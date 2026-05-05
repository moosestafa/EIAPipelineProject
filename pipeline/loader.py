
import boto3
import os
from dotenv import load_dotenv

#load environment variables
load_dotenv()

#converts the dataframe to a parquet file and uploads it to S3 
def save_parquet(df,state,year,month):
    df.to_parquet(f"data/raw/{state}-{year}-{month}.parquet")
    s3_uploader = boto3.client('s3',aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                               aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),region_name = os.getenv("AWS_REGION") )
    s3_uploader.upload_file(f"data/raw/{state}-{year}-{month}.parquet", os.getenv("AWS_BUCKET_NAME"), f"eia/crude_production/state={state}/year={year}/month={month}/data.parquet")
    return f"eia/crude_production/state={state}/year={year}/month={month}/data.parquet"
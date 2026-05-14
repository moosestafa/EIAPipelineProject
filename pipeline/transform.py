
import pandas as pd



#creates dataframe
def create_dataframe(data):
    df = pd.DataFrame(data["response"]["data"])
    return df
#drops unneccessary columns, and makes sure that the correct units are being read in, then drops units table
def clean_data(df):
    df = df[df["series"].str.startswith("MCRFP")]
    df=df.drop(columns=['duoarea','product', 'product-name', 'process','process-name', 'series', 'series-description'])
    df = df[df["units"] == "MBBL"]    
    df= df.drop(columns=["units"])
    
    return df
#sorts data by month, and converts to proper data types
def transform_data(df):
    df = df.sort_values(by = "period")
    df["period"]=df["period"].astype("datetime64[s]")
    df["value"] = df["value"].astype("float64")
    df['year'] = df['period'].dt.year
    df['month'] = df['period'].dt.month
    df = df.rename(columns={"area-name": "area_name"})
    df = df.reset_index(drop=True)
    return df







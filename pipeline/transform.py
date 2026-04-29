
import pandas as pd




def create_dataframe(data):
    df = pd.DataFrame(data["response"]["data"])
    return df

def clean_data(df):
    df=df.drop(columns=['duoarea','product', 'product-name', 'process','process-name', 'series', 'series-description'])
    df = df[df["units"] == "MBBL"]    
    df= df.drop(columns=["units"])
    return df

def transform_data(df):
    df = df.sort_values(by = "period")
    df["period"]=df["period"].astype("datetime64[s]")
    df["value"] = df["value"].astype("float64")
    df['year'] = df['period'].dt.year
    df['month'] = df['period'].dt.month
    df = df.reset_index(drop=True)
    return df










def save_parquet(df,state, start_month,end_month):
    df.to_parquet(f"data/raw/{state}-{start_month}-{end_month}.parquet")

#data/raw